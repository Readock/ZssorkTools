
# load autocomplete
from typing import TYPE_CHECKING
from functools import partial
if TYPE_CHECKING:
    from .PyKrita import *
else:
    from krita import *
            
MENU_LOCATION = "tools/scripts/zssork"
BRUSH_SIZE_MODIFIER = 0.2
BRUSH_OPACITY_MODIFIER = 0.25

class ZssorkToolsDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZssorkTools")
        label = QLabel(self)
        label.setObjectName("label")
        label.setAlignment(Qt.AlignCenter)
        label.setText("Hello World")
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        self.setLayout(layout)


def monkey_patch(view):
    # monkey patching View class
    def message_eating_monkey(*args, **kwargs):
        pass  # nom nom ...
    type(view).showFloatingMessage = message_eating_monkey


class ZssorkTools(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.dialog = ZssorkToolsDialog()

    def setup(self):
        #This runs only once when app is installed
        pass

    def createActions(self, window):
        action = window.createAction("ZssorkToolsOpenDialog", "Open ZssorkTools Dialog", MENU_LOCATION)
        action.triggered.connect(self.dialog.show)

        toggle_brush_action = window.createAction(
            "zssork_toggle_brush", "Toggle Brush", MENU_LOCATION
        )
        toggle_brush_action.triggered.connect(partial(self.toggle_brush))

        toggle_opacity_action = window.createAction(
            "zssork_toggle_opacity", "Toggle Opacity", MENU_LOCATION
        )
        toggle_opacity_action.triggered.connect(partial(self.toggle_opacity))

        toggle_pressure_action = window.createAction(
            "zssork_toggle_pressure", "Smart Toggle Pressure", MENU_LOCATION
        )
        toggle_pressure_action.triggered.connect(partial(self.toggle_pressure))

        increase_brush_size_action = window.createAction(
            "zssork_increase_size", "Increase Brush Size", MENU_LOCATION
        )
        increase_brush_size_action.triggered.connect(partial(self.increase_brush_size))

        decrease_brush_size_action = window.createAction(
            "zssork_decrease_size", "Decrease Brush Size", MENU_LOCATION
        )
        decrease_brush_size_action.triggered.connect(partial(self.decrease_brush_size))

        increase_opacity_action = window.createAction(
            "zssork_increase_opacity", "Increase Opacity", MENU_LOCATION
        )
        increase_opacity_action.triggered.connect(partial(self.increase_opacity))

        decrease_opacity_action = window.createAction(
            "zssork_decrease_opacity", "Decrease Opacity", MENU_LOCATION
        )
        decrease_opacity_action.triggered.connect(partial(self.decrease_opacity))


    def toggle_brush(self):
        # TODO implement lol
        print("")

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
        size = round(size * (1.0 + BRUSH_SIZE_MODIFIER))

        view.setBrushSize(size)
        monkey_patch(view)

    def decrease_brush_size(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        size = view.brushSize()
        size = round(size * (1.0 - BRUSH_SIZE_MODIFIER))

        view.setBrushSize(size)
        monkey_patch(view)

    def increase_opacity(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()
        opacity = min(1, opacity + BRUSH_OPACITY_MODIFIER)

        view.setPaintingOpacity(opacity)
        monkey_patch(view)

    def decrease_opacity(self):
        krita = Krita.instance()
        window = krita.activeWindow()
        view = window.activeView()

        opacity = view.paintingOpacity()
        opacity = max(BRUSH_OPACITY_MODIFIER, opacity - BRUSH_OPACITY_MODIFIER)

        view.setPaintingOpacity(opacity)
        monkey_patch(view)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(ZssorkTools(Krita.instance())) 
