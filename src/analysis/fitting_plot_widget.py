# fitting_plot_widget.py
from operator import index

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, QObject
from src.analysis.fitting_viewbox_main import FittingViewBoxMain
from src.analysis.fitting_viewbox_left import FittingViewBoxLeft
from src.analysis.fitting_viewbox_right import FittingViewBoxRight


class FittingPlotWidget(QObject):
    def __init__(self, plot_widget_main, plot_widget_left, plot_widget_right, ui, fit_manager):
        super().__init__()
        self.overlap_mode = False
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

        # Initialize elastic peak fit items
        self.elastic_fit_curve = None
        self.elastic_peak_line = None

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
        self.initial_view_range_main = None

    def reset_view_main(self):
        if self.initial_view_range_main:
            self.plot_item_main.setRange(xRange=self.initial_view_range_main[0], yRange=self.initial_view_range_main[1])
            self.view_box_main.setLimits(
                xMin=self.initial_view_range_main[0][0], xMax=self.initial_view_range_main[0][1],
            )

    def zoom_button_clicked_main(self):
        if self.ui.pushButton_fitZoom.isChecked():
            self.view_box_main.enable_zoom_mode()
        else:
            self.view_box_main.disable_zoom_mode()

    def inverted_peaks_changed(self):
        # Handle changes when inverted peaks checkbox state changes
        pass  # Implement as needed

    def manual_fit_left_checkbox(self):
        # Implement manual fitting for left plot
        pass  # Implement as needed

    def manual_fit_right_checkbox(self):
        # Implement manual fitting for right plot
        pass  # Implement as needed

    def match_x_checkbox(self):
        # Handle matching X axes between plots
        pass  # Implement as needed

    def match_y_checkbox(self):
        # Handle matching Y axes between plots
        pass  # Implement as needed

    def overlap_mode_clicked(self):
        self.overlap_mode = self.ui.checkBox_fitOverlapMode.isChecked()
        # Re-plot the data accordingly
        if self.x_data is not None and self.y_data is not None:
            self.plot_data(self.x_data, self.y_data)

    def reset_view_left(self):
        # Reset left plot view
        pass  # Implement as needed

    def reset_view_right(self):
        # Reset right plot view
        pass  # Implement as needed

    def plot_data(self, x, y):
        self.x_data = x
        self.y_data = y

        # Clear the plot
        self.plot_item_main.clear()

        # Remove previous data curves if any
        if self.data_curve_main is not None:
            self.plot_item_main.removeItem(self.data_curve_main)
            self.data_curve_main = None

        if self.data_curve_left is not None:
            self.plot_item_main.removeItem(self.data_curve_left)
            self.data_curve_left = None

        if self.data_curve_right is not None:
            self.plot_item_main.removeItem(self.data_curve_right)
            self.data_curve_right = None

        # Reset elastic peak fit items
        if self.elastic_fit_curve is not None:
            self.plot_item_main.removeItem(self.elastic_fit_curve)
            self.elastic_fit_curve = None

        if self.elastic_peak_line is not None:
            self.plot_item_main.removeItem(self.elastic_peak_line)
            self.elastic_peak_line = None

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box_main.disable_zoom_mode()

        # Get the peak fit data
        filename = self.fit_manager.current_plotted_filename
        center = None
        x_fit = None
        y_fit = None
        if filename:
            project = self.fit_manager.project
            if project:
                peak_fit = project.get_dataset_peak_fit(filename, 'elastic_peak')
                if peak_fit:
                    # Get the center
                    center = peak_fit.get('center')
                    print('center: ', center)
                    # Get the fit curve
                    x_fit = peak_fit.get('x_fit')
                    y_fit = peak_fit.get('y_fit')

        # Compute y_min and y_max excluding elastic peak data
        num_channels = len(y)
        if center is not None:
            central_channel = center
        else:
            central_channel = num_channels // 2

        delta = int(0.06 * num_channels)
        start = max(0, int(central_channel - delta))
        end = min(num_channels, int(central_channel + delta))
        exclude_indices = np.r_[0:start, end:num_channels]
        y_excl = y[exclude_indices]

        # Check if y_excl is valid
        if len(y_excl) > 0:
            y_min = np.min(y_excl)
            y_max = np.max(y_excl)
        else:
            y_min = np.min(y)
            y_max = np.max(y)

        x_min = np.min(x)
        x_max = np.max(x)

        # Set initial view range
        self.initial_view_range_main = [[x_min, x_max], [y_min, y_max]]

        # Now handle plotting based on overlap mode
        if self.overlap_mode and center is not None:
            # Implement overlap mode plotting

            # Include center channel in both sides
            index_center = int(np.round(center))

            print('first index_center: ', index_center)

            # Ensure indices are within bounds
            index_center = max(0, min(num_channels - 1, index_center))

            print('second index_center: ', index_center)

            print('x[index_center]: ', x[index_center])
            print('y[index_center]: ', y[index_center])

            # Left side includes indices 0 to index_center inclusive
            x_left = x[0:index_center + 1]
            y_left = y[0:index_center + 1]

            print('x_left[-1]: ', x_left[-1])
            print('y_left[-1]: ', y_left[-1])

            # Right side includes indices index_center to end
            x_right = x[index_center:]
            y_right = y[index_center:]

            print('x_right[0]: ', x_right[0])
            print('y_right[0]: ', y_right[0])

            print('len x: ', len(x))
            print('len y: ', len(y))
            print('index_center: ', index_center)
            print("len x_left: ", len(x_left))
            print("len y_left: ", len(y_left))
            print("len x_right: ", len(x_right))
            print("len y_right: ", len(y_right))
            print('x_left[-1]: ', x_left[-1])
            print('x_right[0]: ', x_right[0])
            print('x_min: ', x_min)
            print('x_max: ', x_max)
            print('y_min: ', y_min)
            print('y_max: ', y_max)
            print('--------------------------------')

            # Adjust x-values
            x_left_adjusted = (center - x_left[::-1])  # Reverse x_left and adjust
            y_left_adjusted = y_left[::-1]

            x_right_adjusted = x_right - center

            # Plot left and right data
            self.data_curve_left = self.plot_item_main.plot(x_left_adjusted, y_left_adjusted, pen='lightgreen')

            self.data_curve_right = self.plot_item_main.plot(x_right_adjusted, y_right, pen='lightblue')

            # Combine adjusted x and y data for computing x range
            x_combined = np.concatenate((x_left_adjusted, x_right_adjusted))

            # Set x-axis range from 0 to max x
            x_min_adjusted = 0
            x_max_adjusted = np.max(x_combined)

            # Set initial view range
            self.initial_view_range_main = [[x_min_adjusted, x_max_adjusted], [y_min, y_max]]
            self.plot_item_main.setRange(xRange=[x_min_adjusted, x_max_adjusted], yRange=[y_min, y_max])

            # Adjust x_fit and plot elastic peak line at x=0
            if x_fit is not None and y_fit is not None and len(x_fit) > 0 and len(y_fit) > 0:
                x_fit_adjusted = x_fit - center
                self.elastic_fit_curve = self.plot_item_main.plot(x_fit_adjusted, y_fit, pen=pg.mkPen('grey'))

            # Plot vertical line at x=0
            self.elastic_peak_line = pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen('grey', style=Qt.DashLine))
            self.plot_item_main.addItem(self.elastic_peak_line)

            # Set x-axis limits
            self.min_x, self.max_x = x_min_adjusted, x_max_adjusted
            self.view_box_main.setLimits(xMin=self.min_x, xMax=self.max_x)
            # Remove any y-axis limits
            self.view_box_main.setLimits(yMin=None, yMax=None)

            # Disable auto-range on x-axis to prevent automatic adjustments during interactions
            self.plot_item_main.disableAutoRange()

        else:
            # Normal plotting mode

            # Plot the data
            self.data_curve_main = self.plot_item_main.plot(x, y, pen='w')

            # Now plot the elastic peak fit if available
            if x_fit is not None and y_fit is not None and len(x_fit) > 0 and len(y_fit) > 0:
                self.elastic_fit_curve = self.plot_item_main.plot(x_fit, y_fit, pen=pg.mkPen('grey'))

            # Plot the peak center as a vertical dashed line
            if center is not None and not np.isnan(center):
                self.elastic_peak_line = pg.InfiniteLine(pos=center, angle=90, pen=pg.mkPen('grey', style=Qt.DashLine))
                self.plot_item_main.addItem(self.elastic_peak_line)

            # Set initial view range (already computed)
            self.plot_item_main.setRange(xRange=[x_min, x_max], yRange=[y_min, y_max])

            # Set x-axis limits only
            self.min_x, self.max_x = x_min, x_max
            self.view_box_main.setLimits(xMin=self.min_x, xMax=self.max_x)
            # Remove any y-axis limits
            self.view_box_main.setLimits(yMin=None, yMax=None)

            # Disable auto-range on x-axis to prevent automatic adjustments during interactions
            self.plot_item_main.disableAutoRange()

    def reset_view(self):
        if self.initial_view_range_main:
            self.plot_item_main.setRange(xRange=self.initial_view_range_main[0], yRange=self.initial_view_range_main[1])
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
        pass  # Implement as needed

    def clear_plot(self):
        # Clear the plot and reset variables
        self.plot_item_main.clear()

        # Remove data curves
        if self.data_curve_main is not None:
            self.plot_item_main.removeItem(self.data_curve_main)
            self.data_curve_main = None

        if self.data_curve_left is not None:
            self.plot_item_main.removeItem(self.data_curve_left)
            self.data_curve_left = None

        if self.data_curve_right is not None:
            self.plot_item_main.removeItem(self.data_curve_right)
            self.data_curve_right = None

        # Reset elastic peak fit items
        if self.elastic_fit_curve is not None:
            self.plot_item_main.removeItem(self.elastic_fit_curve)
            self.elastic_fit_curve = None

        if self.elastic_peak_line is not None:
            self.plot_item_main.removeItem(self.elastic_peak_line)
            self.elastic_peak_line = None

        # Reset variables
        self.x_data = None
        self.y_data = None

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box_main.disable_zoom_mode()

        # Clear the initial view range
        self.initial_view_range_main = None
