from PySide6.QtCore import Qt
from pyqtgraph import ViewBox
import pyqtgraph as pg

class FittingViewBoxRight(ViewBox):
    def __init__(self, fitting_plot_widget):
        super().__init__()
        self.fitting_plot_widget = fitting_plot_widget