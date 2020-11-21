from collections import Counter
from itertools import islice
from preprocess import *

class Window:
	def __init__(self, sequences,  min_sup, min_len, max_len):
		
		min_sup = len(sequences) * min_sup
		
		freq_seqs = self._find_patterns(sequences, min_sup, min_len, max_len)
		
		self.frequentSeqs = Window.FreqSequences(freq_seqs) 
	
	def FrequentSequences(self):
		return self.frequentSeqs
		
	@staticmethod
	def train(sequences,  min_sup = 0.005 , min_len = 1, max_len = 10):
		return Window(sequences,  min_sup , min_len, max_len)
		
	class FreqSequences:
		def __init__(self, fs):
			self.fs = fs
		def collect(self):
			return self.fs
			
	class Pattern:
		def __init__(self, seq, freq):
			self.sequence = seq
			self.frequence = freq
			
	def _window(self, sequence, n=1):
		it = iter(sequence)
		result = tuple(islice(it, n))
		if len(result) == n:
		    yield result    
		for elem in it:
		    result = result[1:] + (elem,)
		    yield result

	def _find_patterns(self, sequences, min_sup, min_size, max_size):
		
		counter = Counter()
		patterns = []
		
		for size in range(min_size, max_size + 1):						
			for itin in sequences:
				counted = []
				for w in self._window(itin, size):
					if w not in counted:
						counted.append(w)
						counter.update([w])
			
		for route, count in counter.most_common():
			if count >= min_sup:
				patterns.append( Window.Pattern(route, count) )
		
		return patterns


if __name__ == '__main__':
	r = Routes.start('data/sorted_labelled_photo_unixtime.csv')
	r.process()
	itin_list = r.itineraries.values()
	itin_list = [list(itin) for itin in itin_list]
	model = Window.train(itin_list, min_sup = 0.005)
	seqs = model.FrequentSequences().collect()
	with open('output_w.csv', 'wb') as out:
		for fs in seqs:
			out.write('{}: {}'.format(list(fs.sequence), fs.frequence))
			out.write('\n')
	
