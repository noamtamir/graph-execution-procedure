class Node:
    def __init__(self, value):
        self.value = value
        self.linked_nodes = []
    
    @property
    def node_type(self):
        if self.value.startswith('s'):
            return 's'
        else:
            return 'd'
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'{str(self)} : {[str(node) for node in self.linked_nodes]}'


class Graph:
    @classmethod
    def from_links(cls, links):
        graph = Graph()
        graph.insert_links(links)
        return graph
    
    def __init__(self):
        self.nodes = {}
    
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
    
    def to_dict(self):
        return {value: [str(linked_node) for linked_node in node.linked_nodes] for value, node in self.nodes.items()}
    
    def get_execution_procedure(self, state_node):
        execution_procedure={}
        launch_sequence, next_state = self.create_launch_sequence(state_node)
        execution_procedure[str(state_node)] = {'launch': [str(node) for node in launch_sequence], 'next': str(next_state) if next_state else None}
        if next_state:
            execution_procedure.update(self.get_execution_procedure(state_node=next_state))
        return execution_procedure

    def create_launch_sequence(self, node):
        launch_sequence = set()
        next_state = None
        for linked_node in node.linked_nodes:
            if linked_node.node_type == 'd':
                launch_sequence.add(linked_node)
                linked_launch_sequence, linked_next_state = self.create_launch_sequence(linked_node)
                launch_sequence = launch_sequence | linked_launch_sequence
                assert not linked_next_state #TODO: Q: Can a dependency be a parent of a state? this assumes it cannot.
            else:
                 #TODO: Q: Can the only be 1 next state? This assumes so.
                next_state = linked_node

        return launch_sequence, next_state
