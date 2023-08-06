from typing import Optional
from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets

import matplotlib as mpl
import matplotlib.transforms as transforms
from matplotlib.figure import Figure
from matplotlib.artist import Artist
try:  # starting from mpl version 3.6.0
    from matplotlib.axes import Axes
except:
    from matplotlib.axes._subplots import Axes
from matplotlib.text import Text
import matplotlib.transforms as transforms

from pylustrator.helper_functions import changeFigureSize, main_figure
from pylustrator.QLinkableWidgets import DimensionsWidget, ComboWidget


class QPosAndSize(QtWidgets.QWidget):
    element = None
    transform = None
    transform_index = 0
    scale_type = 0

    def __init__(self, layout: QtWidgets.QLayout, signals: "Signals"):
        """ a widget that holds all the properties to set and the tree view

        Args:
            layout: the layout to which to add the widget
            fig: the figure
        """
        QtWidgets.QWidget.__init__(self)

        signals.figure_changed.connect(self.setFigure)
        signals.figure_element_selected.connect(self.select_element)
        signals.figure_selection_moved.connect(self.selection_moved)
        self.signals = signals

        layout.addWidget(self)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.input_position = DimensionsWidget(self.layout, "X:", "Y:", "cm")
        self.input_position.valueChangedX.connect(lambda x: self.changePos(x, None))
        self.input_position.valueChangedY.connect(lambda y: self.changePos(None, y))

        self.input_shape = DimensionsWidget(self.layout, "W:", "H:", "cm")
        self.input_shape.valueChanged.connect(self.changeSize)

        self.input_transform = ComboWidget(self.layout, "", ["cm", "in", "px", "none"])
        self.input_transform.editingFinished.connect(self.changeTransform)

        self.input_shape_transform = ComboWidget(self.layout, "", ["scale", "bottom right", "top left"])
        self.input_shape_transform.editingFinished.connect(self.changeTransform2)

        self.layout.addStretch()

    def setFigure(self, figure):
        self.fig = figure

    def select_element(self, element):
        """ select an element """
        if element is None:
            self.setElement(self.fig)
        else:
            self.setElement(element)

    def selection_moved(self):
        self.setElement(self.element)

    def changeTransform(self):
        """ change the transform and the units of the position and size widgets """
        name = self.input_transform.text()
        self.transform_index = ["cm", "in", "px", "none"].index(name)#transform_index
        if name == "none":
            name = ""
        self.input_shape.setUnit(name)
        self.input_position.setUnit(name)
        self.setElement(self.element)

    def changeTransform2(self):#, state: int, name: str):
        """ when the dimension change type is changed from 'scale' to 'bottom right' or 'bottom left' """
        name = self.input_shape_transform.text()
        self.scale_type = ["scale", "bottom right", "top left"].index(name)
        #self.scale_type = state

    def changePos(self, value_x: float, value_y: float):
        """ change the position of an axes """
        elements = [self.element]
        elements += [element.target for element in main_figure(self.element).selection.targets]

        old_positions = []
        new_positions = []
        for element in elements:
            old_pos = element.get_position()
            try:
                old_positions.append([old_pos.x0, old_pos.y0, old_pos.width, old_pos.height])
            except AttributeError:
                old_positions.append(old_pos)
            if getattr(old_pos, "width", None) is not None:
                pos = [old_pos.x0, old_pos.y0, old_pos.width, old_pos.height]
            else:
                pos = [old_pos[0], old_pos[1]]
            if value_x is not None:
                pos[0] = value_x
            if value_y is not None:
                pos[1] = value_y
            new_positions.append(pos)

        fig = self.fig

        def redo():
            for element, pos in zip(elements, new_positions):
                element.set_position(pos)
                if isinstance(element, Text):
                    fig.change_tracker.addNewTextChange(element)
                elif isinstance(element, Axes):
                    fig.change_tracker.addNewAxesChange(element)
                elif len(pos) == 4:
                    fig.change_tracker.addChange(element, ".set_position([%f, %f, %f, %f])" % tuple(pos))
                else:
                    fig.change_tracker.addChange(element, ".set_position([%f, %f])" % tuple(pos))

        def undo():
            for element, pos in zip(elements, old_positions):
                element.set_position(pos)
                if isinstance(element, Text):
                    fig.change_tracker.addNewTextChange(element)
                elif isinstance(element, Axes):
                    fig.change_tracker.addNewAxesChange(element)
                elif len(pos) == 4:
                    fig.change_tracker.addChange(element, ".set_position([%f, %f, %f, %f])" % tuple(pos))
                else:
                    fig.change_tracker.addChange(element, ".set_position([%f, %f])" % tuple(pos))

        redo()
        self.fig.change_tracker.addEdit([undo, redo, "Change position"])

        self.fig.signals.figure_selection_property_changed.emit()
        self.fig.canvas.draw()

    def changeSize(self, value: list):
        """ change the size of an axes or figure """
        if isinstance(self.element, Figure):

            if self.scale_type == 0:
                self.fig.set_size_inches(value)
                self.fig.change_tracker.addChange(self.element, ".set_size_inches(%f/2.54, %f/2.54, forward=True)" % (
                value[0] * 2.54, value[1] * 2.54))
            else:
                if self.scale_type == 1:
                    changeFigureSize(value[0], value[1], fig=self.fig)
                elif self.scale_type == 2:
                    changeFigureSize(value[0], value[1], cut_from_top=True, cut_from_left=True, fig=self.fig)
                self.fig.change_tracker.addChange(self.element, ".set_size_inches(%f/2.54, %f/2.54, forward=True)" % (
                value[0] * 2.54, value[1] * 2.54))
                for axes in self.fig.axes:
                    pos = axes.get_position()
                    self.fig.change_tracker.addChange(axes, ".set_position([%f, %f, %f, %f])" % (
                    pos.x0, pos.y0, pos.width, pos.height))
                for text in self.fig.texts:
                    pos = text.get_position()
                    self.fig.change_tracker.addChange(text, ".set_position([%f, %f])" % (pos[0], pos[1]))

            self.fig.selection.update_selection_rectangles()
            self.fig.canvas.draw()
            self.fig.widget.updateGeometry()

            # emit a signal that the figure size has changed
            self.signals.figure_size_changed.emit()
        else:
            elements = [self.element]
            elements += [element.target for element in self.element.figure.selection.targets if
                         element.target != self.element and isinstance(element.target, Axes)]

            old_positions = []
            new_positions = []
            for element in elements:
                pos = element.get_position()
                old_positions.append(pos)
                pos = [pos.x0, pos.y0, pos.width, pos.height]
                pos[2] = value[0]
                pos[3] = value[1]
                new_positions.append(pos)

            fig = self.fig

            def redo():
                for element, pos in zip(elements, new_positions):
                    element.set_position(pos)
                    if isinstance(element, Axes):
                        fig.change_tracker.addNewAxesChange(element)
                    else:
                        fig.change_tracker.addChange(element, ".set_position([%f, %f, %f, %f])" % tuple(pos))

            def undo():
                for element, pos in zip(elements, new_positions):
                    element.set_position(pos)
                    if isinstance(element, Axes):
                        fig.change_tracker.addNewAxesChange(element)
                    else:
                        fig.change_tracker.addChange(element, ".set_position([%f, %f, %f, %f])" % tuple(pos))

            redo()
            self.fig.change_tracker.addEdit([undo, redo, "Change size"])
            self.fig.signals.figure_selection_property_changed.emit()
            self.fig.canvas.draw()


    def getTransform(self, element: Artist) -> Optional[mpl.transforms.Transform]:
        """ get the transform of an Artist """
        if isinstance(element, Figure):
            if self.transform_index == 0:
                return transforms.Affine2D().scale(2.54, 2.54)
            return None
        if isinstance(element, Axes):
            if self.transform_index == 0:
                return transforms.Affine2D().scale(2.54,
                                                   2.54) + element.figure.dpi_scale_trans.inverted() + element.figure.transFigure
            if self.transform_index == 1:
                return element.figure.dpi_scale_trans.inverted() + element.figure.transFigure
            if self.transform_index == 2:
                return element.figure.transFigure
            return None
        if self.transform_index == 0:
            return transforms.Affine2D().scale(2.54,
                                               2.54) + element.figure.dpi_scale_trans.inverted() + element.get_transform()
        if self.transform_index == 1:
            return element.figure.dpi_scale_trans.inverted() + element.get_transform()
        if self.transform_index == 2:
            return element.get_transform()
        return None

    def setElement(self, element: Artist):
        """ set the target Artist of this widget """
        #self.label.setText(str(element))
        self.element = element

        self.input_shape_transform.setDisabled(True)
        self.input_transform.setDisabled(True)

        if isinstance(element, Figure):
            pos = element.get_size_inches()
            self.input_shape.setTransform(self.getTransform(element))
            self.input_shape.setValue((pos[0], pos[1]))
            self.input_shape.setEnabled(True)
            self.input_transform.setEnabled(True)
            self.input_shape_transform.setEnabled(True)
        elif isinstance(element, Axes):
            pos = element.get_position()
            self.input_shape.setTransform(self.getTransform(element))
            self.input_shape.setValue((pos.width, pos.height))
            self.input_transform.setEnabled(True)
            self.input_shape.setEnabled(True)

        else:
            self.input_shape.setDisabled(True)

        try:
            pos = element.get_position()
            self.input_position.setTransform(self.getTransform(element))
            try:
                self.input_position.setValue(pos)
            except Exception as err:
                self.input_position.setValue((pos.x0, pos.y0))
            self.input_transform.setEnabled(True)
            self.input_position.setEnabled(True)
        except:
            self.input_position.setDisabled(True)