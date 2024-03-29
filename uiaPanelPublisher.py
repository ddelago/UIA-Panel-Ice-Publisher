import requests
import sys
import RPi.GPIO as GPIO
from variable_server import VariableServer
import sys, Ice, IceStorm, time
Ice.loadSlice("eproc_cmd_tlm.ice")
import gov.nasa.jsc.er
import argparse
    
# Assign description to the help doc
parser = argparse.ArgumentParser(
    description='Starts connection to Trick and Ice and streams UIA Panel State')

# Add arguments
parser.add_argument(
    '--trickAddr', type=str, help='Trick Sim IP Address', required=False)
parser.add_argument(
    '--trickPort', type=str, help='Trick Sim Port Number', required=False)
parser.add_argument(
    '--iceAddr', type=str, help='Ice IP Address (eProc)', required=True)
parser.add_argument(
    '--Ice.Override.ConnectTimeout', type=str, help='Timeout value for Ice connection attempts', required=False)
parser.add_argument(
    '--Ice.Trace.Protocol', action='store_true', help='Enabled Ice tracing', required=False)
parser.add_argument(
    '--Ice.Trace.Network', type=str, help='Enable Ice Network tracing', required=False)

# Array for all arguments passed to script
args = parser.parse_args()


"""  Trick Initialization """
if args.trickAddr is not None and args.trickPort is not None:
    print("Connecting to Trick at {}:{}".format(args.trickAddr, args.trickPort))
    variable_server = VariableServer(args.trickAddr, args.trickPort)
    print("connected to trick")

""" Begin Connection to Ice """
with Ice.initialize(sys.argv) as communicator:
    print("Initializing IceStorm")
    """  ICE Storm Initialization """
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h {} -p 10000".format(args.iceAddr))
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)
    
    # Create topic if it doesn't exist already
    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'eproc_tlm_topic')
    
    # Create publisher object
    pub = topic.getPublisher().ice_oneway()
    panel = gov.nasa.jsc.er.TelemetryPrx.uncheckedCast(pub)
    header = gov.nasa.jsc.er.MessageHeader(0, 'TELEMETRY', 'SWITCH_PANEL') 
    
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

    # Used for printing values to terminal
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
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_DEPRESS', 'ON'))
                payload['depress_pump'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.oxygen.depress_pump', 1)
            else:
                GPIO.output(17,0)
                GPIO.output(4, 1)
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_DEPRESS', 'OFF'))
                payload['depress_pump'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.oxygen.depress_pump', 0)
        #EV1
        #green led only
            #EMU1 on/off
            if (GPIO.input(22) == False):
                GPIO.output(27,1)
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_POWER', 'ON'))
                payload['emu1'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[0].power.state', 1)
            else:
                GPIO.output(27,0)
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_POWER', 'OFF'))
                payload['emu1'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[0].power.state', 0)


            #EV1 SUPPLY on/off
            if (GPIO.input(10) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_SUPPLY', 'ON'))
                payload['ev1_supply'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[0].water.supply', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_SUPPLY', 'OFF'))
                payload['ev1_supply'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[0].water.supply', 0)

            #EV1 WASTE on/off
            if (GPIO.input(9) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_WASTE', 'ON'))
                payload['ev1_waste'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[0].water.waste', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV1_WATER_WASTE', 'OFF'))
                payload['ev1_waste'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[0].water.waste', 0)

            #EMU1 OXYGEN on/off
            if (GPIO.input(25) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_OXYGEN', 'ON'))
                payload['emu1_O2'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[0].oxygen.valve', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_OXYGEN', 'OFF'))
                payload['emu1_O2'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[0].oxygen.valve', 0)

        #EV2
        #green led only
            #EMU2 on/off
            if (GPIO.input(24) == False):
                GPIO.output(23,1)
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_POWER', 'ON'))
                payload ['emu2'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[1].power.state', 1)
            else:
                GPIO.output(23,0)
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_POWER', 'OFF'))
                payload ['emu2'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[1].power.state', 0)

            #EV2 SUPPLY on/off
            if (GPIO.input(26) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_SUPPLY', 'ON'))
                payload['ev2_supply'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[1].water.supply', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_SUPPLY', 'OFF'))
                payload['ev2_supply'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[1].water.supply', 0)

            #EV2 WASTE on/off
            if (GPIO.input(16) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_WASTE', 'ON'))
                payload['ev2_waste'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[1].water.waste', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EV2_WATER_WASTE', 'OFF'))
                payload['ev2_waste'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.ev[1].water.waste', 0)

            #EMU2 OXYGEN on/off
            if (GPIO.input(20) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_OXYGEN', 'ON'))
                payload['emu2_O2'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[1].oxygen.valve', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU2_OXYGEN', 'OFF'))
                payload['emu2_O2'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.emu[1].oxygen.valve', 0)

        #O2 Vent
            if (GPIO.input(21) == False):
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_VENT', 'ON'))
                payload['O2_vent'] = 'true'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.oxygen.vent', 1)
            else:
                seqTelem.append(gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.O2_VENT', 'OFF'))
                payload['O2_vent'] = 'false'
                if args.trickAddr is not None and args.trickPort is not None:
                    variable_server.set_value('dyn.uia.oxygen.vent', 0)

            # IceStorm publish
            telemMessage = gov.nasa.jsc.er.TelemetryMessage(header, seqTelem)
            panel.transfer(telemMessage)
            
            if args.trickAddr is not None and args.trickPort is not None:
                oxygen_supply_pressure = variable_server.get_value('dyn.uia.oxygen.supply_pressure')
                emu1_voltage = variable_server.get_value('dyn.uia.emu[0].power.voltage')
                emu2_voltage = variable_server.get_value('dyn.uia.emu[1].power.voltage')
                print("Oxygen Supply Pressure: {}\nEMU1 Voltage: {}\nEMU2 Voltage: {}".format(oxygen_supply_pressure, emu1_voltage, emu2_voltage))
            print(payload)
            time.sleep(.250)
    

    except KeyboardInterrupt:
        print ("user interruption") #interupted using Keyboard "CTRL" + "C"
        GPIO.cleanup()

    except Exception as e:
        GPIO.cleanup()
        print (e)
