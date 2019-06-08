import mido
inputname = 'V61:V61 MIDI 1 28:0'
with mido.open_input(inputname) as inport:
    for msg in inport:
        print( msg )
