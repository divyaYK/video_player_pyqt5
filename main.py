import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QProgressBar, QPushButton, QVBoxLayout, QWidget
class VideoPlayer(QWidget):
  def __init__(self) -> None:
    super().__init__()
    self.setWindowTitle("Video Player")
    self.setGeometry(50, 50, 1080, 900)
    self.UI()
    self.show()

  def UI(self):
    self.widgets()
    self.layouts()


  def widgets(self):
    self.choose_dir = QPushButton("Choose Directory")
    self.choose_dir.clicked.connect(self.openDir)

  def layouts(self):
    self.mainLayout = QVBoxLayout()
    self.topMainLayout = QVBoxLayout()
    self.gridLayout = QGridLayout()

    self.topMainLayout.addStretch()
    self.topMainLayout.addWidget(self.choose_dir)
    self.topMainLayout.addStretch()

    self.mainLayout.addLayout(self.topMainLayout)
    self.mainLayout.addLayout(self.gridLayout)
    self.setLayout(self.mainLayout)

  def openDir(self):
    directory = QFileDialog.getExistingDirectory(self, "Select Directory")
    print(directory)


def main():
  App = QApplication(sys.argv)
  window = VideoPlayer()
  sys.exit(App.exec_())


if __name__ == '__main__':
  main()