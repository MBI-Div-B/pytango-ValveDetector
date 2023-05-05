#!/usr/bin/env python3

from tango import DevState, AttributeProxy
from tango.server import Device, device_property


class ValveDetector(Device):
    # Properties representing two ports of an DAQ-Device
    Input1 = device_property(
        dtype='str',
        doc='FQDN to Tango Attribute for Input1:\n'
        'domain/family/member/attribute',
    )

    Input2 = device_property(
        dtype='str',
        doc='Optional\nFQDN to Tango Attribute for Input2:\n'
        'domain/family/member/attribute',
    )

    InputType = device_property(
        dtype="str",
        default_value='0',
        doc='0 - normally open (NCC); 1 - normally closed (NOC)',
    )

    def init_device(self):
        # set up connection to a running device server 
        Device.init_device(self)
        self.set_state(DevState.INIT)
        self.info_stream('Initialization of valve device.')
        try:
            # open a attribute proxy. That means we are accessing a specific device server attribute of an running device. 
            self.input1 = AttributeProxy(self.Input1)
            self.input2 = AttributeProxy(self.Input2)
            self.set_status('Connected to device: {:s}'.format(self.Input1[:-3]))
        except:
            self.error_stream('Could not connect to DAQDevice.')
            self.set_status('Could not connect to DAQDevice.')
            self.set_state(DevState.ALARM)
            return
        
    def always_executed_hook(self):
        self.set_state(DevState.RUNNING)
        self.set_status('Reading data of valve.')
        
        # read out value of the attribute proxy
        val1 = self.input1.read().value
        val2 = self.input2.read().value

        if val1 == True and val2 == True:
            self.set_state(DevState.MOVING)
            self.set_status('Valve is moving. That means it is in the state between open and close.')
        elif val1 == True and val2 == False:
            self.set_state(DevState.CLOSE)  
            self.set_status('Valve is closed.')
                
        elif val1 == False and val2 == True:
            self.set_state(DevState.OPEN)
            self.set_status('Valve is open.')
        else:
            self.set_status('Check if everything is ok at the valve.')
            self.set_state(DevState.ALARM) 


if __name__ == '__main__':
    ValveDetector.run_server()
