import csv
from math import cos, sin, asin, sqrt, radians

class Routes():

	def __init__(self, path):
			self.file_path = path
			self.itineraries = {} 						# {userid : (route)} 
			self.users = [] 						# [ user_id ]
			self.avg_distance = 0.0
			self.min_distance = [float('inf'), 0]	# [distance in m, index]
			self.max_distance = [0.0, 0]			# [distance in m, index]
			self.destinations = {} 					# { poi_name: lon-lat }

	
	@staticmethod
	def start(path):
		return Routes(path)
	
	def removeUnderscore(self, long, lat):
	
		if lat[0] == '_':
			lat = float(lat[1:])
		else:
			lat = float(lat)

		if long[0] == '_':
			long = float(long[1:])
		else:
			long = float(long)
		return long, lat
			
	# calculate distance in km
	def haversine_dist(self, lat, long, plat, plong):
	
		long, lat = self.removeUnderscore(long, lat)
		plong, plat = self.removeUnderscore(plong, plat)
		
		lat, long, plat, plong = map(radians, [lat, long, plat, plong])
		dlat = lat - plat
		dlong = long - plong
		a = sin(dlat/2)**2 + cos(lat) * cos(plat) * sin(dlong/2)**2
		c = 2 * asin(sqrt(a)) 
		r = 6371 
	
		return c * r
	
	def calculate_distances(self):
		with open(self.file_path, ) as dataset:
			fields = ['unixtime', 'photo_id', 'user_id', 'publish_time', 'creation_time', 'lat', 'long', 'poi_name', 'poi_lat', 'poi_long']
			reader = csv.DictReader(dataset, fieldnames = fields)
			dist_sum = 0
			length = 0
			for row in reader: 
				distance = self.haversine_dist(row['lat'], row['long'], row['poi_lat'], row['poi_long'])
				length += 1
				dist_sum += distance
				if distance < self.min_distance[0]:
					self.min_distance[0] = distance
					self.min_distance[1] = length 
				if distance > self.max_distance[0]:
					self.max_distance[0] = distance
					self.max_distance[1] = length
			
			self.max_distance[0] *= 1000 
			self.min_distance[0] *= 1000
			self.avg_distance = 1000*dist_sum/length	
			return self.avg_distance, self.max_distance, self.min_distance
			
			
	def process(self, distance_treshold = float('inf')):
	
		with open(self.file_path) as dataset:
			fields = ['unixtime', 'photo_id', 'user_id', 'publish_time', 'creation_time', 'lat', 'long', 'poi_name', 'poi_lat', 'poi_long']
			reader = csv.DictReader(dataset, fieldnames = fields)
			route = []	
			prev_poi = 'nowhere'
			new_user = False
			first = True
			# dictionary / userid : (route) /
			
			for row in reader:
				new_user = False
				distance = self.haversine_dist(row['lat'], row['long'], row['poi_lat'], row['poi_long'])
				if first:
					self.users.append(row['user_id'])
					first = False
				
				if row['poi_name'] not in self.destinations:
					self.destinations[row['poi_name']] = self.removeUnderscore(row['long'], row['lat']) 
			
				if row['user_id'] != self.users[-1]:
					self.itineraries[self.users[-1]] = tuple(route)
					route = []
					self.users.append(row['user_id'])
					new_user = True
		
				if (row['poi_name'] != prev_poi or new_user) and distance*1000.0 < distance_treshold:
					prev_poi = row['poi_name']
					route.append( prev_poi ) 
						


if __name__ == "__main__":
	r = Routes.start('data/sorted_labelled_photo_unixtime.csv')
	print( r.calculate_distances() )	
	r.process()
	for name, crdnt in r.destinations.iteritems():
		print(name, crdnt)



