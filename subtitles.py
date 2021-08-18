import os
from PyQt5.QtCore import QTimer
import pysrt
from PyQt5.QtWidgets import QWidget

class Subtitles(QWidget):
  def __init__():
    super().__init__()
  
  def playSubtitles(self, path):
    self.subs = pysrt.open(path)
    self.timer = QTimer()
    self.timer.timeout.connect(self.printSubtitles)

    