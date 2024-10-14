# fitting_plot_widget.py
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, QObject
from src.analysis.fitting_viewbox_main import FittingViewBoxMain
from src.analysis.fitting_viewbox_left import FittingViewBoxLeft
from src.analysis.fitting_viewbox_right import FittingViewBoxRight


class FittingPlotWidget(QObject):
    def __init__(self, plot_widget_main, plot_widget_left, plot_widget_right, ui, fit_manager):
        super().__init__()
        self.plot_widget_main = plot_widget_main
        self.plot_widget_left = plot_widget_left
        self.plot_widget_right = plot_widget_right
        self.ui = ui
        self.fit_manager = fit_manager

        # Initialize plot and variables
        self.x_data = None
        self.y_data = None
        self.data_curve_main = None  # The main data plot
        self.data_curve_left = None
        self.data_curve_right = None

        # Variables for interactions
        self.zoom_mode = False
        self.left_plot_fitting = False
        self.right_plot_fitting = False
        self.left_x_range = 40
        self.right_x_range = 40

        # Set up custom ViewBox and PlotItem
        self.view_box_main = FittingViewBoxMain(self)  # Create the custom ViewBox
        self.plot_item_main = pg.PlotItem(viewBox=self.view_box_main)  # Create PlotItem with custom ViewBox
        self.plot_widget_main.setCentralItem(self.plot_item_main)  # Set the PlotItem as the central item of plot_widget

        self.view_box_left = FittingViewBoxLeft(self)
        self.plot_item_left = pg.PlotItem(viewBox=self.view_box_left)
        self.plot_widget_left.setCentralItem(self.plot_item_left)

        self.view_box_right = FittingViewBoxRight(self)
        self.plot_item_right = pg.PlotItem(viewBox=self.view_box_right)
        self.plot_widget_right.setCentralItem(self.plot_item_right)

        # Connect UI buttons, Main
        self.ui.pushButton_fitResetZoom.clicked.connect(self.reset_view_main)
        self.ui.pushButton_fitZoom.clicked.connect(self.zoom_button_clicked_main)
        self.ui.checkBox_fitInvertedPeaks.stateChanged.connect(self.inverted_peaks_changed)
        self.ui.checkBox_fitOverlapMode.clicked.connect(self.overlap_mode_clicked)

        # Connect UI buttons, Left
        self.ui.pushButton_fitLeftZoomReset.clicked.connect(self.reset_view_left)
        self.ui.checkBox_fitLeftManualFit.clicked.connect(self.manual_fit_left_checkbox)

        # Connect UI buttons, Right
        self.ui.pushButton_fitRightZoomReset.clicked.connect(self.reset_view_right)
        self.ui.checkBox_fitRightManualFit.clicked.connect(self.manual_fit_right_checkbox)

        # Connect UI buttons, fitting settings
        self.ui.checkBox_fitMatchX.clicked.connect(self.match_x_checkbox)
        self.ui.checkBox_fitMatchY.clicked.connect(self.match_y_checkbox)

        # Keep track of the initial view range for resetting
        self.initial_view_range = None

    def reset_view_main(self):
        print('reset_view_main')

    def zoom_button_clicked_main(self):
        print('zoom_button_clicked_main')

    def inverted_peaks_changed(self):
        print('inverted_peaks_changed')

    def manual_fit_left_checkbox(self):
        print('manual_fit_left_checkbox')

    def manual_fit_right_checkbox(self):
        print('manual_fit_right_checkbox')

    def match_x_checkbox(self):
        print('match_x_checkbox')

    def match_y_checkbox(self):
        print('match_y_checkbox')

    def overlap_mode_clicked(self):
        print('overlap_mode_clicked')

    def reset_view_left(self):
        print('reset_view_left')

    def reset_view_right(self):
        print('reset_view_right')

    def plot_data(self, x, y):
        self.x_data = x
        self.y_data = y

        # Clear the plot
        self.plot_item_main.clear()
        self.plot_item_left.clear()
        self.plot_item_right.clear()

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box_main.disable_zoom_mode()

        # Plot the new data
        self.data_curve_main = self.plot_item_main.plot(x, y, pen='w')
        self.data_curve_right = self.plot_item_right.plot(pen='w')
        self.data_curve_left = self.plot_item_left.plot(pen='w')

        # Enable auto-ranging to adjust the view to the new data
        self.plot_item_main.enableAutoRange()
        self.plot_item_main.autoRange()
        self.initial_view_range = self.plot_item_main.viewRange()

        # Set x-axis limits only
        self.min_x, self.max_x = np.min(x), np.max(x)
        self.view_box_main.setLimits(xMin=self.min_x, xMax=self.max_x)
        # Remove any y-axis limits
        self.view_box_main.setLimits(yMin=None, yMax=None)

        # Disable auto-range on x-axis to prevent automatic adjustments during interactions
        self.plot_item_main.disableAutoRange()

    def reset_view(self):
        if self.initial_view_range:
            self.plot_item_main.setRange(xRange=self.initial_view_range[0], yRange=self.initial_view_range[1])
            self.view_box_main.setLimits(
                xMin=self.min_x, xMax=self.max_x,
            )

    def zoom_button_clicked(self):
        if self.ui.pushButton_fitZoom.isChecked():
            self.view_box_main.enable_zoom_mode()
        else:
            self.view_box_main.disable_zoom_mode()

    def inverted_peaks_changed(self, state):
        # Handle changes when inverted peaks checkbox state changes
        pass  # We can implement this later

    def clear_plot(self):
        # Clear the plot and reset variables
        self.plot_item_main.clear()
        self.x_data = None
        self.y_data = None
        self.data_curve_main = None

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box_main.disable_zoom_mode()

        # Clear the initial view range
        self.initial_view_range = None
