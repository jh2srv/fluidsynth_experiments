import time
import rtmidi
import fluidsynth

class MidiInputHandler(object):
    def __init__(self, port, fsynth ):
        self.port = port
        self._wallclock = time.time()
        self._fsynth = fsynth

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        # if message[0] == 224:
        #     print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        if message[0] == 144:
            self._fsynth.noteon(0, message[1], message[2])
            return

        if message[0] == 128:
            self._fsynth.noteoff(0, message[1])
            return
        if message[0] == 176:
            self._fsynth.cc(0, 1, message[2]) # 1 = vibrato
            return
        
        if message[0] == 224:
            value = 130*(message[2] - 64)
            self._fsynth.pitch_bend(0, value)
            print(value)
            return        
        # print('\tdata ', data) # None
        # print('\tdata ', type(data))

def midi_callback(event, data = None):
    message, deltatime = event
    print("[%s] @%0.6f %r" % ('test', deltatime, message))
    # print('\tdata ', data) # None
    # print('\tdata ', type(data))


fsynth = fluidsynth.Synth()
fsynth.setting("audio.period-size", 256)
fsynth.setting("audio.periods", 8)
fsynth.setting("synth.chorus.active", False)
fsynth.setting("synth.reverb.active", False)

fsynth.start()
sfid = fsynth.sfload("example.sf2")
fsynth.program_select(0, sfid, 0, 0)

midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()

for i, available_port in enumerate(available_ports):
    print(i, '\t', available_port)

print('\nSelect (MPKmini2 is keyboard) ...')
x = input()
midi_in.open_port(int(x))


# midi_in.set_callback(midi_callback)




midi_in.set_callback(MidiInputHandler('test', fsynth))

while True:
    time.sleep(1)

1


# Messages:
#   0x90 = 144 = Note on
#   0x80 = 128 = Note Off
# The printed message is in format:
#       [message, note, velocitie]

# [176, 1, 0] [176, 1, 127]: joystick down up
#          [224, 0, 64]
# [224, 0, 0]    [224, 0, 64]   [224, 127, 127]