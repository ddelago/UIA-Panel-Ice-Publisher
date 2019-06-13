import sys, Ice, IceStorm, time
Ice.loadSlice("eproc_cmd_tlm.ice")
import gov.nasa.jsc.er
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 127.0.0.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    # Create topic if it doesn't exist already
    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'eproc_tlm_topic')

    # Create publisher object
    pub = topic.getPublisher().ice_oneway()
    panel = gov.nasa.jsc.er.TelemetryPrx.uncheckedCast(pub)

    header = gov.nasa.jsc.er.MessageHeader(0, 'TELEMETRY', 'SWITCH_PANEL') 
    data = gov.nasa.jsc.er.TelemetryData('HAL.UIA.SWITCH_PANEL.EMU1_POWER', 'Hello')

    seqTelem = [data]

    telemMessage = gov.nasa.jsc.er.TelemetryMessage(header, seqTelem)

    payload = {'emu1': ' ', 'ev1_supply': ' ', 'ev1_waste': ' ', 'emu1_O2': ' ',
               'emu2': ' ', 'ev2_supply': ' ', 'ev2_waste': ' ', 'emu2_O2': ' ',
               'O2_vent':' ', 'depress_pump': ' '}

    
    while True:
        payload['emu1'] = "ON"
        panel.transfer(telemMessage)
        # print(payload)
        time.sleep(.250)