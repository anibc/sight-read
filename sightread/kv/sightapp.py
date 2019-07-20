from kivy.app import App
from sightread.kv.rootwidget import RootWidget

class SightApp(App):
    def build(self):
        return RootWidget()
