
# load autocomplete
from typing import TYPE_CHECKING
from functools import partial
if TYPE_CHECKING:
    from .PyKrita import *
else:
    from krita import *
            
MENU_LOCATION = "tools/scripts/zssork"

class ZssorkSettings:
    def __init__(self):
        self.settings = QSettings("Zssork", "ZssorkTools")
        self.primary_brush = self.settings.value("primary_brush", "")
        self.secondary_brush = self.settings.value("secondary_brush", "")
        self.keep_config_tool_switch = self.settings.value("keep_config_tool_switch", True, type=bool)
        self.keep_opacity_line_tool_switch = self.settings.value("keep_opacity_line_tool_switch", True, type=bool)
        self.keep_size_line_tool_switch = self.settings.value("keep_size_line_tool_switch", True, type=bool)
        self.deactivate_pressure_on_start = self.settings.value("deactivate_pressure_on_start", True, type=bool)
        self.brush_size_modifier = self.settings.value("brush_size_modifier", 0.2, type=float)
        self.brush_opacity_modifier = self.settings.value("brush_opacity_modifier", 0.25, type=float)

    def set_primary_brush(self, name):
        self.primary_brush = name
        self.settings.setValue("primary_brush", self.primary_brush)

    def set_secondary_brush(self, name):
        self.secondary_brush = name
        self.settings.setValue("secondary_brush", self.secondary_brush)

    def toggle_keep_config_tool_switch(self):
        self.keep_config_tool_switch = not self.keep_config_tool_switch
        self.settings.setValue("keep_config_tool_switch", self.keep_config_tool_switch)

    def toggle_keep_opacity_line_tool_switch(self):
        self.keep_opacity_line_tool_switch = not self.keep_opacity_line_tool_switch
        self.settings.setValue("keep_opacity_line_tool_switch", self.keep_opacity_line_tool_switch)

    def toggle_keep_size_line_tool_switch(self):
        self.keep_size_line_tool_switch = not self.keep_size_line_tool_switch
        self.settings.setValue("keep_size_line_tool_switch", self.keep_size_line_tool_switch)

    def toggle_deactivate_pressure_on_start(self):
        self.deactivate_pressure_on_start = not self.deactivate_pressure_on_start
        self.settings.setValue("deactivate_pressure_on_start", self.deactivate_pressure_on_start)

    def set_brush_size_modifier(self, value):
        self.brush_size_modifier = max(0.1, min(1.0, value))
        self.settings.setValue("brush_size_modifier", self.brush_size_modifier)

    def set_brush_opacity_modifier(self, value):
        self.brush_opacity_modifier = max(0.1, min(1.0, value))
        self.settings.setValue("brush_opacity_modifier", self.brush_opacity_modifier)

class ZssorkToolsSettingsDialog(QDialog):

    def __init__(self, settings:ZssorkSettings):
        super().__init__()
        self.setWindowTitle("ZssorkTools")
        self.setMinimumSize(700, 200)

        self.settings = settings

        label = QLabel("Zssork Tools Settings", self)
        label.setAlignment(Qt.AlignCenter)

        self.btn_set_primary = QPushButton("Set Primary (from selected)")
        self.btn_set_secondary = QPushButton("Set Secondary (from selected)")

        self.btn_set_primary.clicked.connect(self.set_primary_brush)
        self.btn_set_secondary.clicked.connect(self.set_secondary_brush)

        self.chooser = PresetChooser(self)

        self.keep_config_switch = QCheckBox("Keep same size/opacity on primary/secondary tool switches", self)
        self.keep_config_switch.setChecked(self.settings.keep_config_tool_switch)
        self.keep_config_switch.stateChanged.connect(self.settings.toggle_keep_config_tool_switch)

        self.keep_opacity_switch = QCheckBox("Keep same opacity on line tool switch", self)
        self.keep_opacity_switch.setChecked(self.settings.keep_opacity_line_tool_switch)
        self.keep_opacity_switch.stateChanged.connect(self.settings.toggle_keep_opacity_line_tool_switch)

        self.keep_size_switch = QCheckBox("Keep same size on line tool switch", self)
        self.keep_size_switch.setChecked(self.settings.keep_size_line_tool_switch)
        self.keep_size_switch.stateChanged.connect(self.settings.toggle_keep_size_line_tool_switch)

        self.deactivate_pressure_on_start = QCheckBox("Deactivate pen pressure on startup", self)
        self.deactivate_pressure_on_start.setChecked(self.settings.deactivate_pressure_on_start)
        self.deactivate_pressure_on_start.stateChanged.connect(self.settings.toggle_deactivate_pressure_on_start)

        self.brush_size_modifier_input = QDoubleSpinBox(self)
        self.brush_size_modifier_input.setRange(0.0, 1.0)
        self.brush_size_modifier_input.setSingleStep(0.05)
        self.brush_size_modifier_input.setDecimals(2)
        self.brush_size_modifier_input.setValue(self.settings.brush_size_modifier)
        self.brush_size_modifier_input.valueChanged.connect(self.settings.set_brush_size_modifier)

        self.brush_opacity_modifier_input = QDoubleSpinBox(self)
        self.brush_opacity_modifier_input.setRange(0.0, 1.0)
        self.brush_opacity_modifier_input.setSingleStep(0.05)
        self.brush_opacity_modifier_input.setDecimals(2)
        self.brush_opacity_modifier_input.setValue(self.settings.brush_opacity_modifier)
        self.brush_opacity_modifier_input.valueChanged.connect(self.settings.set_brush_opacity_modifier)

        # Restore saved
        self.update_labels()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.btn_set_primary)
        layout.addWidget(self.btn_set_secondary)
        layout.addWidget(self.chooser)
        layout.addWidget(self.keep_config_switch)
        layout.addWidget(self.keep_opacity_switch)
        layout.addWidget(self.keep_size_switch)
        layout.addWidget(self.deactivate_pressure_on_start)

        form_layout = QFormLayout()
        form_layout.addRow("Brush Size Modifier (in %):", self.brush_size_modifier_input)
        form_layout.addRow("Brush Opacity Modifier:", self.brush_opacity_modifier_input)
        layout.addLayout(form_layout)

        self.setLayout(layout)

    def update_labels(self):
        self.btn_set_primary.setText(f"Update Primary (current: {self.settings.primary_brush if self.settings.primary_brush else 'None'})")
        self.btn_set_secondary.setText(f"Update Secondary (current: {self.settings.secondary_brush if self.settings.secondary_brush else 'None'})")

    def set_primary_brush(self):
        preset = self.chooser.currentPreset()
        if preset:
            self.settings.set_primary_brush(preset.name())
            self.update_labels()

    def set_secondary_brush(self):
        preset = self.chooser.currentPreset()
        if preset:
            self.settings.set_secondary_brush(preset.name())
            self.update_labels()

def monkey_patch(view):
    # monkey patching View class
    def message_eating_monkey(*args, **kwargs):
        pass  # nom nom ...
    type(view).showFloatingMessage = message_eating_monkey


class ZssorkTools(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.menu = None
        self.settings = ZssorkSettings()
        self.dialog = ZssorkToolsSettingsDialog(self.settings)
        self.previous_tool = None
        self.is_left_mouse_button_down = False
        self.is_shift_key_down = False
        QApplication.instance().installEventFilter(self)


    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Shift and not event.isAutoRepeat():
                self.is_shift_key_down = True
                self.temporary_switch_to_line_tool()
                return False

            if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Shift and not event.isAutoRepeat():
                self.is_shift_key_down = False
                if not self.is_left_mouse_button_down:
                    self.switch_temporary_tool_back()
                return False

            if (event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton) or event.type() == QEvent.TabletPress:
                self.is_left_mouse_button_down = True
                return False

            if (event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton) or event.type() == QEvent.TabletRelease:
                self.is_left_mouse_button_down = False
                if not self.is_shift_key_down:
                    self.switch_temporary_tool_back()
                return False

        except Exception as e:
            print("ShiftLineTool error:", e)
        return False

    def is_tool_active(self, tool_name):
        toolbox = Krita.instance().activeWindow().qwindow().findChild(QDockWidget, 'ToolBox')
        brush_button = toolbox.findChild(QToolButton, tool_name)
        return brush_button.isChecked() if brush_button else False

    def temporary_switch_to_line_tool(self):
        if self.is_tool_active('KritaShape/KisToolBrush'):
            krita = Krita.instance()
            window = krita.activeWindow()
            view = window.activeView()
            opacity = view.paintingOpacity()
            self.previous_tool = "KritaShape/KisToolBrush"
            Krita.instance().action('KritaShape/KisToolLine').trigger()
            if self.settings.keep_opacity_line_tool_switch:
                view.setPaintingOpacity(opacity)


    def switch_temporary_tool_back(self):
        if self.previous_tool:
            Krita.instance().action(self.previous_tool).trigger()
            self.previous_tool = None

    def setup(self):
        #This runs only once when app is installed
        pass

    def createActions(self, window):
        action = window.createAction('Zssork', 'Zssork', 'tools/scripts/zssork')
        self.menu = QMenu('Zssork', window.qwindow())
        action.setMenu(self.menu)
        action = window.createAction("ZssorkToolsOpenDialog", "Open ZssorkTools Dialog", MENU_LOCATION)
        action.triggered.connect(self.dialog.show)

        action = window.createAction(
            "zssork_toggle_brush", "Toggle Primary/Secondary Brush", MENU_LOCATION
        )
        action.triggered.connect(partial(self.toggle_brush))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_toggle_opacity", "Toggle Opacity", MENU_LOCATION
        )
        action.triggered.connect(partial(self.toggle_opacity))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_toggle_pressure", "Smart Toggle Pressure", MENU_LOCATION
        )
        action.triggered.connect(partial(self.toggle_pressure))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_increase_size", "Increase Brush Size", MENU_LOCATION
        )
        action.triggered.connect(partial(self.increase_brush_size))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_decrease_size", "Decrease Brush Size", MENU_LOCATION
        )
        action.triggered.connect(partial(self.decrease_brush_size))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_increase_opacity", "Increase Opacity", MENU_LOCATION
        )
        action.triggered.connect(partial(self.increase_opacity))
        self.menu.addAction(action)

        action = window.createAction(
            "zssork_decrease_opacity", "Decrease Opacity", MENU_LOCATION
        )
        action.triggered.connect(partial(self.decrease_opacity))
        self.menu.addAction(action)

        QTimer.singleShot(500, self.delayed_init)

    def delayed_init(self): # hmpf
        if self.settings.deactivate_pressure_on_start:
            self.disable_pressure()
        QApplication.instance().installEventFilter(self)

    def toggle_brush(self):
        if self.is_preset_resource_active(self.settings.primary_brush):
            self.activate_preset_resource(self.settings.secondary_brush)
        else:
            self.activate_preset_resource(self.settings.primary_brush)

    def is_preset_resource_active(self, name):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()
        return name == view.currentBrushPreset().name()

    def activate_preset_resource(self, name):
        if not name:
            return
        presets = Krita.instance().resources("preset")
        resource = presets.get(name, None)
        if resource:
            krita = Krita.instance()
            window = krita.activeWindow()
            view = window.activeView()
            opacity = view.paintingOpacity()
            size = view.brushSize()
            view.setCurrentBrushPreset(resource)
            if self.settings.keep_config_tool_switch:
                view.setBrushSize(size)
            if self.settings.keep_config_tool_switch:
                view.setPaintingOpacity(opacity)

    def toggle_opacity(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()

        if not hasattr(krita, "_toggle_opacity_alt_state"):
            krita._toggle_opacity_alt_state = 0.5

        # toggle opacity between alt opacity state (e.g. 0.5) and 1
        if opacity >= 0.95:
            view.setPaintingOpacity(krita._toggle_opacity_alt_state)
        else:
            krita._toggle_opacity_alt_state = opacity
            view.setPaintingOpacity(1)
        monkey_patch(view)

    def disable_pressure(self):
        action = Krita.instance().action("disable_pressure")
        if action and action.isChecked():
            action.setChecked(False)

    def toggle_pressure(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()

        if not hasattr(krita, "_toggle_opacity_alt_state"):
            krita._toggle_opacity_alt_state = 0.5

        action = krita.action("disable_pressure")
        if not action:
            window.showNotification("Action not found: disable_pressure")
            return

        use_opacity = not action.isChecked()

        if use_opacity:
            if opacity <= 0.95:
                krita._toggle_opacity_alt_state = opacity
            view.setPaintingOpacity(1)
            action.setChecked(True)
        else:
            view.setPaintingOpacity(krita._toggle_opacity_alt_state)
            action.setChecked(False)
        monkey_patch(view)

    def increase_brush_size(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        size = view.brushSize()
        size = round(size * (1.0 + self.settings.brush_size_modifier))

        view.setBrushSize(size)
        monkey_patch(view)

    def decrease_brush_size(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        size = view.brushSize()
        size = round(size * (1.0 - self.settings.brush_size_modifier))

        view.setBrushSize(size)
        monkey_patch(view)

    def increase_opacity(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()
        opacity = min(1, opacity + self.settings.brush_opacity_modifier)

        view.setPaintingOpacity(opacity)
        monkey_patch(view)

    def decrease_opacity(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()
        opacity = max(self.settings.brush_opacity_modifier, opacity - self.settings.brush_opacity_modifier)

        view.setPaintingOpacity(opacity)
        monkey_patch(view)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(ZssorkTools(Krita.instance()))
