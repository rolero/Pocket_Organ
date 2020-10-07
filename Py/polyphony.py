import time
import midi
import metronome

# This code assumes only one chord will ever be sent at once.
# TODO:
# * have Midi return the MIDI message string, and have Polyphony call the looper directly

class Polyphony:
    def __init__(self, keyboard, display, looper):
        self.pending = []   #list of notes scheduled for playing in the future
                            #format of each note: (note, velocity, ticks_ms)
        self.k = keyboard
        self.d = display
        self.l = looper
        self.l.p = self
        self.midi = midi.Midi()
        self.metronome = metronome.Metronome(self.midi)
        self.scale = [60, 62, 64, 65, 67, 69, 71, 72]
        self.chord_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
        self.melody_keys_transpose = bytearray(8) #for keeping track of how which key was played
        self.instr = 22
        self.set_instr(self.instr)
        self.volume = 64
        self.set_volume(self.volume)
        #TODO: move the drum names to instr_names.py
        self.drums = [("Snare", 38), ("Bass drum", 36), ("Low tom", 45), ("High tom", 50), ("Crash cymbal", 49), ("Ride cymbal", 51), ("Open hi-hat", 46), ("Closed hi-hat", 42) ]
        
    def start_chord(self):
        def round_note(n):
            return n%12 + 60
        root = self.scale[self.k.current_note_key] + self.k.sharp #current_note_key should not be None
        
        #Here is the logic to determine the chord shape
        aug = self.k.fifth and not self.k.minor
        dim = self.k.fifth and self.k.minor
        sus4 = self.k.third and not self.k.minor
        sus2 = self.k.third and self.k.minor

        #Triad
        chord = [        round_note(root),
                         round_note(root + 4 - self.k.minor + sus4 - sus2*2),
                         round_note(root + 7 + aug - dim)
                         ]
        #Seventh
        if self.k.seventh:
            chord.append(round_note(root+10-self.k.minor))
        self.play_chord(chord, 64, 40)
        self.d.disp_chord(
        #print(
             self.chord_names[self.k.current_note_key] +
             ("#" if self.k.sharp else "") +
             ("m" if self.k.minor else "") +
             ("7" if self.k.seventh else "")
             )
    
    def play_chord(self, notes, velocity, timing): #timing = number of ms between successive notes
        """Starts playing a list of notes.
        The 1st one is played immediately, the following ones are spaced by timing (in milliseconds).
        """
        self.l.append(self.midi.note_on(self.l.chord_channel, notes[0], velocity))
        for i, n in enumerate(notes[1:], start=1):
            self.pending.append((n, velocity, time.ticks_ms()+timing*i))
        
    def stop_chord(self):
        self.l.append(self.midi.all_off(self.l.chord_channel))
        self.pending = []
        self.d.clear()

    def start_note(self, i):
        transpose = 12*self.k.fifth + 12*self.k.seventh - 12*self.k.third - 12*self.k.minor + 1*self.k.sharp
        self.melody_keys_transpose[i] = transpose
        self.l.append(self.midi.note_on(self.l.melody_channel, self.scale[i]+transpose, 64))
    
    def stop_note(self, i):
        self.l.append(self.midi.note_off(self.l.melody_channel, self.scale[i]+self.melody_keys_transpose[i], 64))

    def stop_all_notes(self):
        self.l.append(self.midi.all_off(self.l.melody_channel))
        
    def play_drum(self, note):
        name, note = self.drums[note]
        self.l.append(self.midi.note_on(self.l.drum_channel, note, 64))
        return name

    def set_instr(self, instr):
        self.instr = instr
        self.midi.set_instr(self.l.chord_channel,  instr)
        self.midi.set_instr(self.l.melody_channel, instr)
        
    def set_volume(self, vol):
        #TODO: if changing in quick succession, only append every 0.1s (requires making a queue of volume changes)
        self.midi.set_controller(self.l.chord_channel, 7, vol)
        self.midi.set_controller(self.l.melody_channel, 7, vol)

    def loop(self):
        self.metronome.loop()
        #Check if a note is due for playing, and play it. Assumes the notes are listed chronologycally.
        if len(self.pending):
            next = self.pending[0][2]
            if next <= time.ticks_ms():
                n = self.pending.pop(0)
                self.l.append(self.midi.note_on(self.l.chord_channel, n[0], n[1]))       
                
#end
