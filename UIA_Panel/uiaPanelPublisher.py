import requests
import sys
import RPi.GPIO as GPIO
import sys, Ice, IceStorm, time
Ice.loadSlice("UIA.ice")
import UIA
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 192.168.137.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    # Create topic if it doesn't exist already
    # IceStorm.TopicManagerPrx.create(topicManagerProxy, 'UIA_Panel')
    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'UIA_Panel')
    if(topic is None):
        IceStorm.TopicManagerPrx.create(topicManagerProxy, 'UIA_Panel')

    # Create publisher object
    pub = topic.getPublisher().ice_oneway()
    panel = UIA.PanelSwitchesPrx.uncheckedCast(pub)

    print(topic, panel)


    GPIO.setmode (GPIO.BCM)

    #Depress Pump GPIOs
    GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    #EV1 GPIOs
    GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(27, GPIO.OUT)
    #EV2 GPIOs
    GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(23, GPIO.OUT)

    GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    payload = {'emu1': ' ', 'ev1_supply': ' ', 'ev1_waste': ' ', 'emu1_O2': ' ',
               'emu2': ' ', 'ev2_supply': ' ', 'ev2_waste': ' ', 'emu2_O2': ' ',
               'O2_vent':' ', 'depress_pump': ' '}

    try:
        while True:
        #UIA Depress Pump
        #green enable / yellow fault LEDs
            if (GPIO.input(18) == False):
                GPIO.output(17,1)
                GPIO.output(4, 0)
                payload ['depress_pump'] = 'true'
                #print ("ENABLE")
            else:
                GPIO.output(17,0)
                GPIO.output(4, 1)
                payload ['depress_pump'] = 'false'
                #print ("FAULT")

        #EV1
        #green led only
            #EMU1 on/off
            if (GPIO.input(22) == False):
                GPIO.output(27,1)
                payload ['emu1'] = 'true'
                #print ("EV1 ON")
            else:
                GPIO.output(27,0)
                payload ['emu1'] = 'false'
                #print ("EV1 OFF")

            #EV1 SUPPLY on/off
            if (GPIO.input(10) == False):
                payload['ev1_supply'] = 'true'
                #print('SUPPLY1 ON')
            else:
                payload['ev1_supply'] = 'false'
                #print('SUPPLY1 OFF')

            #EV1 WASTE on/off
            if (GPIO.input(9) == False):
                payload['ev1_waste'] = 'true'
                #print('WASTE1 ON')
            else:
                payload['ev1_waste'] = 'false'
                #print('WASTE2 OFF')

            #EMU1 OXYGEN on/off
            if (GPIO.input(25) == False):
                payload['emu1_O2'] = 'true'
                #print('OXYGEN1 ON')
            else:
                payload['emu1_O2'] = 'false'
                #print('OXYGEN2 OFF')

        #EV2
        #green led only
            #EMU2 on/off
            if (GPIO.input(24) == False):
                GPIO.output(23,1)
                payload ['emu2'] = 'true'
                #print ("EV2 ON")
            else:
                GPIO.output(23,0)
                payload ['emu2'] = 'false'
                #print ("EV2 OFF")

            #EV2 SUPPLY on/off
            if (GPIO.input(26) == False):
                payload['ev2_supply'] = 'true'
                #print('SUPPLY2 ON')
            else:
                payload['ev2_supply'] = 'false'
                #print('SUPPLY2 OFF')

            #EV2 WASTE on/off
            if (GPIO.input(16) == False):
                payload['ev2_waste'] = 'true'
                #print('WASTE2 ON')
            else:
                payload['ev2_waste'] = 'false'
                #print('WASTE2 OFF')

            #EMU2 OXYGEN on/off
            if (GPIO.input(20) == False):
                payload['emu2_O2'] = 'true'
                #print('OXYGEN2 ON')
            else:
                payload['emu2_O2'] = 'false'
                #print('OXYGEN2 OFF')

        #O2 Vent
            if (GPIO.input(21) == False):
                payload['O2_vent'] = 'true'
                #print('O2 VENT ON')
            else:
                payload['O2_vent'] = 'false'
                #print('O2 VENT OFF')

            #r = requests.patch('http://192.70.120.211:3000/api/simulation/newuiacontrols', params = payload)
            panel.sendState(payload)
            print(payload)
            time.sleep(.250)
    
            #print(r.url)

    #except KeyboardInterrupt:
        #print ("user interruption") #interupted using Keyboard "CTRL" + "C"
        #GPIO.cleanup()

    except Exception as e:
        GPIO.cleanup()
        print (e)
