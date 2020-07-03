from exceptions import IllegalNode, IllegalDependency

STATE_NODE = 's'
DEPENDENCY_NODE = 'd'

class Node:
    def __init__(self, value):
        self.value = value
        self.linked_nodes = []
        self.next_states = []
        self.dependencies = []
    
    @property
    def node_type(self):
        if self.value.startswith(STATE_NODE):
            return STATE_NODE
        elif self.value.startswith(DEPENDENCY_NODE):
            return DEPENDENCY_NODE
        else:
            raise IllegalNode('Input contained illegal node types.')
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'{str(self)} : {[str(node) for node in self.linked_nodes]}'
    
    def get_dependencies(self):
        dependecies = []
        for dependency in self.dependencies:
            dependency_dependecies = dependency.get_dependencies()
            dependecies.insert(0, dependency)
            dependecies = dependency_dependecies + dependecies
        seen = set()
        dependecies = [x for x in dependecies if not (x in seen or seen.add(x))] # clean up duplicates, if dependency has already been launched
        return dependecies


class Graph:
    def __init__(self):
        self.nodes = {}

    @classmethod
    def from_links(cls, links):
        graph = Graph()
        graph.insert_links(links)
        return graph
    
    def insert_links(self, links):
        for link in links:
            self.insert_link(link)
    
    def insert_link(self, link):
        node_from_value = link[0]
        node_to_value = link[1]
        node_from = self.nodes.get(node_from_value)
        node_to = self.nodes.get(node_to_value)
        if not node_from:
            node_from = Node(node_from_value)
            self.nodes[node_from_value] = node_from
        if not node_to:
            node_to = Node(node_to_value)
            self.nodes[node_to_value] = node_to
        node_from.linked_nodes.append(node_to)
        if node_to.node_type == STATE_NODE:
            node_from.next_states.append(node_to)
        else:
            node_from.dependencies.append(node_to)
        if node_from.node_type == DEPENDENCY_NODE and node_to.node_type == STATE_NODE:
            raise IllegalDependency('A dependency node was connected to a new state node.')
        
    
    def to_dict(self):
        return {value: [str(linked_node) for linked_node in node.linked_nodes] for value, node in self.nodes.items()}
    
    def get_launch_sequence(self, state_node=None, launch_sequence=None):
        if launch_sequence is None:
            launch_sequence={}
        dependecies = state_node.get_dependencies()
        next_states = state_node.next_states
        launch_sequence[str(state_node)] = {
            'launch': [str(node) for node in dependecies],
            'next': [str(next_state) for next_state in next_states] if next_states else None
        }
        if next_states:
            for next_state in next_states:
                if not launch_sequence.get(str(next_state)):
                    launch_sequence.update(self.get_launch_sequence(state_node=next_state, launch_sequence=launch_sequence))
        return launch_sequence
