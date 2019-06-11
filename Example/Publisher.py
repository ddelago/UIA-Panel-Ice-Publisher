import sys, Ice, IceStorm, time
import Demo
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 127.0.0.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    # IceStorm.TopicManagerPrx.create(topicManagerProxy, 'New_Topic')
    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'New_Topic')
    topic2 = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'eproc_cmd_topic')
    print topicManagerProxy.retrieveAll()
    # print topic2.ice_ids()

    pub = topic.getPublisher().ice_oneway()
    printer = Demo.PrinterPrx.uncheckedCast(pub)

    while True:
        time.sleep(1)
        printer.printString("Hello World")
