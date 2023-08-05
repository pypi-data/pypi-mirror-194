from typing import Dict, Optional

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from numpy.typing import ArrayLike

from primawera.canvasbase import CanvasBase
from primawera.filters import linear_stretch, gamma_correction, \
    linear_contrast, logarithm_stretch
from primawera.lut import apply_lut
from primawera.visualiser import Visualiser


class Canvas3D(CanvasBase):
    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None, *args,
                 **kwargs) -> None:
        super().__init__(data, mode, desktop_height, desktop_width,
                         filters, filters_options, *args, **kwargs)
        self._init_interface()
        self._create_actions()
        self._set_actions_checkable()
        self._connect_actions()

        # TODO: move this higher, so that we do not have to process image
        #       twice during this constructor.
        if self.mode != 'F':
            self._no_filter()
        else:
            self._linear_stretch()
        self.get_actions()[0].setChecked(True)

    def _init_interface(self):
        super()._init_interface()
        # Processing
        processed_data = self._process_data()

        # Visualise
        maximum_width = int(self.desktop_width * 0.80)
        maximum_height = int(self.desktop_height * 0.80)
        self.view_layout = QGridLayout()
        self.vis_main_window = Visualiser(processed_data.copy(), (0, 1, 2),
                                          self.mode, maximum_height,
                                          maximum_width, True)
        self.vis_row_time = Visualiser(processed_data, (1, 0, 2),
                                       self.mode, maximum_height,
                                       maximum_width, False)
        self.vis_col_time = Visualiser(processed_data, (2, 1, 0),
                                       self.mode, maximum_height,
                                       maximum_width, False)
        self.view_layout.addWidget(self.vis_main_window, 0, 0, Qt.AlignTop)
        self.view_layout.addWidget(self.vis_row_time, 1, 0, Qt.AlignTop)
        self.view_layout.addWidget(self.vis_col_time, 0, 1, Qt.AlignTop)

        self.main_layout.addLayout(self.view_layout, 1)

        # TODO: consider if it is useful any longer
        # Set up scaling factors, so that all extra space is filled using
        # spacers.
        self.view_layout.setColumnStretch(2, 1)
        self.view_layout.setRowStretch(2, 1)

        self.setLayout(self.main_layout)

        # These are just to simplify some member functions
        self.visualisers = [self.vis_main_window, self.vis_row_time,
                            self.vis_col_time]
        self.axes_orientations = [(0, 1, 2), (1, 0, 2), (2, 1, 0)]

        self._connect_visualisers_signals()
        self._hide_scroll_bars()

    def _connect_visualisers_signals(self):
        # Here we synchronize the QScrollAreas using signals.
        self.vis_main_window.value_change_emitter_vertical.connect(
            self.vis_col_time.get_vertical_bar().setValue)
        self.vis_main_window.value_change_emitter_horizontal.connect(
            self.vis_row_time.get_horizontal_bar().setValue)

        self.vis_col_time.value_change_emitter_vertical.connect(
            self.vis_main_window.get_vertical_bar().setValue)
        self.vis_row_time.value_change_emitter_horizontal.connect(
            self.vis_main_window.get_horizontal_bar().setValue)

    def _connect_info_window_and_canvas(self):
        self.vis_main_window.signal_position.connect(
            self.changed_coordinates_signal)
        self.vis_col_time.signal_position.connect(
            self.changed_coordinates_signal)
        self.vis_row_time.signal_position.connect(
            self.changed_coordinates_signal)

    def _hide_scroll_bars(self):
        # Hide unused bars
        row_time = self.vis_row_time.get_scroll_area()
        row_time.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        row_time.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        col_time = self.vis_col_time.get_scroll_area()
        col_time.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        col_time.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _redraw(self, new_data):
        for vis, axes_orientation in zip(self.visualisers,
                                         self.axes_orientations):
            vis.update_data(new_data, axes_orientation,
                            self.mode_visualisation)
            vis.redraw()

    def get_filters(self):
        if self.mode == "F":
            return [self.linear_stretch_action, self.logarithm_stretch_action]

        result = [self.no_filter_action]
        if self.mode == "1":
            return result

        if self.mode == "grayscale":
            result.append(self.linear_stretch_action)
        result.extend([self.linear_contrast_action,
                       self.gamma_correction_action])
        return result

    def get_luts(self):
        if self.mode == "F" or self.mode == "grayscale":
            return [action for _, action in self.lut_actions]
        return []

    def get_actions(self):
        return self.get_filters() + self.get_luts()

    def get_menus(self):
        base_menu = super().get_menus()
        filters_menu = ("Filters", self.get_filters())
        luts_menu = ("LUT", self.get_luts())
        result = [filters_menu, luts_menu] if luts_menu[1] else [filters_menu]
        return result + base_menu

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_N:
            for vis in [vis for vis in self.visualisers if vis.has_focus()]:
                vis.next_frame()
        elif event.key() == QtCore.Qt.Key_P:
            for vis in [vis for vis in self.visualisers if vis.has_focus()]:
                vis.previous_frame()
        else:
            super().keyPressEvent(event)

    def _process_data(self):
        super()._process_data()
        processed_data = self.data.astype(float)

        # Apply filters
        if self.filters.get("linear_stretch", False):
            processed_data = 255.0 * linear_stretch(processed_data)
        elif self.filters.get("gamma_correction", False):
            gamma_factor = self.filters_options.get("factor", 0.5)
            processed_data = gamma_correction(processed_data, gamma_factor)
        elif self.filters.get("linear_contrast", False):
            stretch_factor = self.filters_options.get("factor", 2)
            processed_data = linear_contrast(processed_data, stretch_factor)
        elif self.filters.get("logarithm_stretch", False):
            processed_data = logarithm_stretch(processed_data)
            processed_data = 255.0 * linear_stretch(processed_data)

        processed_data = np.clip(processed_data, 0, 255.0).astype(np.uint8)

        # Apply LUT
        if self.lut is not None:
            self.mode_visualisation = "rgb"
            processed_data = apply_lut(processed_data, self.lut)
        self.menus_changed_signal.emit()
        return processed_data

    def _increase_zoom_level(self):
        for vis in self.visualisers:
            vis.increase_zoom_level()

    def _decrease_zoom_level(self):
        for vis in self.visualisers:
            vis.decrease_zoom_level()
