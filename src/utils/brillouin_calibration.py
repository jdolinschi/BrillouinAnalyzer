class BrillouinCalibration:
    def __init__(self):
        self.laser_wavelength_nm = None
        self.mirror_spacing_mm = None
        self.scattering_angle_deg = None
        self.x1 = None
        self.x2 = None
        self.nm_per_channel = None
        self.ghz_per_channel = None

    def set_parameters(self, laser_wavelength_nm, mirror_spacing_mm, scattering_angle_deg):
        """Sets the basic parameters for the calibration."""
        self.laser_wavelength_nm = laser_wavelength_nm
        self.mirror_spacing_mm = mirror_spacing_mm
        self.scattering_angle_deg = scattering_angle_deg

    def set_peak_positions(self, x1, x2):
        """Sets the channel positions for the two peaks."""
        self.x1 = x1
        self.x2 = x2

    def calculate(self):
        """Performs the calibration calculations for nm/channel and GHz/channel."""
        # Ensure that all inputs are set
        if None in (self.laser_wavelength_nm, self.mirror_spacing_mm, self.scattering_angle_deg, self.x1, self.x2):
            raise ValueError("All parameters must be set before calculation.")

        # Calculate deltax (absolute difference between x1 and x2)
        deltax = abs(self.x1 - self.x2)

        # Calculate nm/channel
        self.nm_per_channel = (self.laser_wavelength_nm / 2) / deltax

        # Calculate GHz/channel
        c = 299702547  # Speed of light in air, in m/s
        mirror_spacing_m = self.mirror_spacing_mm / 1000  # Convert mm to m
        FSR = c / (2 * mirror_spacing_m)  # Free Spectral Range in Hz
        FSR_ghz = FSR / 1e9  # Convert FSR to GHz
        self.ghz_per_channel = FSR_ghz / deltax

    def get_results(self):
        """Returns the calculated nm/channel and GHz/channel."""
        if self.nm_per_channel is None or self.ghz_per_channel is None:
            raise ValueError("Calculations have not been performed yet.")
        return {
            'nm_per_channel': self.nm_per_channel,
            'ghz_per_channel': self.ghz_per_channel
        }
