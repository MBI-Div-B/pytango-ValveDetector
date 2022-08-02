# PyTango Device Server for Valve State Detection

Provide the state of a generic valve by reading one or two switches via TangoAttributes
e.g. from a DAQ-device.

The switches can be configured as normally closed (NCC) or normally open (NOC).

If only one switch is provided it directly defines the two states OPEN or CLOSED.

If two switches are given they define the two states OPEN and CLOSED if they have the
opposite values.
If both inputs have the same value the valve is neither OPEN or CLOSED but in an undefined
MOVING state.