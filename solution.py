from graph import Graph


def solution(links):
    if not links:
        return {}
    graph = Graph.from_links(links)
    return graph.get_execution_procedure(graph.nodes['s1'])


if __name__ == "__main__":
    links = [
        ('s1','s3'),
        ('s1','d1'),
        ('s1','d2'),
        ('s2','d4'),
        ('s2','d3'),
        ('s3','s2'),
        ('s3','d1'),
        ('s2','s4'),
        ('d3','d2'),
        ('s4','d3')
    ]
    execution_procedure = solution(links)
    print(execution_procedure)