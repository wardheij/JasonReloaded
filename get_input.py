import numpy as np

def import_data(file_name):
	# input data: based on line 1 read following lines

	no_videos = 0
	no_endpoints = 0
	no_caches = 0
	endpoints = []

	with open(file_name) as f:

	    # number-of videos, endpoints, descriptions, servers, capacity
	    variables = list(map(int, f.readline().split(' ')))

	    video_sizes = list(map(int, f.readline().split(' ')))

	    no_videos = variables[0]
	    no_endpoints = variables[1]
	    no_caches = variables[3]
	    capacity = variables[4]

	    endpoints = [{} for _ in range(no_endpoints)]

	    # loop over all endpoints and get their caches latencies
	    for i in range(no_endpoints):

	        # grab line
	        line = list(map(int, f.readline().split(' ')))

	        # endpoint latency
	        latency = line[0]

	        endpoints[i]["data"] = latency

	        # number of caches
	        no_caches_end = line[1]

	        cache_latencies = np.zeros(no_caches)

	        # append empty array for requests per video
	        endpoints[i]["videos"] = np.zeros(no_videos)

	        # find all caches
	        for _ in range(no_caches_end):
	            cache = f.readline()
	            cache = cache.split(' ')

	            # append as a dict for cache no : cache latency
	            cache_latencies[int(cache[0])] = int(cache[1])

	        # append cache latencies
	        endpoints[i]["cache"] = cache_latencies

	    # after we've seen all endpoints
	    for i in range(no_videos):
	        video_line = f.readline()
	        video_line = video_line.split(' ')
	        video_line = map(int, video_line)
	        video_id, endpoint, no_requests = video_line
	        endpoints[endpoint]["videos"][video_id] = no_requests

	return no_endpoints, no_videos, no_caches, video_sizes, capacity, endpoints

class Cache(object):
	def __init__(self, size):
		self.size = size
		self.content = 0
		self.video_list = []
		self.endpoint_list = []

	def add_video(self, video_sizes, v):
		if self.content + video_sizes[v] <= self.size:
			self.video_list.append(v)
			self.content += video_sizes[v]
			return 1
		return 0

	def add_endpoint(self, endpoint):
		self.endpoint_list.append(endpoint)
		
		
def fill_score(score, endpoints, video_sizes):
	for e, endpoint in enumerate(endpoints):
		for v, video in enumerate(endpoint["videos"]):
			for c, cache in enumerate(endpoint["cache"]):
				score[e, v, c] = get_score(video, video_sizes[v], cache, endpoint["data"])

def get_score(requests, video_size, cache, data_latency):
	if requests == 0 or cache == 0:
		return 0

	latency_improvement = data_latency - cache

	return (requests * latency_improvement) / video_size

def try_best_greedy(score, video_sizes, cache_list, endpoints, C):
	flat_score = score.flatten()

	i = 0
	while i < 100:
		i += 1
		index = np.argmax(flat_score)

		# endpoint video cache
		e, v, c = np.unravel_index(index, score.shape)

		if cache_list[c].add_video(video_sizes, v):
			update_score(v, c, cache_list, endpoints, score, C)

			highest_score = flat_score[index]
			return highest_score

		flat_score[index] = 0
		score[e, v, c] = 0

def update_score(v, cache, cache_list, endpoints, score, C):
	for e in cache_list[cache].endpoint_list:
		if endpoints[e]["videos"][v]:
			improvement = score[e, v, cache] 

			for c in range(C):
				if score[e, v, c]:
					score[e, v, c] -= improvement

def output_result(cache_list):
	out = open("output.txt", "w")

	counter = 0
	for cache in cache_list:
		if cache.video_list:
			counter += 1

	out.write(str(counter) + "\n")

	for c, cache in enumerate(cache_list):
		if cache.video_list:
			out.write(str(c) + " ")
			
			for vid in cache.video_list:
				out.write(str(vid) + " ")

			out.write("\n")

	out.close()

def do_simple_greedy():
	cache_list = []

	E, V, C, video_sizes, capacity, endpoints = import_data("me_at_the_zoo.in")

	score = np.zeros((E, V, C))

	for _ in range(C):
		cache_list.append(Cache(capacity))

	for index, e in enumerate(endpoints):
		for c, caches in enumerate(e["cache"]):
			if caches:
				cache_list[c].add_endpoint(index)

	# Prepare score-space
	fill_score(score, endpoints, video_sizes)

	# Perform algorithm
	for _ in range(100):
		try_best_greedy(score, video_sizes, cache_list, endpoints, C)


	output_result(cache_list)


do_simple_greedy()