import numpy as np

endpoints = []
video_sizes = []
cache_list = []
score = np.array([])
capacity = 0
E = 0
V = 0
C = 0

def import_data(file_name):
	# input data: based on line 1 read following lines

	no_videos = 0
	no_endpoints = 0
	no_caches = 0

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

	return no_endpoints, no_caches, no_videos, video_sizes

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
		
		
def fill_score(score):
	for e, endpoint in enumerate(endpoints):
		for v, video in enumerate(endpoint["videos"]):
			for c, cache in enumerate(endpoint["cache"]):
				score[e, v, c] = get_score(video, video_sizes[v], cache, endpoint["data"])
				print get_score(video, video_sizes[v], cache, endpoint["data"])

def get_score(requests, video_size, cache, data_latency):
	if requests == 0 or cache == 0:
		return 0

	latency_improvement = data_latency - cache

	return (requests * latency_improvement) / video_size

def try_best_greedy(score, video_sizes):
	flat_score = score.flatten()

	# while True:
		print "hier"
		index = np.argmax(flat_score)

		# endpoint video cache
		e, v, c = np.unravel_index(index, score.shape)

		if cache_list[c].add_video(video_sizes, v):
			update_score(v, c)

			highest_score = flat_score[index]
			return highest_score

		flat_score[index] = 0
		score[e, v, c] = 0

def update_score(v, cache):
	for endpoint in cache_list[cache]:
		if endpoint["videos"][v]:
			e = endpoint["index"]
			improvement = score[e, v, cache] 

			for c in range(C):
				if score[e, v, c]:
					score[e, v, c] -= improvement

def output_result():
	out = open("output.txt", "w")

	counter = 0
	for cache in cache_list:
		if cache.video_list:
			counter += 1

	out.write(str(counter) + "\n")

	for c, cache in enumerate(cache_list):
		out.write(str(c) + " ")
		
		out.write(cache.video_list.join(" "))

		out.write("\n")

	out.close()

def do_simple_greedy():

	E, V, C, video_sizes = import_data("me_at_the_zoo.in")

	score = np.zeros((E, V, C))

	for _ in range(C):
		cache_list.append(Cache(capacity))

	# Prepare score-space
	fill_score(score)

	# Perform algorithm
	try_best_greedy(score, video_sizes)


	output_result()


do_simple_greedy()