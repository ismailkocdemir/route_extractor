#author: Tianming Lu
#adapted by: Ismail H. Kocdemir

from preprocess import Routes as r
import time
import csv


class Itineraries:
		def __init__(self, itins, dests):
			self.itins = itins
			self.dests = dests
		def getItins(self):
			return self.itins
		def getItinsAsList(self):
			itin_list = self.itins.values()
			return [[list(itin_list[i]), i] for i in range(len(itin_list))]
		def getDestinations(self):
			return self.dests

class PrefixSpan2:

	def __init__(self, sequences, destinations, minSupport, maxPatternLength):

		minSupport = minSupport * len(sequences)

		freqSequences = self._prefixSpan2(
			self.SequencePattern([], None, maxPatternLength), 
			sequences, minSupport, maxPatternLength)
		self.freqSeqs = PrefixSpan2.FreqSequences(freqSequences, destinations)

	@staticmethod
	def train(sequences, destinations, minSupport = 0.005, maxPatternLength = 10):
		return PrefixSpan2(sequences, destinations, minSupport, maxPatternLength)

	
	@staticmethod
	def collectItinsFrom(read_path):
		rt = r.start(read_path)
		rt.process()
		return Itineraries(rt.itineraries, rt.destinations)
	
	def freqSequences(self):
		return self.freqSeqs

	class FreqSequences:
		def __init__(self, fs, dests):
			self.fs = fs
			self.dests = dests
		def collect(self):
			return self.fs
		def writeFrequenciesTo(self, write_path = 'output_ps2.txt'):
			sorted_result = sorted(self.fs, key = lambda obj: obj.freq, reverse = True)
			with open(write_path, 'w') as out:
				for fs in sorted_result:
					out.write('{}: {}\n'.format(fs.sequence, fs.freq))
					
		def toCSV(self, write_path = 'frequent_itineraries.csv'):
			with open(write_path, 'w') as out:
				writer = csv.DictWriter(out, ['itin_id', 'long', 'lat', 'index', 'name', 'freq'])
				itin_id = 0
				for seq in self.fs:
					if len(seq.sequence) > 1:
						index = 0
						for poi in seq.sequence:
							writer.writerow({'itin_id' : itin_id,  'long' : self.dests[poi][0], 'lat':self.dests[poi][1], 'index': index, 'name': poi, 'freq':seq.freq})	
							index += 1
						itin_id += 1 			


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


	def _prefixSpan2(self,pattern, S, threshold, maxPatternLength):
		patterns = []
		
		if self._checkPatternLengths(pattern, maxPatternLength):
			f_list = self._frequent_items(S, threshold, maxPatternLength, (len(pattern.sequence) == 0))
			for i in f_list:
				p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength)
				p.append(i)
				if self._checkPatternLengths(pattern, maxPatternLength):
					patterns.append(p)
				p_S = self._build_projected_database(S, p, (len(p.sequence)==1))

				p_patterns = self._prefixSpan2(p, p_S, threshold, maxPatternLength)
				patterns.extend(p_patterns)

		return patterns


	def _frequent_items(self, S, threshold, maxPatternLength, firstIter):

		items = {}
		f_list = []
		if S is None or len(S) == 0:
			return []
		
		if firstIter:
			for s in S:
				counted = []
				for item in s[0]:
					if item not in counted:
						counted.append(item)
						if item in items:
							items[item].append(s[1])
						else:
							items[item] = [s[1]]
		else:
			for s in S:
				if s[0][0] in items:
					items[s[0][0]].append(s[1])
				else:
					items[s[0][0]] = [s[1]]
							
							
		for k, v in items.iteritems():
			freq = len(set(v))
			if freq >= threshold:
				f_list.append( self.SequencePattern([k], freq, maxPatternLength) )		
				
		f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]
		sorted_list = sorted(f_list, key=lambda p: p.freq)
		return sorted_list


	def _build_projected_database(self, S, pattern, firstIter):
		p_S = []
		last_item = pattern.sequence[-1]
		for s in S:
			for i in range( len(s[0])):
				element = s[0][i]
				if last_item != element:
					if firstIter:
						continue
					else:
						break
				p_s = [[], s[1]]
				p_s[0] = s[0][i + 1:]
				if len(p_s[0]) != 0:
					p_S.append(p_s)
				if(firstIter == False):
					break
		return p_S



if __name__ == "__main__":
	itins =	PrefixSpan2.collectItinsFrom('sorted_labelled_photo_unixtime.csv')
	model = PrefixSpan2.train(itins.getItinsAsList(), itins.getDestinations())
	model.freqSequences().writeFrequenciesTo()
	model.freqSequences().toCSV()

