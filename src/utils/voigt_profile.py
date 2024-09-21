import numpy as np
from scipy.optimize import curve_fit
from scipy.special import wofz  # For Voigt profile
from scipy.special import erf   # For asymmetric functions

# Define the Voigt profile
def voigt_profile(x, amplitude, center, sigma, gamma):
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2))
    return amplitude * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))

# Define the Pseudo-Voigt profile
def pseudo_voigt(x, amplitude, center, sigma, gamma):
    eta = gamma / (gamma + sigma)
    gauss = np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
    lorentz = gamma ** 2 / ((x - center) ** 2 + gamma ** 2)
    return amplitude * (eta * lorentz + (1 - eta) * gauss)

# Define the Asymmetric Pseudo-Voigt (Martinelli) function
def asymmetric_pseudo_voigt(x, amplitude, center, sigma, gamma, asymmetry):
    # Adjust sigma and gamma based on asymmetry parameter
    sigma_mod = sigma * (1 + asymmetry * np.sign(x - center))
    gamma_mod = gamma * (1 + asymmetry * np.sign(x - center))
    eta = gamma_mod / (gamma_mod + sigma_mod)
    gauss = np.exp(-((x - center) ** 2) / (2 * sigma_mod ** 2))
    lorentz = gamma_mod ** 2 / ((x - center) ** 2 + gamma_mod ** 2)
    return amplitude * (eta * lorentz + (1 - eta) * gauss)

# VoigtFitter Class
class VoigtFitter:
    def __init__(self, inverted=False, method='voigt'):
        self.x = None
        self.y = None
        self.fit_params = None
        self.fit_cov = None
        self.inverted = inverted  # Flag to indicate if the data is inverted
        self.method = method  # Fitting method: 'voigt', 'pseudo_voigt', 'asymmetric_pseudo_voigt'

    def fit(self, x, y, initial_guess=None, maxfev=1000, increase_fit_time_on_failure=False):
        self.x = x
        self.y = y  # Do not invert y data

        # Select fitting function based on method
        function_map = {
            'voigt': voigt_profile,
            'pseudo_voigt': pseudo_voigt,
            'asymmetric_pseudo_voigt': asymmetric_pseudo_voigt,
        }
        fitting_function = function_map.get(self.method)
        if fitting_function is None:
            raise ValueError(f"Fitting method '{self.method}' not recognized.")

        # Provide an initial guess if not given
        if initial_guess is None:
            amplitude_guess = np.max(self.y) - np.min(self.y)
            if self.inverted:
                amplitude_guess = -abs(amplitude_guess)
                center_guess = x[np.argmin(self.y)]
            else:
                amplitude_guess = abs(amplitude_guess)
                center_guess = x[np.argmax(self.y)]
            sigma_guess = np.std(x) / 2
            gamma_guess = sigma_guess
            if self.method == 'asymmetric_pseudo_voigt':
                asymmetry_guess = 0.0
                initial_guess = [amplitude_guess, center_guess, sigma_guess, gamma_guess, asymmetry_guess]
            else:
                initial_guess = [amplitude_guess, center_guess, sigma_guess, gamma_guess]

        # Perform the curve fitting using scipy's curve_fit
        try:
            self.fit_params, self.fit_cov = curve_fit(
                fitting_function, x, self.y, p0=initial_guess, maxfev=maxfev
            )
        except RuntimeError as e:
            if increase_fit_time_on_failure:
                try:
                    # Try again with higher maxfev
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

        # Store fit results for further analysis
        return self.get_fit_curve(x)

    def get_fit_curve(self, x):
        """Return the fitted curve."""
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        # Select fitting function based on method
        function_map = {
            'voigt': voigt_profile,
            'pseudo_voigt': pseudo_voigt,
            'asymmetric_pseudo_voigt': asymmetric_pseudo_voigt,
        }
        fitting_function = function_map.get(self.method)
        if fitting_function is None:
            raise ValueError(f"Fitting method '{self.method}' not recognized.")

        fit_curve = fitting_function(x, *self.fit_params)
        return fit_curve

    def get_parameter(self, param_name):
        """Return only the specified parameter."""
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        param_map = {}
        param_names = ['amplitude', 'center', 'sigma', 'gamma']
        if self.method == 'asymmetric_pseudo_voigt':
            param_names.append('asymmetry')

        for i, name in enumerate(param_names):
            param_map[name] = self.fit_params[i]

        param_map['fwhm'] = self.calculate_fwhm()
        param_map['area'] = self.calculate_area()

        if param_name not in param_map:
            raise ValueError(f"Parameter '{param_name}' not recognized.")

        return param_map[param_name]

    def get_parameters(self, param_names):
        """Return a dictionary of requested parameters."""
        return {param: self.get_parameter(param) for param in param_names}

    def calculate_fwhm(self):
        """Calculate the FWHM from sigma and gamma."""
        sigma = self.fit_params[2]
        gamma = self.fit_params[3]
        if self.method == 'asymmetric_pseudo_voigt':
            asymmetry = self.fit_params[4]
            # Adjust sigma and gamma for asymmetry
            sigma_left = sigma * (1 + asymmetry)
            sigma_right = sigma * (1 - asymmetry)
            gamma_left = gamma * (1 + asymmetry)
            gamma_right = gamma * (1 - asymmetry)
            fwhm_left = 0.5346 * 2 * gamma_left + np.sqrt(
                0.2166 * (2 * gamma_left) ** 2 + (2.0 * sigma_left * np.sqrt(2 * np.log(2))) ** 2
            )
            fwhm_right = 0.5346 * 2 * gamma_right + np.sqrt(
                0.2166 * (2 * gamma_right) ** 2 + (2.0 * sigma_right * np.sqrt(2 * np.log(2))) ** 2
            )
            return (fwhm_left + fwhm_right) / 2  # Average FWHM
        else:
            return 0.5346 * 2 * gamma + np.sqrt(
                0.2166 * (2 * gamma) ** 2 + (2.0 * sigma * np.sqrt(2 * np.log(2))) ** 2
            )

    def calculate_area(self):
        """Calculate the area under the peak."""
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
            return (area_left + area_right) / 2  # Average area
        else:
            return amplitude * np.pi * (gamma + sigma)

    def goodness_of_fit(self):
        """Calculate R-squared or another measure of fit quality."""
        residuals = self.y - self.get_fit_curve(self.x)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.y - np.mean(self.y)) ** 2)
        return 1 - (ss_res / ss_tot)

# Example usage:
# fitter = VoigtFitter(inverted=True, method='pseudo_voigt')
# fit_curve = fitter.fit(x_data, y_data)
# fwhm = fitter.get_parameter('fwhm')
# r_squared = fitter.goodness_of_fit()
