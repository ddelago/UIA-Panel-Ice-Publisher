import sys, Ice, IceStorm
import Demo
 
class PrinterI(Demo.Printer):
    def printString(self, s, current=None):
        print s
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 127.0.0.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    adapter = communicator.createObjectAdapterWithEndpoints("adapter", "tcp:udp")
    printer = PrinterI()

    subscriber = adapter.addWithUUID(printer).ice_oneway()
    adapter.activate()

    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'New_Topic')

    qos = {}
    qos["retryCount"] = "0"
    print topic.subscribeAndGetPublisher(qos, subscriber)

    communicator.waitForShutdown()
    topic.unsubscribe(subscriber)

