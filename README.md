# UIA Panel Ice Publisher
ZeroC IceStorm Publisher and Subscriber in Python for UIA Panel with Trick Connection

## Getting Started
1. Make sure eProc is installed and running
2. Make sure the Trick Simulation is running (optional)
3. Install [ZeroC Ice](https://zeroc.com/downloads/ice) for Python
    - `pip install zeroc-ice`
4. Clone this repository onto Raspberry Pi

## Running

python uiaPanelPublisher.py {Trick Ip} {Trick Port} --Ice.Trace.Protocol --Ice.Trace.Network=2 --Ice.Override.ConnectTimeout=2000
python uiaPanelPublisher.py 192.168.3.104 44803 --Ice.Override.ConnectTimeout=2000
python uiaPanelPublisher.py 192.168.3.109 40463 --Ice.Trace.Protocol --Ice.Trace.Network=2 --Ice.Override.ConnectTimeout=2000

Debugging
python uiaPanelPublisher.py {Trick Ip} {Trick Port} --Ice.Trace.Protocol --Ice.Trace.Network=2 --Ice.Override.ConnectTimeout=2000
