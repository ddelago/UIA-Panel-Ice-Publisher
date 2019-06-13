import sys, Ice, IceStorm
Ice.loadSlice("eproc_cmd_tlm.ice")
import gov.nasa.jsc.er
 
class PanelI(gov.nasa.jsc.er.Telemetry):
    def transfer(self, s, current=None):
        print s
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 127.0.0.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    adapter = communicator.createObjectAdapterWithEndpoints("adapter", "tcp:udp")
    panel = PanelI()

    subscriber = adapter.addWithUUID(panel).ice_oneway()
    adapter.activate()

    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'eproc_tlm_topic')

    qos = {}
    qos["retryCount"] = "0"
    print topic.subscribeAndGetPublisher(qos, subscriber)

    communicator.waitForShutdown()
    topic.unsubscribe(subscriber)

