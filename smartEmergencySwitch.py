import pifacedigitalio

buttons = [ False, False, False, False ]

pifacedigital = None;

state = ""

def set_state(new_state):
    global state, buttons, pifacedigital
    
    if state is new_state:
        return
    else:
        state = new_state

    print("State: " + state);

    if new_state == "ON":
        pifacedigital.relays[0].turn_on()

    elif state == "OFF" or state == "ERROR":
        if state == "ERROR":
            pifacedigital.output_pins[2].turn_on()
            pifacedigital.output_pins[3].turn_on()
        else:
            pifacedigital.output_pins[2].turn_off()
            pifacedigital.output_pins[3].turn_off()
        
        buttons = [ False, False, False, False ]

        pifacedigital.relays[0].turn_off()

        pifacedigital.output_pins[4].turn_off()
        pifacedigital.output_pins[5].turn_off()
        pifacedigital.output_pins[6].turn_off()
        pifacedigital.output_pins[7].turn_off()
  
def switch_pressed(event):
    global state, buttons, pifacedigital
    if state == "OFF":
        buttons[event.pin_num] = not buttons[event.pin_num]
        
        # set LED
        if buttons[event.pin_num] == True:
            event.chip.output_pins[event.pin_num + 4].turn_on()

        else:
            event.chip.output_pins[event.pin_num + 4].turn_off()
    
        if buttons[0] and buttons[1] and buttons[2] and buttons[3]:
           set_state("ON")

    elif state == "ON" or state == "ERROR":
        set_state("OFF")
       
def ai_anomaly_callback():
    set_state("ERROR")

if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()

    set_state("OFF")

    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
    listener.activate()

    print("Starting the Brainuim MQTT client thread...");
    
    import brainiumClient
    import threading
    
    brainiumClient.anomalyCallback = ai_anomaly_callback
    
    brainiumMqttThread = threading.Thread(target = brainiumClient.main)
    brainiumMqttThread.start()

