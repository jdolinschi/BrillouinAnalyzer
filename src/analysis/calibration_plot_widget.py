# src/analysis/calibration_plot_widget.py
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QCursor
from pyqtgraph import ViewBox
from ..utils.voigt_profile import VoigtFitter
from PySide6.QtWidgets import QGraphicsRectItem


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

        # Keep track of the initial view range for resetting
        self.initial_view_range = None


    def plot_data(self, x, y):
        self.x_data = x
        self.y_data = y
        self.plot_item.clear()
        self.data_curve = self.plot_item.plot(x, y, pen='w')  # Plot data in white
        self.initial_view_range = self.plot_item.viewRange()
        self.reset_fits()

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
        if self.ui.pushButton_calibFitLeftPeak.isChecked():
            self.ui.pushButton_calibFitRightPeak.setChecked(False)
            self.view_box.enable_fitting_mode('left')
        else:
            self.view_box.disable_fitting_mode()

    def fit_right_peak_clicked(self):
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

    def confirm_fit(self, peak_type, fitter):
        # Save the fit parameters via CalibrationManager
        self.calibration_manager.save_peak_fit(peak_type, fitter)
        # Update the list widget
        if peak_type == 'left':
            self.calibration_manager.update_left_peak_list(fitter)
        elif peak_type == 'right':
            self.calibration_manager.update_right_peak_list(fitter)
        # Keep the fit curve and center line
        # Disable fitting mode
        self.view_box.disable_fitting_mode()

class CalibrationViewBox(ViewBox):
    def __init__(self, calibration_plot_widget):
        super().__init__(enableMenu=False)
        self.calibration_plot_widget = calibration_plot_widget
        self.zoom_mode = False
        self.fitting = False
        self.current_peak = None
        self.x_range = calibration_plot_widget.x_range
        self.zoom_start_pos = None
        self.zoom_rect = None

    def enable_zoom_mode(self):
        self.zoom_mode = True
        self.setMouseEnabled(False, False)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.CrossCursor)

    def disable_zoom_mode(self):
        self.zoom_mode = False
        self.setMouseEnabled(True, True)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)

    def enable_pan_mode(self):
        self.setMouseEnabled(True, True)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.OpenHandCursor)

    def disable_pan_mode(self):
        self.setMouseEnabled(False, False)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)

    def enable_fitting_mode(self, peak_type):
        self.fitting = True
        self.current_peak = peak_type
        self.setMouseEnabled(False, False)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.CrossCursor)

    def disable_fitting_mode(self):
        self.fitting = False
        self.current_peak = None
        self.setMouseEnabled(True, True)
        self.calibration_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, ev):
        if self.zoom_mode and ev.button() == Qt.LeftButton:
            self.zoom_start_pos = ev.pos()
            ev.accept()
        elif self.fitting and ev.button() == Qt.LeftButton:
            # Confirm fit
            self.calibration_plot_widget.confirm_fit(self.current_peak, self.fitter)
            ev.accept()
        else:
            super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self.zoom_mode and self.zoom_start_pos:
            rect = pg.QtCore.QRectF(self.zoom_start_pos, ev.pos()).normalized()
            if not self.zoom_rect:
                self.zoom_rect = QGraphicsRectItem(rect)
                self.zoom_rect.setPen(pg.mkPen('r', width=1, style=Qt.DashLine))
                self.scene().addItem(self.zoom_rect)
            else:
                self.zoom_rect.setRect(rect)
            ev.accept()
        elif self.fitting:
            mouse_point = self.mapToView(ev.pos())
            x_center = mouse_point.x()
            x_range = self.x_range
            x_min = x_center - x_range / 2
            x_max = x_center + x_range / 2
            print('x_max: ', x_max)
            print('x_min: ', x_min)
            x_data = self.calibration_plot_widget.x_data
            y_data = self.calibration_plot_widget.y_data
            mask = (x_data >= x_min) & (x_data <= x_max)
            x_fit = x_data[mask]
            y_fit = y_data[mask]
            if len(x_fit) > 5:
                # Perform Voigt fit
                fitter = VoigtFitter(inverted=True)
                try:
                    fitter.fit(x_fit, y_fit)
                    fit_curve = fitter.get_fit_curve(x_fit)
                    center = fitter.get_parameter('center')
                    # if the center is less than the minimum of the x_data or greater than the maximum of the x_data, don't plot it
                    if np.min(x_data) <= center <= np.max(x_data):
                        self.calibration_plot_widget.update_fit_plot(x_fit, fit_curve, center, self.current_peak)
                    else:
                        # Update only the fit curve without the vertical line
                        self.calibration_plot_widget.update_fit_plot(x_fit, fit_curve, None, self.current_peak)
                    print('self.current_peak: ', self.current_peak)
                    print('center: ', center)
                    # Store the fitter for confirmation
                    self.fitter = fitter
                except Exception:
                    pass  # Fit failed
            ev.accept()
        else:
            super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if self.zoom_mode and self.zoom_start_pos:
            self.scene().removeItem(self.zoom_rect)
            self.zoom_rect = None
            start = self.mapToView(self.zoom_start_pos)
            end = self.mapToView(ev.pos())
            x0, x1 = sorted([start.x(), end.x()])
            y0, y1 = sorted([start.y(), end.y()])
            self.calibration_plot_widget.plot_item.setXRange(x0, x1, padding=0)
            self.calibration_plot_widget.plot_item.setYRange(y0, y1, padding=0)
            self.zoom_start_pos = None
            ev.accept()
        else:
            super().mouseReleaseEvent(ev)

    def wheelEvent(self, ev):
        modifiers = ev.modifiers()
        if self.fitting:
            # Adjust fitting range
            delta = ev.delta()
            factor = 1.02 ** (delta / 120)
            self.x_range *= factor
            if self.x_range < 1:
                self.x_range = 1
            elif self.x_range > (self.viewRange()[0][1] - self.viewRange()[0][0]):
                self.x_range = self.viewRange()[0][1] - self.viewRange()[0][0]
            print('self.x_range: ', self.x_range)
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

