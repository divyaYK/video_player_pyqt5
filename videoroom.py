from PyQt5.QtWidgets import QWidget

class VideoRoom(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Video Room")
    self.setGeometry(50, 50, 1080, 900)
    self.UI()

  def UI(self):
    pass
