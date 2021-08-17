import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QHBoxLayout, QPushButton, QVBoxLayout, QWidget
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
    self.topMainLayout = QHBoxLayout()
    self.gridLayout = QGridLayout()

    self.topMainLayout.addStretch()
    self.topMainLayout.addWidget(self.choose_dir)
    self.topMainLayout.addStretch()

    self.loadGridLayoutWidgets()

    self.mainLayout.addLayout(self.topMainLayout)
    self.mainLayout.addLayout(self.gridLayout)
    self.setLayout(self.mainLayout)

  def loadGridLayoutWidgets(self):
    with open("./directory_log.json", 'r') as read_dirs:
      all_dirs = json.load(read_dirs)
    self.grid_i = 0
    self.grid_j = 0
    for dir in all_dirs["dirs"]:
      self.gridLayout.addWidget(QPushButton(dir["dir_name"]), self.grid_i, self.grid_j)
      if self.grid_j < 2:
        self.grid_j += 1
      else:
        self.grid_j = 0
        self.grid_i += 1

  def openDir(self):
    self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")
    if self.directory:
      """
      Write json file and store the directory
      """
      # Null Json file isn't dealt with
      with open("./directory_log.json", 'r') as read_logs:
        all_logs = json.load(read_logs)

      dir_name = self.getDirName()
      dir_icon = self.getDirIcon()
      dir_dictionary = {
          "dir_name": dir_name,
          "dir_path": self.directory,
          "dir_image": dir_icon
      }

      with open("directory_log.json", 'w') as write_logs:
        if not bool(all_logs):
          all_logs = {
              "dirs": []
          }
        all_logs["dirs"].append(dir_dictionary)
        write_logs.write(json.dumps(all_logs, indent=2))

    """
    Reload the Widgets
    """
    self.loadGridLayoutWidgets()

  def getDirName(self):
    directories = self.directory.split("/")
    return directories[-1]

  def getDirIcon(self):
    image_extensions = ['.jpg', '.png']
    for img in os.listdir(self.directory):
      ext = os.path.splitext(img)[1]
      if ext.lower() not in image_extensions:
        continue
      return img


def main():
  App = QApplication(sys.argv)
  window = VideoPlayer()
  sys.exit(App.exec_())


if __name__ == '__main__':
  main()
