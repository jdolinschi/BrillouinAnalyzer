# fitting_plot_widget.py
import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, QObject
from pyqtgraph import ViewBox

class FittingPlotWidget(QObject):
    def __init__(self, plot_widget, ui, fit_manager):
        super().__init__()
        self.plot_widget = plot_widget
        self.ui = ui
        self.fit_manager = fit_manager

        # Initialize plot and variables
        self.x_data = None
        self.y_data = None
        self.data_curve = None  # The main data plot

        # Variables for interactions
        self.zoom_mode = False

        # Set up custom ViewBox and PlotItem
        self.view_box = FittingViewBox(self)  # Create the custom ViewBox
        self.plot_item = pg.PlotItem(viewBox=self.view_box)  # Create PlotItem with custom ViewBox
        self.plot_widget.setCentralItem(self.plot_item)  # Set the PlotItem as the central item of plot_widget

        # Connect UI buttons
        self.ui.pushButton_fitResetZoom.clicked.connect(self.reset_view)
        self.ui.pushButton_fitZoom.clicked.connect(self.zoom_button_clicked)
        # For inverted peaks checkbox
        self.ui.checkBox_fitInvertedPeaks.stateChanged.connect(self.inverted_peaks_changed)

        # Keep track of the initial view range for resetting
        self.initial_view_range = None

    def plot_data(self, x, y):
        self.x_data = x
        self.y_data = y

        # Clear the plot
        self.plot_item.clear()

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box.disable_zoom_mode()

        # Plot the new data
        self.data_curve = self.plot_item.plot(x, y, pen='w')

        # Enable auto-ranging to adjust the view to the new data
        self.plot_item.enableAutoRange()
        self.plot_item.autoRange()
        self.initial_view_range = self.plot_item.viewRange()

        # Set x-axis limits only
        self.min_x, self.max_x = np.min(x), np.max(x)
        self.view_box.setLimits(xMin=self.min_x, xMax=self.max_x)
        # Remove any y-axis limits
        self.view_box.setLimits(yMin=None, yMax=None)

        # Disable auto-range on x-axis to prevent automatic adjustments during interactions
        self.plot_item.disableAutoRange()

    def reset_view(self):
        if self.initial_view_range:
            self.plot_item.setRange(xRange=self.initial_view_range[0], yRange=self.initial_view_range[1])
            self.view_box.setLimits(
                xMin=self.min_x, xMax=self.max_x,
            )

    def zoom_button_clicked(self):
        if self.ui.pushButton_fitZoom.isChecked():
            self.view_box.enable_zoom_mode()
        else:
            self.view_box.disable_zoom_mode()

    def inverted_peaks_changed(self, state):
        # Handle changes when inverted peaks checkbox state changes
        pass  # We can implement this later

    def clear_plot(self):
        # Clear the plot and reset variables
        self.plot_item.clear()
        self.x_data = None
        self.y_data = None
        self.data_curve = None

        # Reset interaction modes
        self.ui.pushButton_fitZoom.setChecked(False)
        self.view_box.disable_zoom_mode()

        # Clear the initial view range
        self.initial_view_range = None

class FittingViewBox(ViewBox):
    def __init__(self, fitting_plot_widget):
        super().__init__(enableMenu=False)
        self.fitting_plot_widget = fitting_plot_widget
        self.zoom_mode = False
        self.zoom_start_pos = None
        self.zoom_rect = None

        self.setAcceptHoverEvents(True)
        self.enableAutoRange(False)
        self.setMouseMode(pg.ViewBox.PanMode)
        self.axis_zoom_orientation = None

    def enable_zoom_mode(self):
        self.zoom_mode = True
        self.setMouseEnabled(False, False)
        self.fitting_plot_widget.plot_widget.setCursor(Qt.CrossCursor)

    def disable_zoom_mode(self):
        self.zoom_mode = False
        self.setMouseMode(pg.ViewBox.PanMode)
        self.setMouseEnabled(True, True)
        self.fitting_plot_widget.plot_widget.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, ev):
        if self.zoom_mode and ev.button() == Qt.LeftButton:
            self.zoom_start_pos = self.mapSceneToView(ev.scenePos())
            self.saved_view_range = self.viewRange()  # Save the current view range
            x_range, y_range = self.saved_view_range
            # Freeze the current range, preventing it from changing while zooming
            self.setLimits(xMin=x_range[0], xMax=x_range[1], yMin=y_range[0], yMax=y_range[1])
            ev.accept()
        elif ev.button() == Qt.MiddleButton:
            # Start rectangle zoom with middle-click
            self.zoom_start_pos = self.mapSceneToView(ev.scenePos())
            self.zoom_rect = None
            ev.accept()
        elif ev.button() == Qt.LeftButton and (ev.modifiers() & Qt.AltModifier):
            # Start axis zoom
            self.axis_zoom_start_pos = self.mapSceneToView(ev.scenePos())
            self.axis_zoom_rect = None
            ev.accept()
        else:
            super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self.zoom_start_pos is not None:
            # Middle-click drag to zoom
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
        elif hasattr(self, 'axis_zoom_start_pos'):
            # Alt + Left-click drag to zoom axis
            current_pos = self.mapSceneToView(ev.scenePos())
            delta_x = abs(current_pos.x() - self.axis_zoom_start_pos.x())
            delta_y = abs(current_pos.y() - self.axis_zoom_start_pos.y())
            # Determine orientation dynamically
            if delta_x > delta_y:
                orientation = pg.LinearRegionItem.Vertical
            else:
                orientation = pg.LinearRegionItem.Horizontal
            if not hasattr(self, 'axis_zoom_orientation') or self.axis_zoom_orientation != orientation:
                # Remove the old item if orientation changes
                if hasattr(self, 'axis_zoom_rect') and self.axis_zoom_rect:
                    self.removeItem(self.axis_zoom_rect)
                self.axis_zoom_orientation = orientation
                if orientation == pg.LinearRegionItem.Vertical:
                    self.axis_zoom_rect = pg.LinearRegionItem(
                        values=[self.axis_zoom_start_pos.x(), current_pos.x()],
                        orientation=orientation, movable=False)
                else:
                    self.axis_zoom_rect = pg.LinearRegionItem(
                        values=[self.axis_zoom_start_pos.y(), current_pos.y()],
                        orientation=orientation, movable=False)
                self.addItem(self.axis_zoom_rect)
            else:
                if orientation == pg.LinearRegionItem.Vertical:
                    self.axis_zoom_rect.setRegion([self.axis_zoom_start_pos.x(), current_pos.x()])
                else:
                    self.axis_zoom_rect.setRegion([self.axis_zoom_start_pos.y(), current_pos.y()])
            ev.accept()
        else:
            super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if self.zoom_mode and self.zoom_start_pos:
            if self.zoom_rect:
                self.removeItem(self.zoom_rect)
                self.zoom_rect = None
            start = self.zoom_start_pos
            end = self.mapSceneToView(ev.scenePos())
            x0, x1 = sorted([start.x(), end.x()])
            y0, y1 = sorted([start.y(), end.y()])
            self.fitting_plot_widget.plot_item.setXRange(x0, x1, padding=0)
            self.fitting_plot_widget.plot_item.setYRange(y0, y1, padding=0)
            self.zoom_start_pos = None
            # Re-enable view limits
            self.setLimits(xMin=None, xMax=None, yMin=None, yMax=None)  # Remove limits after zooming
            ev.accept()
        if self.zoom_start_pos is not None:
            current_pos = self.mapSceneToView(ev.scenePos())
            x0, x1 = sorted([self.zoom_start_pos.x(), current_pos.x()])
            y0, y1 = sorted([self.zoom_start_pos.y(), current_pos.y()])
            self.fitting_plot_widget.plot_item.setXRange(x0, x1, padding=0)
            self.fitting_plot_widget.plot_item.setYRange(y0, y1, padding=0)
            if self.zoom_rect:
                self.removeItem(self.zoom_rect)
                self.zoom_rect = None
            self.zoom_start_pos = None
            ev.accept()
        if hasattr(self, 'axis_zoom_start_pos'):
            current_pos = self.mapSceneToView(ev.scenePos())
            delta_x = abs(current_pos.x() - self.axis_zoom_start_pos.x())
            delta_y = abs(current_pos.y() - self.axis_zoom_start_pos.y())
            if delta_x > delta_y:
                # Zoom x axis
                x0, x1 = sorted([self.axis_zoom_start_pos.x(), current_pos.x()])
                self.setXRange(x0, x1, padding=0)
            else:
                # Zoom y axis
                y0, y1 = sorted([self.axis_zoom_start_pos.y(), current_pos.y()])
                self.setYRange(y0, y1, padding=0)
            # Remove the axis_zoom_rect
            if self.axis_zoom_rect:
                self.removeItem(self.axis_zoom_rect)
                self.axis_zoom_rect = None
            del self.axis_zoom_start_pos
            if hasattr(self, 'axis_zoom_orientation'):
                del self.axis_zoom_orientation
            ev.accept()
        else:
            super().mouseReleaseEvent(ev)

    def wheelEvent(self, ev):
        delta = ev.delta()
        modifiers = ev.modifiers()
        if modifiers == Qt.ControlModifier:
            # Zoom Y axis only
            self._zoom_axis(ev, axis='y')
            ev.accept()
        elif modifiers == Qt.ShiftModifier:
            # Zoom X axis only
            self._zoom_axis(ev, axis='x')
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
