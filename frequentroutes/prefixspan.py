#author: Tianming Lu
#adapted by: Ismail H. Kocdemir

from preprocess import *
import time

class PrefixSpan:

	def __init__(self, sequences, minSupport, maxPatternLength):

		minSupport = minSupport * len(sequences)
		
		freqSequences = self._prefixSpan(
			self.SequencePattern([], None, maxPatternLength), 
			sequences, minSupport, maxPatternLength)
		
		self.duplicates = False
		self.freqSeqs = PrefixSpan.FreqSequences(freqSequences, self)

	@staticmethod
	def train(sequences, minSupport = 0.005, maxPatternLength = 10):
		return PrefixSpan(sequences, minSupport, maxPatternLength)
	
	@staticmethod
	def remove_duplicates(freqPatterns):		
		for pat in freqPatterns:
			newSeq = []
			isMultiple = True
			isFirst = True
		 	prev = 'none'
		 	for poi in pat.sequence:
				if poi != prev:
					if isFirst == False:
						isMultiple = False
					else:
						isFirst = False
					newSeq.append(poi)
					prev = poi
			
			if len(newSeq) == 1 and isMultiple and len(pat.sequence) > 1:
				freqPatterns[freqPatterns.index(pat)] = None
			else: 	
				pat.sequence = newSeq
		return [x for x in freqPatterns if x is not None]
			
	
	@staticmethod
	def collectItinsFrom(read_path):
		r = Routes(read_path)
		r.process()
		return r.itineraries
	
	@staticmethod
	def toList(itins):
		itin_list = itins.values()
		return [list(itin) for itin in itin_list]
		
	def keepDuplicates():
		self.duplicates = True
	

	def freqSequences(self):
		return self.freqSeqs

	class FreqSequences:
		def __init__(self, fs, outer):
			self.fs = fs
			self.outer = outer
		def collect(self):
			if self.outer.duplicates:
				return self.fs
			else:
				return PrefixSpan.remove_duplicates(self.fs)
		def writeTo(self, path):
			sorted_result = sorted(self.fs, key = lambda o: o.freq, reverse=True)
			with open(path, 'w') as out:
				for fs in sorted_result:
					out.write('{}: {}\n'.format(fs.sequence, fs.freq))
			
				
	class SequencePattern:
		def __init__(self, sequence, support, maxPatternLength):
			self.sequence = []
			for s in sequence:
				self.sequence.append(s)
			self.freq = support

		def append(self, p):
			self.sequence.extend(p.sequence)
			if self.freq is None:
				self.freq = p.freq
			self.freq = min(self.freq, p.freq)


	def _checkPatternLengths(self,pattern, maxPatternLength):
		if len(pattern.sequence)>maxPatternLength:
			return False
		return True


	def _prefixSpan(self,pattern, S, threshold, maxPatternLength):
		patterns = []
		
		if self._checkPatternLengths(pattern, maxPatternLength):
			f_list = self._frequent_items(S, threshold, maxPatternLength)
			for i in f_list:
				p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength)
				p.append(i)
				if self._checkPatternLengths(pattern, maxPatternLength):
					patterns.append(p)
				p_S = self._build_projected_database(S, p)
				p_patterns = self._prefixSpan(p, p_S, threshold, maxPatternLength)
				patterns.extend(p_patterns)

		return patterns


	def _frequent_items(self, S, threshold, maxPatternLength):

		items = {}
		f_list = []
		if S is None or len(S) == 0:
			return []
			
		for s in S:	
			counted = []
			for item in s:
				if item not in counted:
					counted.append(item)
					if item in items:
						items[item] += 1
					else:
						items[item] = 1
	
		for k, v in items.iteritems():
			if v>= threshold:
				f_list.append( self.SequencePattern([k], v, maxPatternLength) )		
				
		f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]
		
		sorted_list = sorted(f_list, key=lambda p: p.freq)
		return sorted_list


	def _build_projected_database(self, S, pattern):
		p_S = []
		last_item = pattern.sequence[-1]
		for s in S:
			p_s = []
			for element in s:
				if last_item != element:
					continue
				e_index = s.index(element)
				p_s = s[e_index + 1:]
				break
				
			if len(p_s) != 0:
				p_S.append(p_s)

		return p_S



if __name__ == "__main__":
	itins = PrefixSpan.collectItinsFrom('sorted_labelled_photo_unixtime.csv')
	itins = PrefixSpan.toList(itins)
	start = time.time()
	model = PrefixSpan.train(itins)
	elapsed = time.time() - start
	print('ps elapsed', elapsed)
	model.freqSequences().writeTo()


	
