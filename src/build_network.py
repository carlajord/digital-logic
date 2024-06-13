import os
import urllib.parse
import src.constants as cn

ASSET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))


class Network():

    def __init__(self) -> None:

        # initialize network
        self.nodes_def, self.edges_def, self.stylesheet_def = self.initial_network_definition()
        self.nodes = self.make_nodes(self.nodes_def)
        self.edges = self.make_edges(self.edges_def)
        self.stylesheet = self.make_styles(self.stylesheet_def)
        self.network = self.nodes + self.edges

    def get_valve_svg(self, size, color, angle=0):
        svg = f'<svg fill="{color}" width="{size}px" height="{size}px" viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg" stroke="{color}" transform="rotate({angle})"> <g id="SVGRepo_bgCarrier" stroke-width="0"/> <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"/> <g id="SVGRepo_iconCarrier"> <path d="M208,196.68652A15.9999,15.9999,0,0,1,196.68652,224H59.31348A15.9999,15.9999,0,0,1,48,196.68652l68.68457-68.68506L48,59.31348A15.9999,15.9999,0,0,1,59.31348,32h137.373A15.9999,15.9999,0,0,1,208,59.31348l-68.68457,68.68506Z"/> </g> </svg>'
        return 'data:image/svg+xml;utf-8,' + urllib.parse.quote(svg, safe='')

    def initial_network_definition(self):
        nodes = [
            ['source_1', 'Source 1', 0, 0, f'node {cn.OFF_NODE}'],
            ['valve_1', '', 0, 5, f'node {cn.VALVE_VT_OFF}'],
            ['connection_1', '', 0, 10, f'node {cn.IDLE_NODE} {cn.CONNECTION}'],
            ['valve_2', '', 0, 15, f'node {cn.VALVE_VT_OFF}'],
            ['sink_1', 'Sink 1', 0, 20, f'node {cn.IDLE_NODE}'],
            ['valve_3', '', 5, 10, f'node {cn.VALVE_HZ_OFF}'],
            ['observer_1', 'Equipment 1', 10, 10, f'node {cn.IDLE_NODE} {cn.EQUIPMENT}'],
            ['valve_4', '', 15, 10, f'node {cn.VALVE_HZ_OFF}'],
            ['sink_2', 'Sink 1', 20, 10, f'node {cn.IDLE_NODE}'],
        ]
        edges = [
            ['source_1', 'valve_1', cn.OFFLINE],
            ['valve_1', 'connection_1', cn.OFFLINE],
            ['connection_1', 'valve_2', cn.OFFLINE],
            ['valve_2', 'sink_1', cn.OFFLINE],
            ['connection_1', 'valve_3', cn.OFFLINE],
            ['valve_3', 'observer_1', cn.OFFLINE],
            ['observer_1', 'valve_4', cn.OFFLINE],
            ['valve_4', 'sink_2', cn.OFFLINE],
        ]
        stylesheet = [
            ['node', {'content': 'data(label)'}],
            [f'.{cn.OFF_NODE}', {'background-color': 'red', 'line-color': 'red'}],
            [f'.{cn.ON_NODE}', {'background-color': 'green', 'line-color': 'green'}],
            [f'.{cn.PRESSURE}', {'line-color': 'green'}],
            [f'.{cn.FLOW}', {'line-color': 'orange'}],
            [f'.{cn.OFFLINE}', {'line-color': 'grey'}],
            [f'.{cn.VALVE_VT_OFF}', {'shape': 'square',
                              'background-color': 'white', 'line-color': 'white',
                              'background-image': self.get_valve_svg(2*cn.SIZE_FACTOR, "red", 0)}],
            [f'.{cn.VALVE_HZ_OFF}', {'shape': 'square',
                              'background-color': 'white', 'line-color': 'white',
                              'background-image': self.get_valve_svg(2*cn.SIZE_FACTOR, "red", 270)}],
            [f'.{cn.VALVE_VT_ON}', {'shape': 'square',
                              'background-color': 'white', 'line-color': 'white',
                              'background-image': self.get_valve_svg(2*cn.SIZE_FACTOR, "green", 0)}],
            [f'.{cn.VALVE_HZ_ON}', {'shape': 'square',
                              'background-color': 'white', 'line-color': 'white',
                              'background-image': self.get_valve_svg(2*cn.SIZE_FACTOR, "green", 270)}],
            [f'.{cn.EQUIPMENT}', {'shape': 'square'}],
            [f'.{cn.CONNECTION}', {'width': "1px", 'height': "1px"}]
        ]
        return nodes, edges, stylesheet
    

    def make_nodes(self, network_node_definition):

        nodes = [
            {
                'data': {'id': short, 'label': label},
                'position': {'x': x*cn.SIZE_FACTOR, 'y': y*cn.SIZE_FACTOR},
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
    
    def get_node_idx(self, node):
        for idx, n in enumerate(self.nodes_def):
            if n[0] == node: break
        return idx
    
    def get_neighbor_edges_idx(self, node):
        upstream_edges_idx = []
        downstream_edges_idx = []
        for idx, ed in enumerate(self.edges_def):
            if ed[cn.EDGE_SOURCE] == node:
                downstream_edges_idx.append(idx)
            if ed[cn.EDGE_TARGET] == node:
                upstream_edges_idx.append(idx)
        return upstream_edges_idx, downstream_edges_idx
    
    def get_neighbor_nodes_idx(self, node):
        upstream_nodes_idx = []
        downstream_nodes_idx = []
        for ed in self.edges_def:
            if ed[cn.EDGE_SOURCE] == node:
                downstream_nodes_idx.append(self.get_node_idx(ed[cn.EDGE_TARGET]))
            if ed[cn.EDGE_TARGET] == node:
                upstream_nodes_idx.append(self.get_node_idx(ed[cn.EDGE_SOURCE]))
        return upstream_nodes_idx, downstream_nodes_idx

    def get_neighbor_edges_class_from_node(self, node):

        upstream_edges_idx, downstream_edges_idx = self.get_neighbor_edges_idx(node)

        downstream_edge_class = []
        upstream_edge_class = []
        for idx in upstream_edges_idx:
            upstream_edge_class.append(self.edges_def[idx][cn.EDGE_CLASS])
        for idx in downstream_edges_idx:
            downstream_edge_class.append(self.edges_def[idx][cn.EDGE_CLASS])
        
        return upstream_edge_class, downstream_edge_class
        
    def get_neighbor_node_class_from_node(self, node):

        upstream_nodes_idx, downstream_nodes_idx = self.get_neighbor_nodes_idx(node)
        downstream_node_class = []
        upstream_node_class = []
        for idx in upstream_nodes_idx:
            upstream_node_class.append(self.nodes_def[idx][cn.NODE_CLASS])
        for idx in downstream_nodes_idx:
            downstream_node_class.append(self.nodes_def[idx][cn.NODE_CLASS])

        return upstream_node_class, downstream_node_class
    
    def change_network_status(self, node_changed, node_classes):

        # get changed node index in nodes
        idx_node = self.get_node_idx(node_changed)
        
        # --- update nodes
        self.update_nodes(node_changed, node_classes, idx_node)

        # --- update edges
        self.update_edges(node_changed, node_classes[cn.CLASS_NODE_STATUS])

        # if downstream node is sink, equipment or connection, trigger change node on downstream node
        _, downstream_nodes = self.get_neighbor_nodes_idx(node_changed)

        for idx in downstream_nodes:

            child_node = self.nodes_def[idx][cn.NODE_ID]
            child_class = self.nodes_def[idx][cn.NODE_CLASS].split()

            # update idle nodes
            if child_node.startswith(cn.SINK) or child_node.startswith(cn.EQUIPMENT) or child_node.startswith(cn.CONNECTION):
                self.change_network_status(child_node, child_class)
            
        return node_classes[cn.CLASS_NODE_STATUS]
    
    def update_nodes(self, node_changed, node_classes, idx):

        # if connection or equipment: follow mapping for upstream edge
        if node_changed.startswith(cn.SINK) or node_changed.startswith(cn.EQUIPMENT) or node_changed.startswith(cn.CONNECTION):
            upstream_edge_class, _ = self.get_neighbor_edges_class_from_node(node_changed)
            for edc in upstream_edge_class:
                if edc == cn.OFFLINE: node_classes[cn.CLASS_NODE_STATUS] = cn.IDLE_NODE
                else: node_classes[cn.CLASS_NODE_STATUS] = cn.ON_NODE
        
        # if source: change on/off
        elif node_changed.startswith(cn.SOURCE):
            if node_classes[cn.CLASS_NODE_STATUS] == cn.ON_NODE: node_classes[cn.CLASS_NODE_STATUS] = cn.OFF_NODE
            elif node_classes[cn.CLASS_NODE_STATUS] == cn.OFF_NODE: node_classes[cn.CLASS_NODE_STATUS] = cn.ON_NODE
        
        # if valve: change on/off
        elif node_changed.startswith(cn.VALVE):
            if node_classes[cn.CLASS_NODE_STATUS].endswith('on'):
                node_classes[cn.CLASS_NODE_STATUS] = node_classes[cn.CLASS_NODE_STATUS].replace('on', 'off')
            else:
                node_classes[cn.CLASS_NODE_STATUS] = node_classes[cn.CLASS_NODE_STATUS].replace('off', 'on')
        
        # insert change into network
        self.nodes_def[idx][cn.NODE_CLASS] = " ".join(node_classes)

    def update_edges(self, node_changed, new_node_status):
        
        _, downstream_edges = self.get_neighbor_edges_idx(node_changed)
        new_edge_class = cn.OFFLINE

        if node_changed.startswith(cn.SOURCE):
            # if source: flip on/off
            if new_node_status == cn.ON_NODE: new_edge_class = cn.PRESSURE
            else: new_edge_class = cn.OFFLINE

        elif node_changed.startswith(cn.VALVE):
            # if valve:
            #    ON == same edge as upstream
            #    OFF == same edge as downstream
            upstream_edge_class, downstream_edge_class = self.get_neighbor_edges_class_from_node(node_changed)
            if new_node_status.endswith('on'):
                new_edge_class = upstream_edge_class[0]
            else:
                new_edge_class = cn.OFFLINE#downstream_edge_class[0]

        elif node_changed.startswith(cn.CONNECTION) or node_changed.startswith(cn.EQUIPMENT):
            # if node or equipment: follow upstream edge class
            upstream_edge_class, _ = self.get_neighbor_edges_class_from_node(node_changed)
            new_edge_class = upstream_edge_class[0]

        for val in downstream_edges:
            self.edges_def[val][cn.EDGE_CLASS] = new_edge_class
        
        return new_edge_class

    def build_network(self):
        new_nodes = self.make_nodes(self.nodes_def)
        new_edges = self.make_edges(self.edges_def)
        return new_nodes + new_edges

    def update(self, raw):
        
        node_changed = raw['data']['id']

        if node_changed.startswith(cn.SINK): # do nothing
            elements = self.build_network()
            return elements

        # Update node and edges accordingly
        node_classes = raw['classes'].split()
        self.change_network_status(node_changed, node_classes)

        # Rebuild updated network
        elements = self.build_network()
        
        return elements