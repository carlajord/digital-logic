SIZE_FACTOR = 20

# Node status classes
OFF_NODE = 'off_node'
ON_NODE = 'on_node'
IDLE_NODE = 'idle_node'
ALL_STATUS_CLASSES = [OFF_NODE, ON_NODE, IDLE_NODE]

# Edges classes
PRESSURE = 'pressure'
FLOW = 'flow'
OFFLINE = 'offline'
ALL_EDGE_CLASSES = [PRESSURE, FLOW, OFFLINE]

# Node type classes
VALVE = 'valve'
EQUIPMENT = 'obs'
SOURCE = 'source'
SINK = 'sink'
NODE = 'node'

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

# Edge - Node Class Mapping
EDGE_NODE_CLASS_MAP = {
    OFF_NODE: OFFLINE,
    ON_NODE: PRESSURE
}

class Network():

    def __init__(self) -> None:

        # initialize network
        self.nodes_def, self.edges_def, self.stylesheet_def = self.initial_network_definition()
        self.nodes = self.make_nodes(self.nodes_def)
        self.edges = self.make_edges(self.edges_def)
        self.stylesheet = self.make_styles(self.stylesheet_def)
        self.network = self.nodes + self.edges

    def initial_network_definition(self):
        nodes = [
            ['source_1', 'Source 1', 0*SIZE_FACTOR, 0*SIZE_FACTOR, f'node {OFF_NODE}'],
            ['valve_1', 'Valve 1', 0*SIZE_FACTOR, 5*SIZE_FACTOR, f'node {OFF_NODE} {VALVE}'],
            ['node_1', 'Node 1', 0*SIZE_FACTOR, 10*SIZE_FACTOR, f'node {IDLE_NODE}'],
            ['valve_2', 'Valve 2', 0*SIZE_FACTOR, 15*SIZE_FACTOR, f'node {OFF_NODE} {VALVE}'],
            ['sink_1', 'Sink 1', 0*SIZE_FACTOR, 20*SIZE_FACTOR, f'node {IDLE_NODE}'],
            ['valve_3', 'Valve 3', 5*SIZE_FACTOR, 10*SIZE_FACTOR, f'node {OFF_NODE} {VALVE}'],
            ['observer_1', 'Equipment 1', 10*SIZE_FACTOR, 10*SIZE_FACTOR, f'node {IDLE_NODE} {EQUIPMENT}'],
            ['valve_4', 'Valve 4', 15*SIZE_FACTOR, 10*SIZE_FACTOR, f'node {OFF_NODE} {VALVE}'],
            ['sink_2', 'Sink 1', 20*SIZE_FACTOR, 10*SIZE_FACTOR, f'node {IDLE_NODE}'],
        ]
        edges = [
            ['source_1', 'valve_1', OFFLINE],
            ['valve_1', 'node_1', OFFLINE],
            ['node_1', 'valve_2', OFFLINE],
            ['valve_2', 'sink_1', OFFLINE],
            ['node_1', 'valve_3', OFFLINE],
            ['valve_3', 'observer_1', OFFLINE],
            ['observer_1', 'valve_4', OFFLINE],
            ['valve_4', 'sink_2', OFFLINE],
        ]
        stylesheet = [
            ['node', {'content': 'data(label)'}],
            [f'.{OFF_NODE}', {'background-color': 'red', 'line-color': 'red'}],
            [f'.{ON_NODE}', {'background-color': 'green', 'line-color': 'green'}],
            [f'.{PRESSURE}', {'line-color': 'green'}],
            [f'.{FLOW}', {'line-color': 'orange'}],
            [f'.{OFFLINE}', {'line-color': 'grey'}],
            #[f'.{VALVE}', {'background-image': 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Alloy_valves.JPG'}],
            [f'.{VALVE}', {'shape': 'triangle', 'size': 10}],
            [f'.{EQUIPMENT}', {'shape': 'square', 'size': 10}]
        ]
        return nodes, edges, stylesheet
    

    def make_nodes(self, network_node_definition):

        nodes = [
            {
                'data': {'id': short, 'label': label},
                'position': {'x': x, 'y': y},
                'classes': style_class
            }
            for short, label, x, y, style_class in network_node_definition
        ]
        
        return nodes

    def make_edges(self, network_edge_definition):
        edges = [
            {
            'data': {'source': source, 'target': target},
            'classes': style_class
            }
        for source, target, style_class in network_edge_definition
    ]
        return edges

    def make_styles(self, stylesheet_data):
        custom_stylesheet = [
            {
                'selector': selector,
                'style': style
            }
            for selector, style in stylesheet_data
        ]
        return custom_stylesheet
    
    def get_neighbor_edges_class_from_node(self, node):

        downstream_edge_class = []
        upstream_edge_class = []
        for idx, ed in enumerate(self.edges_def):
            if ed[EDGE_SOURCE] == node:
                downstream_edge_class.append(self.edges_def[idx][EDGE_CLASS])
            if ed[EDGE_TARGET] == node:
                upstream_edge_class.append(self.edges_def[idx][EDGE_CLASS])
        return upstream_edge_class, downstream_edge_class

    def get_neighbor_nodes_from_node(self, node):

        downstream_nodes = []
        upstream_nodes = []
        for idx, ed in enumerate(self.edges_def):
            if ed[EDGE_SOURCE] == node:
                downstream_nodes.append(self.edges_def[idx][EDGE_TARGET])
            if ed[EDGE_TARGET] == node:
                upstream_nodes.append(self.edges_def[idx][EDGE_SOURCE])

        return upstream_nodes, downstream_nodes

    def change_network_status(self, node_changed, node_classes):

        # get changed node index in nodes
        for idx, n in enumerate(self.nodes_def):
            if n[0] == node_changed: break

        # if sink or equipment: follow mapping for upstream edge
        if node_changed.startswith(SINK) or node_changed.startswith(EQUIPMENT) or node_changed.startswith(NODE):
            upstream_edge_class, _ = self.get_neighbor_edges_class_from_node(node_changed)
            for edc in upstream_edge_class:
                if edc == OFFLINE: node_classes[CLASS_NODE_STATUS] = IDLE_NODE
                else: node_classes[CLASS_NODE_STATUS] = ON_NODE
            
        # if source or valve: change on/off
        if node_changed.startswith(SOURCE) or node_changed.startswith(VALVE):
            if node_classes[CLASS_NODE_STATUS] == ON_NODE: node_classes[CLASS_NODE_STATUS] = OFF_NODE
            elif node_classes[CLASS_NODE_STATUS] == OFF_NODE: node_classes[CLASS_NODE_STATUS] = ON_NODE
        
        # insert change into network
        self.nodes_def[idx][NODE_CLASS] = " ".join(node_classes)
        
        self.change_edge_status(node_changed, node_classes[CLASS_NODE_STATUS])

        # if downstream node is sink or equipment, trigger change node on downstream node
        _, downstream_nodes = self.get_neighbor_nodes_from_node(node_changed)
        for child_node in downstream_nodes:
            if child_node.startswith(SINK) or child_node.startswith(EQUIPMENT) or child_node.startswith(NODE):
                for idx_child, n in enumerate(self.nodes_def):
                    if n[0] == child_node:
                        child_class = self.nodes_def[idx_child][NODE_CLASS]
                
                self.change_network_status(child_node, child_class.split())
        
        return node_classes[CLASS_NODE_STATUS]

    def change_edge_status(self, node_changed, new_node_status):
        
        downtream_edges = []
        for idx, ed in enumerate(self.edges_def):
            if ed[EDGE_SOURCE] == node_changed:
                downtream_edges.append(idx)

        new_edge_class = OFFLINE

        if node_changed.startswith(SOURCE):
            # if source: flip on/off
            if new_node_status == ON_NODE: new_edge_class = PRESSURE
            else: new_edge_class = OFFLINE

        elif node_changed.startswith(VALVE):
            # if valve: ON == same edge as upstream / OFF == downstream is closed

            if new_node_status == ON_NODE:
                upstream_edge_class, _ = self.get_neighbor_edges_class_from_node(node_changed)
                new_edge_class = upstream_edge_class[0]
            else:
                new_edge_class = OFFLINE

        elif node_changed.startswith(NODE) or node_changed.startswith(EQUIPMENT):
            # if node or equipment: follow upstream edge class
            upstream_edge_class, _ = self.get_neighbor_edges_class_from_node(node_changed)
            new_edge_class = upstream_edge_class[0]

        for val in downtream_edges:
            self.edges_def[val][EDGE_CLASS] = new_edge_class
        
        return new_edge_class

    def build_network(self):
        new_nodes = self.make_nodes(self.nodes_def)
        new_edges = self.make_edges(self.edges_def)
        return new_nodes + new_edges

    def update(self, raw):
        
        node_changed = raw['data']['id']

        if node_changed.startswith(SINK): # do nothing
            elements = self.build_network()
            return elements

        # Update node and edges accordingly
        node_classes = raw['classes'].split()
        self.change_network_status(node_changed, node_classes)

        # Rebuild updated network
        elements = self.build_network()
        
        return elements