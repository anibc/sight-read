from kivy.uix.widget import Widget
from sightread.kv.sheetview import SheetView
from kivy.lang.builder import Builder

class RootWidget( Widget ):
    pass
Builder.load_file( "sightread/kv/rootwidget.kv" )
