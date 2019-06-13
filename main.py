from kivy.app import App
from kivy.uix.widget import Widget

from sheetview import SheetView

class SightRootWidget( Widget ):
    pass

class SightApp(App):

    def build(self):
        return SightRootWidget()


if __name__ == '__main__':
    SightApp().run()
