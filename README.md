# UIA Panel Ice Publisher
ZeroC IceStorm Publisher and Subscriber in Python for UIA Panel with Trick Connection

## Getting Started
1. Make sure eProc is installed and running
2. Make sure the Trick Simulation is running (optional)
3. Install [ZeroC Ice](https://zeroc.com/downloads/ice) for Python
    - `pip install zeroc-ice`
4. Clone this repository onto Raspberry Pi

## Running
The file that you would run on the Raspberry Pi would be the `uiaPanelPublisher.py` Python file. 
To run, a few command line arguements are needed:
- Trick IP Address (Optional)
- Trick IP Port (Optional)
- Ice IP Address (Required)
- Ice Override Connection Timeout Flag (**Required!** Or else execution could hang)
- Ice Trace Protocol (Optional, for debugging)
- Ice Trace Network (Optional, for debugging)

Example executions:
- With Connection to Trick
    ```bash
    $ python uiaPanelPublisher.py --trickAddr={Trick Ip} --trickPort={Trick Port} --iceAddr={Ice Address} --Ice.Override.ConnectTimeout=2000
    ```
- Without Connection to Trick (Only Ice)
    ```bash
    $ python uiaPanelPublisher.py --iceAddr={Ice Address} --Ice.Override.ConnectTimeout=2000
    ```
- With Ice Debugging
    ```bash
    $ python uiaPanelPublisher.py --iceAddr={Ice Address} --Ice.Trace.Protocol --Ice.Trace.Network=2 --Ice.Override.ConnectTimeout=2000
    ```
- Real Example
    ```bash
    $ python uiaPanelPublisher.py --iceAddr=192.168.3.100 --Ice.Override.ConnectTimeout=2000
    ```

## NOTE
If this is the first time that you are running eProc and this application, you may run into some issues. The issue occurs whenever the publisher attempts to connect to Ice. The Ice server stores a log of its hosts and the publisher will attempt to establish a connection to each of these hosts (yours just may be further down the line). 
