'''
Class structure for graphs
TODO: maybe implement class for Paths
'''

from timeit import default_timer as timer


class Graph:
    def __init__(self, graph, s, t):
        self.graph = graph
        self.s = s
        self.t = t
        self.flow_decomposition_paths = []
        self.safe_paths = []
        self.times = {'decomposition': 0, 'safety': 0}

    def excess_flow(self, path):
        '''
        excess_flow(self, path) -> int
        Calculates the excess flow  of the given path. 
        Returns value of excess flow.
        '''
        flow_sum = 0
        flow_out_sum = 0
        for e in path:
            flow_sum += self.graph.edges[e]['capacity']
            flow_out_sum += self.graph.nodes[e[0]]['flow_out']
        return flow_sum - (flow_out_sum - self.graph.nodes[path[0][0]]['flow_out'])

    def safety_of_path(self, path, w):
        '''
        safety_of_path(self, path, w) -> Boolean
        If the given path is w-safe returns true else return false.
        '''
        return self.excess_flow(path) >= w and w > 0

    def maximal_safety(self, flow_decomposition=None, timer=False):
        '''
        maximal_safety(self, flow_decomposition) -> list of paths
        Uses maximal safety algorithm (by Shahbaz, Tomescu) to compute a list of paths.
        Paths are represented as list of edges.
        flow_decomposition parameter is used for testing.
        timer parameter is used measuring the execution of algorithm
        TODO: refactor such that uses only indices to handel the mximum safe part of the paths
        '''
        if not flow_decomposition:
            self.flow_decomposition()
        else:
            self.flow_decomposition_paths = flow_decomposition
        if timer:
            start = timer()
        for path in self.flow_decomposition_paths:
            sub = [path[0], path[1]]
            f = self.excess_flow(sub)
            i = 1
            added = False
            while True:
                if i == len(path)-1 and f > 0:
                    if len(sub) >= 2:
                        self.safe_paths.append(sub)
                    break
                if f > 0:
                    i += 1
                    f_out = self.graph.nodes[path[i][0]]['flow_out']
                    f -= (f_out - self.graph.edges[path[i]]['capacity'])
                    sub.append(path[i])
                    added = False
                else:
                    first = sub[0]
                    if not added:
                        if len(sub[0:-1]) >= 2:
                            self.safe_paths.append(sub[0:-1])
                        added = True
                    sub = [x for x in sub[1:len(sub)]]
                    f_in = self.graph.nodes[sub[0][0]]['flow_in']
                    f += (f_in - self.graph.edges[first]['capacity'])
        if timer:
            end = timer()
            self.times['safety'] = end-start
        return self.safe_paths

    def flow_decomposition(self, timer=False):
        '''
        flow_decomposition(self)->list of paths
        Calculates a flow decomposition for the graph.
        Returns list of paths as list of edges.
        '''
        if timer:
            start = timer()
        v = self.s
        min_flow = float('inf')
        path = []
        copy_of_graph = self.graph.copy()

        cap = copy_of_graph.nodes[self.s]['flow_out']
        while(True):
            if v == self.t:
                self.flow_decomposition_paths.append(path)
                rmv = []
                for e in path:
                    copy_of_graph.edges[e]['capacity'] -= min_flow
                    if copy_of_graph.edges[e]['capacity'] == 0:
                        rmv.append(e)
                copy_of_graph.remove_edges_from(rmv)
                path = []
                cap -= min_flow
                min_flow = float('inf')
                v = self.s
                if cap == 0:
                    break
            else:
                next = list(copy_of_graph.successors(v))[0]
                if copy_of_graph.edges[v, next]['capacity'] < min_flow:
                    min_flow = copy_of_graph.edges[v, next]['capacity']
                path.append((v, next))
                v = next
        if timer:
            end = timer()
            self.times['decomposition'] = end-start
        return self.flow_decomposition_paths
    
    def get_decomposition_time(self):
        '''
        Return time used to compute decomposition of the graph.
        Returns 0 if timer-parameter wasn't used and time wasn't measured
        '''
        return self.times['decomposition']

    def get_safety_time(self):
        '''
        Return time used to compute safety of the graph.
        Returns 0 if timer-parameter wasn't used and time wasn't measured
        '''
        return self.times['safety']

    def print(self):
        print(self)
    
    def safe_paths_to_string(self):
        '''
        safe_paths_to_string(self) -> string edgelist of the paths generated by safety algorithm
        '''
        str = ''
        for path in self.safe_paths:
            for (i,edge) in enumerate(path):
                str += f'{edge[0]} '
                if i == len(path)-1:
                    str += f'{edge[1]}\n'
        return str

    def __str__(self):
        return (f'source: {self.s}\n'
                f'sink: {self.t}\n'
                f'graph: {list(self.graph.edges(data=True))}\n'
                f'nodes: {list(self.graph.nodes(data=True))}\n'
                f'flow decomposition: \n'
                + "\n".join(str(x) for x in self.flow_decomposition_paths) + "\n" +
                f'maximum safe paths:\n'
                + "\n".join(str(x) for x in self.safe_paths))
