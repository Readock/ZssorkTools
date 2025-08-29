
# load autocomplete
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .PyKrita import *
else:
    from krita import *
            

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

class ZssorkTools(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.dialog = ZssorkToolsDialog()

    def setup(self):
        #This runs only once when app is installed
        pass

    def createActions(self, window):
        action = window.createAction("ZssorkToolsOpenDialog", "Open ZssorkTools Dialog", "tools/scripts")
        action.triggered.connect(self.dialog.show)


# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(ZssorkTools(Krita.instance())) 
