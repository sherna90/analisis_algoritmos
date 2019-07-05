import json
import heapq
import numpy as np
from math import radians, cos, sin, asin, sqrt
from collections import deque

class abstract_graph:
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges} | {v for u,v in self.edges}
    
    def adjacency_list(self):
        pass

    def depth_first(self, start):
        path, stack = [], deque()
        stack.append(start)
        L = self.adjacency_list()
        while stack:
            vertex = stack.pop()
            if vertex not in path:
                path.append(vertex)
                stack.extend(L[vertex] - set(path))
        return path

    def breadth_first(self, start):
        path, queue = [], deque()
        queue.append(start)
        L = self.adjacency_list()
        while queue:
            vertex = queue.popleft()
            if vertex not in path:
                path.append(vertex)
                queue.extend(L[vertex] - set(path))
        return path
        
class simple_graph(abstract_graph):
    
    def adjacency_matrix(self):
        n=len(self.nodes)
        mat=np.zeros((n,n))
        for i,v in enumerate(self.nodes):
            for j,k in enumerate(self.nodes):
                if (v,k) in self.edges:
                    mat[i,j]=1
                    mat[j,i]=1
        return mat
    
    def adjacency_list(self):
        adjacent=lambda n : {v for u,v in self.edges if u==n } | {u for u,v in self.edges if v==n}
        return {v:adjacent(v) for v in self.nodes}

class simple_digraph(abstract_graph):
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges if u!=None} | {v for u,v in self.edges if v!=None}
        
    def adjacency_matrix(self):
        n=len(self.nodes)
        mat=np.zeros((n,n))
        for i,v in enumerate(self.nodes):
            for j,k in enumerate(self.nodes):
                if (v,k) in self.edges:
                    mat[i,j]=1
        return mat

    def adjacency_list(self):
        adjacent=lambda n : {v for u,v in self.edges if u==n and v!=None} 
        return {v:adjacent(v) for v in self.nodes} 
    
    def in_degree(self):
        degree= lambda n : len({u for u,v in self.edges if v==n and u!=None})
        return {v:degree(v) for v in self.nodes}
        
    def google_matrix(self,alpha=0.85):
        n=len(self.nodes)
        E=np.ones((n,n))/float(n)
        A=self.adjacency_matrix()
        row_sums = A.sum(axis=1)
        A[row_sums==0,:]=1/float(n)
        row_sums[row_sums==0]=1
        W = A / row_sums[:, np.newaxis]
        W_star=alpha*W+(1-alpha)*E
        return W_star

class weighted_graph(simple_digraph):
    
    def __init__(self,_edges):
        self.edges=_edges
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        
    
    def adjacency_list(self):
        adjacent=lambda n : {v:self.edges[(u,v)] for u,v in self.edges.keys() if u==n }
        return {v:adjacent(v) for v in self.nodes}

    def dijkstra(self,start):
        L = self.adjacency_list()
        U = {start:start}
        D = {v:float('inf') for v in self.nodes}
        D.update(L[start])
        D.update({start:0})
        PQ = []
        heapq.heappush(PQ,(start,0))
        for neighbor,cost in L[start].iteritems():
            heapq.heappush(PQ,(neighbor,cost))
        while len(PQ)>0:
            node,node_cost=heapq.heappop(PQ)
            for neighbor,neighbor_cost in L[node].iteritems():
                new_cost=node_cost+neighbor_cost
                if D[neighbor]>(new_cost):
                    D.update({neighbor:new_cost})
                    heapq.heappush(PQ,(neighbor,new_cost))
                U.update({neighbor:node})
        return D,U

    def shortest_path(self,parent,start,end):
        path=[end]
        k=end
        while k!=start:
            path.append(parent[k])
            k=parent[k]
        return path
        
class json_graph(weighted_graph):

    def __init__(self,_path):
        with open(_path) as file:
            self.data=json.load(file)
        self.edges={ (int(e['source']),int(e['target'])):float(e['length']) for e in self.data['links']}
        self.nodes={u for u,v in self.edges.keys()} | {v for u,v in self.edges.keys()}
        self.nodes_location={int(n['id']):(float(n['y']),float(n['x'])) for n in self.data['nodes']}
    
    def draw_graph(self):
        coords_from_edge = lambda e : [ [float(w) for w in u.split()] for u in e['geometry'].split(' ',1)[1].encode('latin-1').replace('(','').replace(')','').split(',')]
        geo_json=[]
        for e in self.data['links']:
            if 'geometry' in e:
                line_string = {
                    'type': 'Feature',
                    'properties':{
                        'length':e['length'],
                        'source':e['source'],
                        'target':e['target']
                    },
                    'geometry':{
                        'type':'LineString',
                        'coordinates': coords_from_edge(e)
                    }   
                }
                geo_json.append(line_string)
            else:
                if int(e['source']) in self.nodes_location and int(e['target']) in self.nodes_location:
                    node_s=self.nodes_location[int(e['source'])]
                    node_t=self.nodes_location[int(e['target'])]
                    line_string = {
                        'type': 'Feature',
                        'properties':{
                            'length':e['length'],
                            'source':e['source'],
                            'target':e['target']
                        },
                        'geometry':{
                            'type':'LineString',
                            'coordinates': [[node_s[1],node_s[0]],[node_t[1],node_t[0]]]
                        }   
                    }
                    geo_json.append(line_string)
        geometries = {
            'type': 'FeatureCollection',
            'features': geo_json,
        }
        geo_str = json.dumps(geometries)
        return geo_str

    def draw_nodes(self):
        geo_json=[]
        for n,pos in self.nodes_location.iteritems():
            line_string = {
                'type': 'Feature',
                'properties':{
                    'name':str(n)
                },
                'geometry':{
                    'type':'Point',
                    'coordinates': [pos[1],pos[0]]
                    }   
                }
            geo_json.append(line_string)
        geometries = {
            'type': 'FeatureCollection',
            'features': geo_json,
        }
        geo_str = json.dumps(geometries)
        return geo_str


class full_graph(weighted_graph):

    def __init__(self,_path):
        with open(_path) as file:
            self.data=json.load(file)
        self.nodes_location={int(n['id']):(float(n['y']),float(n['x'])) for n in self.data['nodes']}
        self.nodes=set(self.nodes_location.keys())
        distance = lambda u,v : self.haversine(
            self.nodes_location[u][1],
            self.nodes_location[u][0],
            self.nodes_location[v][1],
            self.nodes_location[v][0])
        sorted=list(self.nodes) 
        #self.edges={(u,v):distance(u,v) for u in self.nodes for v in self.nodes if u!=v}
        self.edges={}
        i=1
        for u in sorted:
            for v in sorted[i:]:
                self.edges.update({(u,v):distance(u,v)})
            i+=1
            
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

