import numpy as np
from scipy.optimize import curve_fit
from scipy.special import voigt_profile  # For Voigt profile

# Define the Voigt profile
def voigt_profile_custom(x, amplitude, center, sigma, gamma):
    return amplitude * voigt_profile(x - center, sigma, gamma)

# Define the Pseudo-Voigt profile
def pseudo_voigt(x, amplitude, center, sigma, gamma):
    eta = gamma / (gamma + sigma)
    gauss = np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
    lorentz = gamma ** 2 / ((x - center) ** 2 + gamma ** 2)
    return amplitude * (eta * lorentz + (1 - eta) * gauss)

# Define the Asymmetric Pseudo-Voigt function
def asymmetric_pseudo_voigt(x, amplitude, center, sigma, gamma, asymmetry):
    delta = x - center
    sigma_mod = sigma * (1 + asymmetry * np.sign(delta))
    gamma_mod = gamma * (1 + asymmetry * np.sign(delta))
    eta = gamma_mod / (gamma_mod + sigma_mod)
    gauss = np.exp(-delta ** 2 / (2 * sigma_mod ** 2))
    lorentz = gamma_mod ** 2 / (delta ** 2 + gamma_mod ** 2)
    return amplitude * (eta * lorentz + (1 - eta) * gauss)

class VoigtFitter:
    def __init__(self, inverted=False, method='voigt'):
        self.x = None
        self.y = None
        self.fit_params = None
        self.fit_cov = None
        self.inverted = inverted
        self.method = method

    def fit(self, x, y, initial_guess=None, maxfev=1000, increase_fit_time_on_failure=False):
        self.x = x
        self.y = y

        # Select fitting function based on method
        function_map = {
            'voigt': voigt_profile_custom,
            'pseudo_voigt': pseudo_voigt,
            'asymmetric_pseudo_voigt': asymmetric_pseudo_voigt,
        }
        fitting_function = function_map.get(self.method)
        if not fitting_function:
            raise ValueError(f"Fitting method '{self.method}' not recognized.")

        # Provide an initial guess if not given
        if initial_guess is None:
            baseline = np.median(self.y)
            peak_value = np.min(self.y) if self.inverted else np.max(self.y)
            amplitude_guess = peak_value - baseline  # Negative for inverted peaks
            center_guess = x[np.argmin(self.y)] if self.inverted else x[np.argmax(self.y)]
            sigma_guess = (np.max(x) - np.min(x)) / 6  # Approximate
            gamma_guess = sigma_guess
            if self.method == 'asymmetric_pseudo_voigt':
                asymmetry_guess = 0.0
                initial_guess = [amplitude_guess, center_guess, sigma_guess, gamma_guess, asymmetry_guess]
            else:
                initial_guess = [amplitude_guess, center_guess, sigma_guess, gamma_guess]

        # Perform the curve fitting
        try:
            self.fit_params, self.fit_cov = curve_fit(
                fitting_function, x, self.y, p0=initial_guess, maxfev=maxfev
            )
        except RuntimeError as e:
            if increase_fit_time_on_failure:
                try:
                    self.fit_params, self.fit_cov = curve_fit(
                        fitting_function, x, self.y, p0=initial_guess, maxfev=maxfev * 10
                    )
                except RuntimeError as e:
                    print(f"Fit did not converge after increasing maxfev: {e}")
                    self.fit_params = None
                    self.fit_cov = None
                    return None
            else:
                print(f"Fit did not converge: {e}")
                self.fit_params = None
                self.fit_cov = None
                return None

        return self.get_fit_curve(x)

    def get_fit_curve(self, x):
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        function_map = {
            'voigt': voigt_profile_custom,
            'pseudo_voigt': pseudo_voigt,
            'asymmetric_pseudo_voigt': asymmetric_pseudo_voigt,
        }
        fitting_function = function_map.get(self.method)
        if not fitting_function:
            raise ValueError(f"Fitting method '{self.method}' not recognized.")

        return fitting_function(x, *self.fit_params)

    def get_parameter(self, param_name):
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        param_names = ['amplitude', 'center', 'sigma', 'gamma']
        if self.method == 'asymmetric_pseudo_voigt':
            param_names.append('asymmetry')

        param_map = dict(zip(param_names, self.fit_params))

        param_map['fwhm'] = self.calculate_fwhm()
        param_map['area'] = self.calculate_area()

        if param_name not in param_map:
            raise ValueError(f"Parameter '{param_name}' not recognized.")

        return param_map[param_name]

    def get_parameters(self, param_names):
        return {param: self.get_parameter(param) for param in param_names}

    def calculate_fwhm(self):
        sigma = self.fit_params[2]
        gamma = self.fit_params[3]
        if self.method == 'asymmetric_pseudo_voigt':
            asymmetry = self.fit_params[4]
            sigma_left = sigma * (1 + asymmetry)
            sigma_right = sigma * (1 - asymmetry)
            gamma_left = gamma * (1 + asymmetry)
            gamma_right = gamma * (1 - asymmetry)
            fwhm_left = 0.5346 * 2 * gamma_left + np.sqrt(
                0.2166 * (2 * gamma_left) ** 2 + (2 * sigma_left * np.sqrt(2 * np.log(2))) ** 2
            )
            fwhm_right = 0.5346 * 2 * gamma_right + np.sqrt(
                0.2166 * (2 * gamma_right) ** 2 + (2 * sigma_right * np.sqrt(2 * np.log(2))) ** 2
            )
            return (fwhm_left + fwhm_right) / 2
        else:
            return 0.5346 * 2 * gamma + np.sqrt(
                0.2166 * (2 * gamma) ** 2 + (2 * sigma * np.sqrt(2 * np.log(2))) ** 2
            )

    def calculate_area(self):
        amplitude = self.fit_params[0]
        sigma = self.fit_params[2]
        gamma = self.fit_params[3]
        if self.method == 'asymmetric_pseudo_voigt':
            asymmetry = self.fit_params[4]
            sigma_left = sigma * (1 + asymmetry)
            sigma_right = sigma * (1 - asymmetry)
            gamma_left = gamma * (1 + asymmetry)
            gamma_right = gamma * (1 - asymmetry)
            area_left = amplitude * np.pi * (gamma_left + sigma_left)
            area_right = amplitude * np.pi * (gamma_right + sigma_right)
            return (area_left + area_right) / 2
        else:
            return amplitude * np.pi * (gamma + sigma)

    def goodness_of_fit(self):
        residuals = self.y - self.get_fit_curve(self.x)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.y - np.mean(self.y)) ** 2)
        return 1 - (ss_res / ss_tot)
