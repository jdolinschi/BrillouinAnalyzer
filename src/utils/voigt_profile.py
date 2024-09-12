import numpy as np
from scipy.optimize import curve_fit
from scipy.special import wofz  # For Voigt profile


# Define the Voigt profile
def voigt_profile(x, amplitude, center, sigma, gamma):
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2))
    return amplitude * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))


# VoigtFitter Class
class VoigtFitter:
    def __init__(self, inverted=False):
        self.x = None
        self.y = None
        self.fit_params = None
        self.fit_cov = None
        self.inverted = inverted  # Flag to indicate if the data is inverted

    def fit(self, x, y, initial_guess=None):
        self.x = x
        self.y = -y if self.inverted else y  # Invert y data if inverted is True

        # Provide an initial guess if not given
        if initial_guess is None:
            amplitude_guess = np.max(self.y) - np.min(self.y)
            center_guess = x[np.argmax(self.y)]
            sigma_guess = np.std(x) / 2
            gamma_guess = sigma_guess
            initial_guess = [amplitude_guess, center_guess, sigma_guess, gamma_guess]

        # Perform the curve fitting using scipy's curve_fit
        self.fit_params, self.fit_cov = curve_fit(voigt_profile, x, self.y, p0=initial_guess)

        # Store fit results for further analysis
        return self.get_fit_curve(x)

    def get_fit_curve(self, x):
        """Return the fitted Voigt curve, re-inverted if needed."""
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        fit_curve = voigt_profile(x, *self.fit_params)
        return -fit_curve if self.inverted else fit_curve

    def get_parameter(self, param_name):
        """Return only the specified parameter."""
        if self.fit_params is None:
            raise ValueError("No fit performed yet.")

        param_map = {
            'amplitude': self.fit_params[0],
            'center': self.fit_params[1],
            'sigma': self.fit_params[2],
            'gamma': self.fit_params[3],
            'fwhm': self.calculate_fwhm(),
            'area': self.calculate_area(),
        }

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
        return 0.5346 * 2 * gamma + np.sqrt(0.2166 * (2 * gamma) ** 2 + (2.0 * sigma * np.sqrt(2 * np.log(2))) ** 2)

    def calculate_area(self):
        """Calculate the area under the Voigt peak."""
        amplitude = self.fit_params[0]
        sigma = self.fit_params[2]
        gamma = self.fit_params[3]
        return amplitude * np.pi * (gamma + sigma)

    def goodness_of_fit(self):
        """Calculate R-squared or another measure of fit quality."""
        residuals = self.y - self.get_fit_curve(self.x)
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((self.y - np.mean(self.y)) ** 2)
        return 1 - (ss_res / ss_tot)

# Example usage:
# fitter = VoigtFitter(inverted=True)  # Set inverted to True for upside-down peaks
# fit_curve = fitter.fit(x_data, y_data)
# fwhm = fitter.get_parameter('fwhm')
# r_squared = fitter.goodness_of_fit()
