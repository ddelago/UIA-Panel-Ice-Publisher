import sys, Ice, IceStorm
import Demo
 
with Ice.initialize(sys.argv) as communicator:
    base = communicator.stringToProxy("DemoIceStorm/TopicManager:default -h 127.0.0.1 -p 10000")
    topicManagerProxy = IceStorm.TopicManagerPrx.checkedCast(base)

    # IceStorm.TopicManagerPrx.create(topicManagerProxy, 'New_Topic')
    topic = IceStorm.TopicManagerPrx.retrieve(topicManagerProxy, 'New_Topic')

    print topic
