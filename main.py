import kivy
from kivy.app import App
from kivy.uix.label import Label

kivy.require('2.0.0')

class VideoPlayer(App):
  def build(self):
    return Label(text="Hello there!")


VideoPlayer().run()