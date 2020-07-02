from unittest import TestCase
from solution import solution
from exceptions import IllegalNode, MultipleNextStatesError, IllegalDependency

class TestSolution(TestCase):
    def test_example(self):
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
        expected = {
            's1': {
                'launch': ['d2','d1'],
                'next': 's3'
            },
            's2': {
                'launch': ['d2', 'd3', 'd4'],
                'next': 's4'
            },
            's3': {
                'launch': ['d1'],
                'next': 's2'
            },
            's4': {
                'launch': ['d2', 'd3'],
                'next': None
            }
        }
        self.assertEquals(solution(links), expected)
    
    def test_empty_list(self):
        self.assertEquals(solution([]), {})

    def test_single_link(self):
        self.assertEquals(solution([('s1', 'd1')]), {'s1': {'launch': ['d1'], 'next': None}})

    def test_nested_dependencies(self):
        links = [
            ('s1','s2'),
            ('s1', 'd1'),
            ('s1', 'd2'),
            ('s1', 'd3'),
            ('s2', 'd3'),
            ('s2', 'd4'),
            ('s2', 'd5'),
            ('s2', 'd6'),
            ('s2', 's3'),
            ('d4', 'd1'),
            ('d5', 'd2'),
            ('d6', 'd3'),
            ('s3', 'd7'),
            ('s3', 'd8'),
            ('s3', 'd9'),
            ('d7', 'd8'),
            ('d8', 'd9'),
            ('d8', 'd5'),
            ('d9', 'd1'),
        ]
        expected = {
            's1': {
                'launch': ['d3','d2', 'd1'],
                'next': 's2'
            },
            's2': {
                'launch': ['d3', 'd6', 'd2', 'd5', 'd1', 'd4'],
                'next': 's3'
            },
            's3': {
                'launch': ['d1', 'd9', 'd2', 'd5', 'd8', 'd7'],
                'next': None
            }
        }
        self.assertEquals(solution(links), expected)

    def test_illegal_nodes(self):
        with self.assertRaises(IllegalNode):
            solution([('s1','d1'), ('s1','f1')])

    def test_multiple_next_states(self):
        with self.assertRaises(MultipleNextStatesError):
            solution([('s1','d1'), ('s1','s2'), ('s1','s3')])

    def test_illegal_dependency(self):
        with self.assertRaises(IllegalDependency):
            solution([('s1','d1'), ('d1','s2')])