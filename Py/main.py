from machine import Pin

pin = Pin("B0", Pin.IN, Pin.PULL_UP)
if not(pin()):
    #Start if the "volume" key is pressed on startup
    import pocket_organ

#End
