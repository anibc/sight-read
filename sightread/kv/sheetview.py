from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.layout import Layout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import *

import random as rand
from sightread.note import Note
import mido

def midoinputname():
    gen = ( s for s in mido.get_input_names() if s[ -1 ] == '0' and s[ :3 ] == 'V61' )
    try:
        inputname = next( gen )
    except StopIteration as e:
        inputname = mido.get_input_names()[ 0 ]
    return inputname

class SheetView( FloatLayout ):
    def __init__( self, **kwargs ):
        super(SheetView, self).__init__(**kwargs)
        self.notes = []
        self.ref = self.getRandNote()
        self.bind( on_size=self.showLines )
        self.showLines()
        self.midi = mido.open_input(midoinputname(), callback=self.midiUpdate)
    def midiUpdate(self, msg):
        if msg.type == 'note_on':
            print( msg.note )
            self.notes.append( msg.note )
            if self.ref.n == msg.note:
                while self.ref.n == msg.note:
                    self.ref = self.getRandNote()
        if msg.type == 'note_off':
            self.notes.remove( msg.note )
        self.showNotes()
        self.canvas.ask_update()
    def showLines(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.8,.8,.8,1)
            Rectangle( pos=self.pos, size=(2000,500) )
            Color(*[1]*4)
            for i in range( 0, 130, 12 ):
                h = self.lineHeight( i )
                Line(points=(0,h,2000,h), width=3)
            Color(0,0,0,.8)
            for i in [ Note( i ) for i in range( 43, 78 ) if Note( i ).isWhite() ][::2]:
                h = self.lineHeight( i )
                Line(points=(0, h, 2000, h), width=1.1)
            Color( 1, 0, 1, 0.5 )
            Rectangle( pos=self.pos, size=self.size )
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
        if type( i ) == Note:
            i = i.white().n
        else:
            i = Note( i ).white().n
        return i * 4 + 15 + ( 50 if i > 60 else ( 25 if i == 60 else 0 ) )
    def getRandNote( self ):
        return Note( str( rand.choice( list( range(4,6) ) ) ) + chr( rand.choice( list( range(7) ) ) + ord('A') ) )

