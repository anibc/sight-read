from kivy.app import App
from kivy.core.window import Window
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import *

import random as rand
from note import Note
import mido
inputname = next(( s for s in mido.get_input_names() if s[ -1 ] == '0' and s[ :3 ] == 'V61' ))
# inputname = 'V61:V61 MIDI 1 28:0'

class SightWidget( Widget ):
    def __init__( self, **kwargs ):
        super(SightWidget, self).__init__(**kwargs)
        self.notes = []
        self.ref = self.getRandNote()
        self.bind( on_size=self.showLines )
        self.showLines()
        self.showNotes()
        self.midi = mido.open_input(inputname, callback=self.midiUpdate)
    def midiUpdate(self, msg):
        if msg.type == 'note_on':
            self.notes.append( msg.note )
            if self.ref.n == msg.note:
                while self.ref.n == msg.note:
                    self.ref = self.getRandNote()
        if msg.type == 'note_off':
            self.notes.remove( msg.note )
        self.showNotes()
        self.canvas.ask_update()
    def showLines(self):
        with self.canvas.before:
            Color(.8,.8,.8,1)
            Rectangle( pos=self.pos, size=(2000,1000) )
            Color(0,0,0,.8)
            for i in range(1, 7 * 9 + 1, 2 ):
                h = self.lineHeight( i )
                Line(points=(0, h, 2000, h), width=1.1)
    def showNotes(self):
        s = 10
        self.canvas.clear()
        with self.canvas:
            for n in self.notes:
                Color( 0, 0, 1, 1 )
                Ellipse(pos=(400, self.lineHeight(Note(n))-s/2), size=(s,s))
            Color( 1, 0, 0, 1 )
            Ellipse(pos=(600, self.lineHeight(self.ref)-s/2), size=(s,s))
    def lineHeight(self, i):
        if type(i) == Note:
            t = i.n // 12
            m = ( ord( Note.notes[ i.n % 12 ][0] ) - ord('C') + 7 ) % 7
            i = t * 7 + m
        return i * 4 + 75 + 25 * ( i // 36 )
    def getRandNote( self ):
        return Note( str( rand.choice( list( range(4,6) ) ) ) + chr( rand.choice( list( range(7) ) ) + ord('A') ) )

class SightApp(App):

    def build(self):
        sw = SightWidget()
        return sw


if __name__ == '__main__':
    SightApp().run()
