
SIZE_FACTOR = 20

# Node status classes
OFF_NODE = 'off_node'
ON_NODE = 'on_node'
IDLE_ON = 'idle_on'
IDLE_OFF = 'idle_off'

# Edges classes
PRESSURE = 'pressure'
FLOW = 'flow'
OFFLINE = 'offline'
ALL_EDGE_CLASSES = [PRESSURE, FLOW, OFFLINE]

# Node type classes
VALVE = 'valve'
VALVE_HZ_ON = f'{VALVE}_hz_on'
VALVE_VT_ON = f'{VALVE}_vt_on'
VALVE_HZ_OFF = f'{VALVE}_hz_off'
VALVE_VT_OFF = f'{VALVE}_vt_off'
EQUIPMENT = 'obs'
SOURCE = 'source'
SINK = 'sink'
CONNECTION = 'connection'

# Nodes definition indices
NODE_ID = 0
NODE_LABEL = 1
NODE_X = 2
NODE_Y = 3
NODE_CLASS = 4

# Edges definition indices
EDGE_SOURCE = 0
EDGE_TARGET = 1
EDGE_CLASS = 2

# Node class definition indices
CLASS_NODE_LABEL = 0
CLASS_NODE_STATUS = 1
CLASS_NODE_TYPE = 2
