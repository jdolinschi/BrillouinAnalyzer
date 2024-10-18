import numpy as np


class BrillouinCalibration:
    def __init__(self):
        self.laser_wavelength_nm = None
        self.mirror_spacing_mm = None
        self.scattering_angle_deg = None
        self.x1 = None
        self.x2 = None
        self.nm_per_channel = None
        self.ghz_per_channel = None
        self.x1_uncertainty = None
        self.x2_uncertainty = None
        self.nm_per_channel_uncertainty = None
        self.ghz_per_channel_uncertainty = None

    def set_parameters(self, laser_wavelength_nm, mirror_spacing_mm, scattering_angle_deg):
        """Sets the basic parameters for the calibration."""
        self.laser_wavelength_nm = laser_wavelength_nm
        self.mirror_spacing_mm = mirror_spacing_mm
        self.scattering_angle_deg = scattering_angle_deg

    def set_peak_positions(self, x1, x2, x1_uncertainty=None, x2_uncertainty=None):
        """Sets the channel positions for the two peaks."""
        self.x1 = x1
        self.x2 = x2
        self.x1_uncertainty = x1_uncertainty
        self.x2_uncertainty = x2_uncertainty

    def calculate(self):
        """Performs the calibration calculations for nm/channel and GHz/channel."""
        # Ensure that all inputs are set
        if None in (self.laser_wavelength_nm, self.mirror_spacing_mm, self.scattering_angle_deg, self.x1, self.x2):
            raise ValueError("All parameters must be set before calculation.")

        # Calculate deltax (absolute difference between x1 and x2)
        deltax = abs(self.x1 - self.x2)
        # Uncertainty in deltax
        if self.x1_uncertainty is not None and self.x2_uncertainty is not None:
            deltax_uncertainty = np.sqrt(self.x1_uncertainty ** 2 + self.x2_uncertainty ** 2)
        else:
            deltax_uncertainty = None

        # Calculate nm/channel
        self.nm_per_channel = (self.laser_wavelength_nm / 2) / deltax
        # Uncertainty in nm_per_channel
        if deltax_uncertainty is not None:
            self.nm_per_channel_uncertainty = self.nm_per_channel * (deltax_uncertainty / deltax)
        else:
            self.nm_per_channel_uncertainty = None

        # Calculate GHz/channel
        c = 299702547  # Speed of light in air, in m/s
        mirror_spacing_m = self.mirror_spacing_mm / 1000  # Convert mm to m
        FSR = c / (2 * mirror_spacing_m)  # Free Spectral Range in Hz
        FSR_ghz = FSR / 1e9  # Convert FSR to GHz
        self.ghz_per_channel = FSR_ghz / deltax
        # Uncertainty in ghz_per_channel
        if deltax_uncertainty is not None:
            self.ghz_per_channel_uncertainty = self.ghz_per_channel * (deltax_uncertainty / deltax)
        else:
            self.ghz_per_channel_uncertainty = None

    def get_results(self):
        """Returns the calculated nm/channel and GHz/channel, along with uncertainties."""
        if self.nm_per_channel is None or self.ghz_per_channel is None:
            raise ValueError("Calculations have not been performed yet.")
        print('nm_per_channe: ', self.nm_per_channel)
        print('nm_per_channel_uncertainty: ', self.nm_per_channel_uncertainty)
        print('ghz_per_channel: ', self.ghz_per_channel)
        print('ghz_per_channel_uncertainty: ', self.ghz_per_channel_uncertainty)
        return {
            'nm_per_channel': self.nm_per_channel,
            'nm_per_channel_uncertainty': self.nm_per_channel_uncertainty,
            'ghz_per_channel': self.ghz_per_channel,
            'ghz_per_channel_uncertainty': self.ghz_per_channel_uncertainty
        }
