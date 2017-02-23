import numpy as np

score = np.zeros((E, V, C))

class Cache(object):
	def __init__(self, size):
		self.size = size
		self.content = 0
		self.video_list = []
		self.endpoint_list = []

	def add_video(self, v):
		if self.content + video[v] <= self.size:
			self.video_list.append(v)
			self.content += video[v]
			return 1
		return 0

	def add_endpoint(self, endpoint):
		self.endpoint_list.append(endpoint)
		
		
def fill_score():
	for e, endpoint in enumerate(endpoints):
		for v, video in enumerate(endpoint["videos"]):
			for c, cache enumerate(endpoint["cache"]):
				score[e, v, c] = get_score(video, cache, endpoint["data"])

def get_score(video, cache, data_latency):
	if video == 0 or cache == 0:
		return 0

	requests, video_size = video

	latency_improvement = data_latency - cache

	return (requests * latency_improvement) / video_size

def try_best_greedy():
	flat_score = score.flatten()
	
	while True:
		index = np.argmax(flat_score)

		# endpoint video cache
		e, v, c = np.unravel_index(index, score.shape())

		if cache_list[c].add_video(v):
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


	fill_score()


	while try_best_greedy():

		pass

	output_result()


do_simple_greedy()