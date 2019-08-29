import random, numpy, math, copy, matplotlib.pyplot as plt
from scipy.spatial.distance import pdist,squareform
import json 

class data_loader:

        def __init__(self,_path):
                self.cities=[]
                print(_path)
                with open(_path) as json_file:
                        self.data=json.load(json_file)
                for f in self.data['features']:
                        self.cities.append(f['geometry']['coordinates'])
                self.n_cities=len(self.cities)
                self.tour = random.sample(range(self.n_cities),self.n_cities)

        def draw_nodes(self):
                return self.data

        def draw_path(self,tour):
                geo_json=[]
                for u,v in zip(tour,tour[1:]):
                        line_string = {
                                'type': 'Feature',
                                'properties':{
                                        'source':self.data['features'][u]['properties']['NOMBRE'],
                                        'target':self.data['features'][v]['properties']['NOMBRE']
                                },
                                'geometry':{
                                        'type':'LineString',
                                        'coordinates': [ self.data['features'][u]['geometry']['coordinates'],self.data['features'][v]['geometry']['coordinates'] ]
                                }   
                        }
                        geo_json.append(line_string)
                geometries = {
                        'type': 'FeatureCollection',
                        'features': geo_json,
                }
                geo_str = json.dumps(geometries)
                return geo_str

        def exponential_decay(self,init_temperature,step):
                return init_temperature*math.exp(-float(step)/float(1e5))

        def fast_decay(self,init_temperature,step):
                return float(init_temperature)/float(1+step%1e2)
        
        def log_decay(self,init_temperature,step):
                return float(init_temperature)/math.log(1+step**2)
                
        def solver(self):
                dist_mat=squareform(pdist(self.cities,'euclidean'))
                tour_dist= lambda tour : sum([dist_mat[i,j] for i,j in zip(tour,tour[1:])])
                fitness=tour_dist(self.tour)                  
                maxsteps=int(1e6)
                step=1
                while step<maxsteps:
                        temperature=self.exponential_decay(1,step)
                        [i,j] = sorted(random.sample(range(self.n_cities),2))
                        newTour =  self.tour[:i] + self.tour[j:j+1] + self.tour[i+1:j] + self.tour[i:i+1] + self.tour[j+1:]
                        delta_y=tour_dist(newTour)-fitness
                        eval_fit= 0 if temperature == 0 else -delta_y/temperature
                        if  delta_y<0 or math.exp(eval_fit)>random.random() :
                                self.tour = copy.copy(newTour)
                                fitness=tour_dist(newTour)
                        step=step+1
                        yield self.tour,temperature,fitness