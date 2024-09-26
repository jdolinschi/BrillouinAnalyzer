# calibration_plot_widget.py
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, QObject, QTimer
from pyqtgraph import ViewBox

from ..utils.voigt_profile import VoigtFitter


class CalibrationPlotWidget(QObject):
    def __init__(self, plot_widget, ui, calibration_manager):
        super().__init__()
        self.plot_widget = plot_widget
        self.ui = ui
        self.calibration_manager = calibration_manager

        # Initialize plot and variables
        self.x_data = None
        self.y_data = None
        self.data_curve = None  # The main data plot
        self.left_peak_curve = None  # The left peak fit plot
        self.right_peak_curve = None  # The right peak fit plot
        self.left_peak_line = None  # Vertical line for left peak center
        self.right_peak_line = None  # Vertical line for right peak center

        # Variables for interactions
        self.x_range = 40  # Initial fitting range
        self.fitting = False  # Whether we are in fitting mode
        self.current_peak = None  # 'left' or 'right', depending on which peak we are fitting

        # Set up custom ViewBox and PlotItem
        self.view_box = CalibrationViewBox(self)  # Create the custom ViewBox
        self.plot_item = pg.PlotItem(viewBox=self.view_box)  # Create PlotItem with custom ViewBox
        self.plot_widget.setCentralItem(self.plot_item)  # Set the PlotItem as the central item of plot_widget

        # Connect UI buttons
        self.ui.pushButton_calibResetView.clicked.connect(self.reset_view)
        self.ui.pushButton_calibZoom.clicked.connect(self.zoom_button_clicked)
        self.ui.pushButton_calibPan.clicked.connect(self.pan_button_clicked)
        self.ui.pushButton_calibFitLeftPeak.clicked.connect(self.fit_left_peak_clicked)
        self.ui.pushButton_calibFitRightPeak.clicked.connect(self.fit_right_peak_clicked)
        self.ui.pushButton_calibDeleteLeftPeak.clicked.connect(self.delete_left_peak)
        self.ui.pushButton_calibDeleteRightPeak.clicked.connect(self.delete_right_peak)

        # Keep track of the initial view range for resetting
        self.initial_view_range = None

    def delete_left_peak(self):
        if self.left_peak_curve:
            self.plot_item.removeItem(self.left_peak_curve)
            self.left_peak_curve = None
        if self.left_peak_line:
            self.plot_item.removeItem(self.left_peak_line)
            self.left_peak_line = None
        # Clear left peak data in CalibrationManager
        self.calibration_manager.delete_left_peak_fit()

    def delete_right_peak(self):
        if self.right_peak_curve:
            self.plot_item.removeItem(self.right_peak_curve)
            self.right_peak_curve = None
        if self.right_peak_line:
            self.plot_item.removeItem(self.right_peak_line)
            self.right_peak_line = None
        # Clear right peak data in CalibrationManager
        self.calibration_manager.delete_right_peak_fit()

    def plot_data(self, x, y):
        self.x_data = x
        self.y_data = y
        self.plot_item.clear()
        self.reset_fits()  # Ensure fits are reset
        self.data_curve = self.plot_item.plot(x, y, pen='w')  # Plot data in white
        self.initial_view_range = self.plot_item.viewRange()

        # Set x and y limits
        min_x, max_x = np.min(x), np.max(x)
        self.view_box.setLimits(
            xMin=min_x, xMax=max_x,
        )

    def reset_view(self):
        if self.initial_view_range:
            self.plot_item.setRange(xRange=self.initial_view_range[0], yRange=self.initial_view_range[1])

    def zoom_button_clicked(self):
        if self.ui.pushButton_calibZoom.isChecked():
            self.ui.pushButton_calibPan.setChecked(False)
            self.view_box.enable_zoom_mode()
        else:
            self.view_box.disable_zoom_mode()

    def pan_button_clicked(self):
        if self.ui.pushButton_calibPan.isChecked():
            self.ui.pushButton_calibZoom.setChecked(False)
            self.view_box.enable_pan_mode()
        else:
            self.view_box.disable_pan_mode()

    def fit_left_peak_clicked(self):
        if self.ui.pushButton_calibZoom.isChecked():
            self.ui.pushButton_calibZoom.setChecked(False)
            self.view_box.disable_zoom_mode()

        if self.ui.pushButton_calibFitLeftPeak.isChecked():
            self.ui.pushButton_calibFitRightPeak.setChecked(False)
            self.view_box.enable_fitting_mode('left')
        else:
            self.view_box.disable_fitting_mode()

    def fit_right_peak_clicked(self):
        if self.ui.pushButton_calibZoom.isChecked():
            self.ui.pushButton_calibZoom.setChecked(False)
            self.view_box.disable_zoom_mode()

        if self.ui.pushButton_calibFitRightPeak.isChecked():
            self.ui.pushButton_calibFitLeftPeak.setChecked(False)
            self.view_box.enable_fitting_mode('right')
        else:
            self.view_box.disable_fitting_mode()

    def update_fit_plot(self, x_fit, fit_curve, center, peak_type):
        if peak_type == 'left':
            if self.left_peak_curve:
                self.plot_item.removeItem(self.left_peak_curve)
            self.left_peak_curve = self.plot_item.plot(x_fit, fit_curve, pen='r')
            if self.left_peak_line:
                self.plot_item.removeItem(self.left_peak_line)
            self.left_peak_line = pg.InfiniteLine(pos=center, angle=90, pen=pg.mkPen('y', style=Qt.DashLine))
            self.plot_item.addItem(self.left_peak_line)
        elif peak_type == 'right':
            if self.right_peak_curve:
                self.plot_item.removeItem(self.right_peak_curve)
            self.right_peak_curve = self.plot_item.plot(x_fit, fit_curve, pen='g')
            if self.right_peak_line:
                self.plot_item.removeItem(self.right_peak_line)
            self.right_peak_line = pg.InfiniteLine(pos=center, angle=90, pen=pg.mkPen('b', style=Qt.DashLine))
            self.plot_item.addItem(self.right_peak_line)

    def reset_fits(self):
        # Remove previous fits
        if self.left_peak_curve:
            self.plot_item.removeItem(self.left_peak_curve)
            self.left_peak_curve = None
        if self.right_peak_curve:
            self.plot_item.removeItem(self.right_peak_curve)
            self.right_peak_curve = None
        if self.left_peak_line:
            self.plot_item.removeItem(self.left_peak_line)
            self.left_peak_line = None
        if self.right_peak_line:
            self.plot_item.removeItem(self.right_peak_line)
            self.right_peak_line = None
        # Clear fitting parameter lists
        self.ui.listWidget_calibLeftPeak.clear()
        self.ui.listWidget_calibRightPeak.clear()

    def confirm_fit(self, peak_type, fitter):
        # Save the fit parameters via CalibrationManager
        if fitter is not None:
            self.calibration_manager.save_peak_fit(peak_type, fitter)
            # Update the list widget
            if peak_type == 'left':
                self.calibration_manager.update_left_peak_list(fitter)
            elif peak_type == 'right':
                self.calibration_manager.update_right_peak_list(fitter)
        else:
            # If fitter is None, clear the parameters
            if peak_type == 'left':
                self.calibration_manager.clear_left_peak_list()
            elif peak_type == 'right':
                self.calibration_manager.clear_right_peak_list()

    def load_saved_fit(self, peak_type, peak_fit):
        x_min = peak_fit['x_min']
        x_max = peak_fit['x_max']
        x_fit = peak_fit['x_fit']
        y_fit = peak_fit['y_fit']

        # Reconstruct the fit curve
        amplitude = peak_fit['amplitude']
        center = peak_fit['center']
        sigma = peak_fit['sigma']
        gamma = peak_fit['gamma']

        # Update the plot
        self.update_fit_plot(x_fit, y_fit, center, peak_type)

class CalibrationViewBox(ViewBox):
    def __init__(self, calibration_plot_widget):
        super().__init__(enableMenu=False)
        self.saved_view_range = None
        self.calibration_plot_widget = calibration_plot_widget
        self.zoom_mode = False
        self.fitting = False
        self.fit_locked = False  # Indicates if the fit has been locked in by left-click
        self.current_peak = None
        self.x_range = calibration_plot_widget.x_range
        self.zoom_start_pos = None
        self.zoom_rect = None
        self.fit_timer = QTimer()
        self.fit_timer.timeout.connect(self.perform_fit)
        self.last_mouse_pos = None
        self.previous_mouse_pos = None
        self.wheel_event_triggered = False
        # Enable hover events to track mouse without button presses
        self.setAcceptHoverEvents(True)

    def enable_zoom_mode(self):
        self.zoom_mode = True
        self.setMouseEnabled(False, False)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.CrossCursor)
        self.enableAutoRange(False)

    def disable_zoom_mode(self):
        self.zoom_mode = False
        self.setMouseEnabled(True, True)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)
        self.enableAutoRange(True)

    def enable_pan_mode(self):
        self.setMouseMode(pg.ViewBox.PanMode)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.OpenHandCursor)

    def disable_pan_mode(self):
        self.setMouseMode(pg.ViewBox.RectMode)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)

    def enable_fitting_mode(self, peak_type):
        self.saved_view_range = self.viewRange()
        self.fitting = True
        self.enableAutoRange(False)  # Disable auto-range during fitting
        self.current_peak = peak_type
        self.setMouseEnabled(False, False)
        # Save the current view range before starting fitting
        self.calibration_plot_widget.plot_widget.setCursor(Qt.CrossCursor)
        self.setRange(xRange=self.saved_view_range[0], yRange=self.saved_view_range[1], padding=0)
        self.fit_timer.start(100)
        self.fit_locked = False

    def disable_fitting_mode(self):
        # Only save the fit if it's locked in
        if self.fit_locked and hasattr(self, 'fitter'):
            self.calibration_plot_widget.confirm_fit(self.current_peak, self.fitter)
        else:
            # Clear any previous fit
            if self.current_peak == 'left':
                self.calibration_plot_widget.delete_left_peak()
            elif self.current_peak == 'right':
                self.calibration_plot_widget.delete_right_peak()
            # Clear parameters
            self.calibration_plot_widget.confirm_fit(self.current_peak, None)

        self.fitting = False
        self.fit_locked = False
        self.current_peak = None
        self.setMouseEnabled(True, True)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)
        self.fit_timer.stop()
        self.enableAutoRange(True)  # Re-enable auto-range after fitting

    def mousePressEvent(self, ev):
        if self.zoom_mode and ev.button() == Qt.LeftButton:
            self.zoom_start_pos = self.mapSceneToView(ev.scenePos())
            self.saved_view_range = self.viewRange()  # Save the current view range
            x_range, y_range = self.saved_view_range
            # Freeze the current range, preventing it from changing while zooming
            self.setLimits(xMin=x_range[0], xMax=x_range[1], yMin=y_range[0], yMax=y_range[1])
            ev.accept()
        elif self.fitting:
            if ev.button() == Qt.LeftButton:
                if not self.fit_locked:
                    # Lock in the fit
                    self.fit_locked = True
                    self.calibration_plot_widget.confirm_fit(self.current_peak, self.fitter)
                ev.accept()
            elif ev.button() == Qt.RightButton:
                if self.fit_locked:
                    # Reset the fit
                    self.fit_locked = False
                    # Remove previous fit plot and center line
                    if self.current_peak == 'left':
                        self.calibration_plot_widget.delete_left_peak()
                    elif self.current_peak == 'right':
                        self.calibration_plot_widget.delete_right_peak()
                    # Clear parameters
                    self.calibration_plot_widget.confirm_fit(self.current_peak, None)
                    # Continue fitting with mouse movement
                    self.last_mouse_pos = None
                ev.accept()
        else:
            super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self.zoom_mode and self.zoom_start_pos:
            current_pos = self.mapSceneToView(ev.scenePos())
            pos = [min(self.zoom_start_pos.x(), current_pos.x()), min(self.zoom_start_pos.y(), current_pos.y())]
            size = [abs(current_pos.x() - self.zoom_start_pos.x()), abs(current_pos.y() - self.zoom_start_pos.y())]

            if not self.zoom_rect:
                # Using pg.RectROI for better integration
                self.zoom_rect = pg.RectROI(pos, size, pen=pg.mkPen('r', width=1, style=Qt.DashLine))
                self.addItem(self.zoom_rect)
            else:
                self.zoom_rect.setPos(pos)
                self.zoom_rect.setSize(size)
            ev.accept()
        else:
            super().mouseMoveEvent(ev)

    def hoverMoveEvent(self, ev):
        if self.fitting and not self.fit_locked:
            self.last_mouse_pos = ev.pos()
            ev.accept()
        else:
            super().hoverMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if self.zoom_mode and self.zoom_start_pos:
            if self.zoom_rect:
                self.removeItem(self.zoom_rect)
                self.zoom_rect = None
            start = self.zoom_start_pos
            end = self.mapSceneToView(ev.scenePos())
            x0, x1 = sorted([start.x(), end.x()])
            y0, y1 = sorted([start.y(), end.y()])
            self.calibration_plot_widget.plot_item.setXRange(x0, x1, padding=0)
            self.calibration_plot_widget.plot_item.setYRange(y0, y1, padding=0)
            self.zoom_start_pos = None
            # Re-enable view limits
            self.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)  # Remove limits after zooming
            ev.accept()
        else:
            super().mouseReleaseEvent(ev)

    def wheelEvent(self, ev):
        delta = ev.delta()
        modifiers = ev.modifiers()
        if self.fitting and not self.fit_locked:
            factor = 1.02 ** (delta / 120)
            self.x_range *= factor
            # Clamp x_range within reasonable bounds
            self.x_range = max(1, min(self.x_range, self.viewRange()[0][1] - self.viewRange()[0][0]))
            # Set the flag to trigger the fit
            self.wheel_event_triggered = True
            self.perform_fit()
            ev.accept()
        elif modifiers == Qt.ControlModifier:
            # Zoom Y axis only
            self._zoom_axis(ev, axis='y')
            ev.accept()
        elif modifiers == Qt.ShiftModifier:
            # Zoom X axis only
            self._zoom_axis(ev, axis='x')
            ev.accept()
        elif modifiers == Qt.AltModifier:
            # Zoom both axes equally
            self._zoom_axis(ev, axis='xy')
            ev.accept()
        else:
            super().wheelEvent(ev)

    def perform_fit(self):
        if self.fit_locked:
            return  # Do not update fit if it's locked

        if self.last_mouse_pos and (self.previous_mouse_pos != self.last_mouse_pos or self.wheel_event_triggered):
            self.previous_mouse_pos = self.last_mouse_pos
            self.wheel_event_triggered = False  # Reset the flag after the fit
            mouse_point = self.mapToView(self.last_mouse_pos)
            x_center = mouse_point.x()
            x_range = self.x_range
            x_min = x_center - x_range / 2
            x_max = x_center + x_range / 2
            x_data = self.calibration_plot_widget.x_data
            y_data = self.calibration_plot_widget.y_data
            mask = (x_data >= x_min) & (x_data <= x_max)
            x_fit = x_data[mask]
            y_fit = y_data[mask]
            if len(x_fit) > 5:
                # Perform Voigt fit
                fitter = VoigtFitter(inverted=True, method='pseudo_voigt')
                try:
                    fitter.fit(x_fit, y_fit, increase_fit_time_on_failure=True)
                    fitter.x_min = x_min
                    fitter.x_max = x_max
                    fitter.x_fit = x_fit
                    fitter.y_fit = fitter.get_fit_curve(x_fit)
                    fit_curve = fitter.get_fit_curve(x_fit)
                    center = fitter.get_parameter('center')
                    if np.min(x_data) < center < np.max(x_data):
                        self.calibration_plot_widget.update_fit_plot(x_fit, fit_curve, center, self.current_peak)
                        # Store the fitter for confirmation
                        self.fitter = fitter
                    else:
                        self.calibration_plot_widget.update_fit_plot(x_fit, fit_curve, None, self.current_peak)
                except Exception as e:
                    print(f"Fitting failed: {e}")  # Optional: Log the error

    def _zoom_axis(self, ev, axis):
        zoom_factor_x = 1.07 ** (ev.delta() / 120)  # Increased zoom rate for x-axis
        zoom_factor_y = 1.07 ** (ev.delta() / 120)
        zoom_factor_xy = 1.02 ** (ev.delta() / 120)  # Existing zoom rate for xy-axis
        mouse_point = self.mapToView(ev.pos())
        if axis == 'x':
            self.scaleBy((1 / zoom_factor_x, 1), center=mouse_point)
        elif axis == 'y':
            self.scaleBy((1, 1 / zoom_factor_y), center=mouse_point)
        elif axis == 'xy':
            self.scaleBy((1 / zoom_factor_xy, 1 / zoom_factor_xy), center=mouse_point)
