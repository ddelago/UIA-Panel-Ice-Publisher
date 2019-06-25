import requests
import sys
import RPi.GPIO as GPIO
from variable_server import VariableServer
import sys, Ice, IceStorm, time
Ice.loadSlice("eproc_cmd_tlm.ice")
import gov.nasa.jsc.er
    
print("Connecting to Trick")
"""  Trick Initialization """
variable_server = VariableServer(sys.argv[1], sys.argv[2])
print(variable_server.get_value('dyn.uia.oxygen.supply_pressure'))


with Ice.initialize(sys.argv) as communicator:
    print("Initializing IceStorm")
    """  ICE Storm Initialization """
    # base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 192.168.3.100 -p 10000")
    # print(1)
    # topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)
    # print(2)
    # # Create topic if it doesn't exist already
    # topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'eproc_tlm_topic')
    # print(3)
    # publisher = topic.getPublisher()
    # print(3.5)
    # # Create publisher object
    # pub = publisher.ice_oneway()
    # print(pub)
    # print(4)
    # panel = gov.nasa.jsc.er.TelemetryPrx.uncheckedCast(pub)
    # print(5)
    # header = gov.nasa.jsc.er.MessageHeader(0, 'TELEMETRY', 'SWITCH_PANEL') 
    # print(6)
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
            seqTelem = []
        #UIA Depress Pump
        #green enable / yellow fault LEDs
            if (GPIO.input(18) == False):
                GPIO.output(17,1)
                GPIO.output(4, 0)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_DEPRESS', 'ON'))
                payload['depress_pump'] = 'true'
                variable_server.set_value('dyn.uia.oxygen.depress_pump', 1)
                #print ("ENABLE")
            else:
                GPIO.output(17,0)
                GPIO.output(4, 1)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_DEPRESS', 'OFF'))
                payload['depress_pump'] = 'false'
                variable_server.set_value('dyn.uia.oxygen.depress_pump', 0)
                #print ("FAULT")

        #EV1
        #green led only
            #EMU1 on/off
            if (GPIO.input(22) == False):
                GPIO.output(27,1)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_POWER', 'ON'))
                payload['emu1'] = 'true'
                variable_server.set_value('dyn.uia.emu[0].power.state', 1)
                #print ("EV1 ON")
            else:
                GPIO.output(27,0)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_POWER', 'OFF'))
                payload['emu1'] = 'false'
                variable_server.set_value('dyn.uia.emu[0].power.state', 0)
                #print ("EV1 OFF")

            #EV1 SUPPLY on/off
            if (GPIO.input(10) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_SUPPLY', 'ON'))
                payload['ev1_supply'] = 'true'
                variable_server.set_value('dyn.uia.ev[0].water.supply', 1)
                #print('SUPPLY1 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_SUPPLY', 'OFF'))
                payload['ev1_supply'] = 'false'
                variable_server.set_value('dyn.uia.ev[0].water.supply', 0)
                #print('SUPPLY1 OFF')

            #EV1 WASTE on/off
            if (GPIO.input(9) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_WASTE', 'ON'))
                payload['ev1_waste'] = 'true'
                variable_server.set_value('dyn.uia.ev[0].water.waste', 1)
                #print('WASTE1 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_WASTE', 'OFF'))
                payload['ev1_waste'] = 'false'
                variable_server.set_value('dyn.uia.ev[0].water.waster', 0)
                #print('WASTE2 OFF')

            #EMU1 OXYGEN on/off
            if (GPIO.input(25) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_OXYGEN', 'ON'))
                payload['emu1_O2'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print('OXYGEN1 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_OXYGEN', 'OFF'))
                payload['emu1_O2'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print('OXYGEN2 OFF')

        #EV2
        #green led only
            #EMU2 on/off
            if (GPIO.input(24) == False):
                GPIO.output(23,1)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_POWER', 'ON'))
                payload ['emu2'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print ("EV2 ON")
            else:
                GPIO.output(23,0)
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_POWER', 'OFF'))
                payload ['emu2'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print ("EV2 OFF")

            #EV2 SUPPLY on/off
            if (GPIO.input(26) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_SUPPLY', 'ON'))
                payload['ev2_supply'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print('SUPPLY2 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_SUPPLY', 'OFF'))
                payload['ev2_supply'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print('SUPPLY2 OFF')

            #EV2 WASTE on/off
            if (GPIO.input(16) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_WASTE', 'ON'))
                payload['ev2_waste'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print('WASTE2 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_WASTE', 'OFF'))
                payload['ev2_waste'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print('WASTE2 OFF')

            #EMU2 OXYGEN on/off
            if (GPIO.input(20) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_OXYGEN', 'ON'))
                payload['emu2_O2'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print('OXYGEN2 ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_OXYGEN', 'OFF'))
                payload['emu2_O2'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print('OXYGEN2 OFF')

        #O2 Vent
            if (GPIO.input(21) == False):
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_VENT', 'ON'))
                payload['O2_vent'] = 'true'
                variable_server.set_value('dyn.uia.', 1)
                #print('O2 VENT ON')
            else:
                # seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_VENT', 'OFF'))
                payload['O2_vent'] = 'false'
                variable_server.set_value('dyn.uia.', 1)
                #print('O2 VENT OFF')

            #r = requests.patch('http://192.70.120.211:3000/api/simulation/newuiacontrols', params = payload)
            # print("make telem")
            # telemMessage = gov.nasa.jsc.er.TelemetryMessage(header, seqTelem)
            # print("transfer telem")
            # panel.transfer(telemMessage)
            
            # Trick connection


            print(payload)
            time.sleep(.250)
    
            #print(r.url)

    #except KeyboardInterrupt:
        #print ("user interruption") #interupted using Keyboard "CTRL" + "C"
        #GPIO.cleanup()

    except Exception as e:
        GPIO.cleanup()
        print (e)
