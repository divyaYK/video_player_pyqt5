import os
import json
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QSlider, QStyle, QToolBox, QVBoxLayout, QWidget


os.environ["QT_GSTREAMER_PLAYBIN_FLAGS"] = str(0x00000017)
class VideoRoom(QWidget):
  def __init__(self):
    super().__init__()
    self.setGeometry(50, 50, 1080, 900)

  def UI(self):
    dir_name = self.windowTitle()
    with open("./directory_log.json", 'r') as read_logs:
      all_dirs = json.load(read_logs)

    self.all_dir_paths = list()
    self.all_dir_names = list()
    self.dir_found = False

    for dir in all_dirs["dirs"]:
      if dir_name in dir["dir_name"]:
        self.dir_found = True
        dir_path = dir["dir_path"]
        for dirpaths, dirnames, filenames in os.walk(dir_path):
          if dir_path != dirpaths:
            self.all_dir_paths.append(dirpaths)
          if dir_name != dirnames:
            self.all_dir_names.extend(dirnames)
        break

    if self.dir_found is False:
      return QLabel("Directory doesn't exist")

    self.widgets()
    self.layouts()

  def widgets(self):
    self.videoWidget = QVideoWidget()
    self.playButton = QPushButton()
    self.playButton.setEnabled(False)
    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    self.playButton.clicked.connect(self.playVideo)

    self.positionSlider = QSlider(Qt.Horizontal)
    self.positionSlider.setRange(0, 0)
    self.positionSlider.sliderMoved.connect(self.setVideoPosition)

  def layouts(self):
    self.roomLayout = QHBoxLayout()
    self.videoOnlyLayout = QVBoxLayout()
    self.videoListLayout = QVBoxLayout()
    self.videoWithNotesLayout = QVBoxLayout()
    self.notesLayout = QHBoxLayout()
    self.videoControlLayout = QHBoxLayout()

    self.videoOnlyLayout.addWidget(self.videoWidget)
    self.videoControlLayout.addWidget(self.playButton)
    self.videoControlLayout.addWidget(self.positionSlider)

    self.setVideoListLayout()

    self.videoOnlyLayout.addLayout(self.videoControlLayout)
    self.videoWithNotesLayout.addLayout(self.videoOnlyLayout)
    self.videoWithNotesLayout.addLayout(self.notesLayout)
    self.roomLayout.addLayout(self.videoWithNotesLayout)
    self.roomLayout.addLayout(self.videoListLayout)

    self.setLayout(self.roomLayout)

    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    self.mediaPlayer.setVideoOutput(self.videoWidget)
    self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
    self.mediaPlayer.positionChanged.connect(self.positionChanged)
    self.mediaPlayer.durationChanged.connect(self.durationChanged)

  def setVideoListLayout(self):
    self.toolbox = QToolBox()
    for path in self.all_dir_paths:
      subtitle_list = []
      valid_videos = ['.mp4', '.3gp', '.avi', '.webm']
      valid_subtitles = ['.scc', '.srt', '.3gpp']
      dir_content_list = QListWidget()
      for file in os.listdir(path):
        filename, extension = os.path.splitext(file)
        if extension.lower() in valid_subtitles:
          subtitle_list.append(file)
      for file in os.listdir(path):
        filename, extension = os.path.splitext(file)
        if extension.lower() in valid_videos:
          video_data = [str(path) + '/' + file]
          for subtitle_file in subtitle_list:
            if filename in subtitle_file:
              video_data.append(str(path) + '/' + subtitle_file)

          video_file = QListWidgetItem(filename)
          video_file.setData(Qt.UserRole, video_data)
          dir_content_list.addItem(video_file)

      dir_content_list.itemClicked.connect(self.videoSelected)
      index = self.all_dir_paths.index(path)
      self.toolbox.addItem(dir_content_list, self.all_dir_names[index])
    self.videoListLayout.addWidget(self.toolbox)

  def videoSelected(self, video_file):
    video_data = video_file.data(Qt.UserRole)
    if video_data[0] != "":
      self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile((video_data[0]))))
      self.playButton.setEnabled(True)
      self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

  def playVideo(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.pause()
    else:
      self.mediaPlayer.play()

  def setVideoPosition(self, position):
    self.mediaPlayer.setPosition(position)

  def mediaStateChanged(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
    else:
      self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
  
  def durationChanged(self, duration):
    self.positionSlider.setRange(0, duration)
  
  def positionChanged(self, position):
    self.positionSlider.setValue(position)