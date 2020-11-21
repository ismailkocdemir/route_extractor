from prefixspan2 import PrefixSpan2 as ps2			
from prefixspan import PrefixSpan as ps
from collections import defaultdict
import time
import csv

def stringsearch(pattern, text):
	# A naive method to find substring.
	m = len(pattern)
	n = len(text)

	if m > n :
		return 0

	lst = []
	for i in range( n-m+1):
		j = 0
		for _ in range( m ):
			if pattern[j] != text[i+j]:
				break
			j+=1
		if j==m:
			lst.append(i)
	return lst


def lps_efc(pattern, m): 
	# Original version. Finds longest prefix which is also suffix. 
	lps = [0] * m
	j = 0
	i = 1
	while i < m:
		if pattern[i] == pattern[j]:
			j+=1
			lps[i] = j
			i+=1
		else:
			if j == 0:
				lps[i]
				i +=1
			else:
				j = lps[j-1]
	return lps

def lps_naive(pattern, m): 
	# Finds longest prefix which is also suffix. Wrote down without any clue from the original algorithm. Slower.
	lps = [0] * m		   

	for i in range(1, m):
		pre = i-1
		suf = i
		while pre >= 0:
			if pattern[pre] == pattern[suf]:
				if pre == 0:
					break
				pre -= 1
				suf -= 1
			else:
				pre -= 1
				suf = i
		if pre == 0:
			lps[i] = i - suf + 1
	return lps

def kmp(pattern, text):   
	# KMP substring search.
	m = len(pattern)
	n = len(text)

	if m > n:
		return 0

	lps = lps_efc(pattern, m)

	occurences = []
	mismatch = 0
	for i in range( n-m+1):
		j = lps[mismatch - 1]
		while j<m:
			if pattern[j] != text[i+j]:
				break
			j+=1
		if j==m:
			occurences.append(i)
		mismatch = j

	return occurences

def extractAndDecompose(in_path, out_path = 'decomposed.csv', min_sup = 0.005, max_length = 10, consecutive = True):

	if consecutive:	
		# Uses modified PrefixSpan
		itins_dests = ps2.collectItinsFrom(in_path)
		itins = itins_dests.getItinsAsList()
		dests = itins_dests.getDestinations() 
		itin_list = [ item[0] for item in itins]
		model = ps2.train(itins, dests, min_sup, max_length)
	else:
		# Uses original PrefixSpan																												
		itins = ps.collectItinsFrom(in_path) 										
		itin_list = ps2.toList(itins)
		model = ps.train(itin_list, min_sup, max_length)		
	
	freqseqs = model.freqSequences().collect()
	seq_freq = []
	for itin in itin_list:
		itin_decomp = []
		itin_len = len(itin)
		for fs in freqseqs:
			seq = fs.sequence
			if len(seq) <= itin_len:		
				itin_decomp.append((fs, kmp(seq, itin)))
		seq_freq.append(itin_decomp)	

	
	with open(out_path, 'w') as out:
		fieldnames = ['itinerary','sequence', 'total_frequency', 'occurrence_indexes']
		writer = csv.DictWriter(out, fieldnames = fieldnames)
		i = 0
		for itin in itin_list:
			for item in seq_freq[i]:
				if len(item[1]) > 0:
					writer.writerow( {'itinerary':itin, 'sequence': item[0].sequence, 'total_frequency': item[0].freq, 'occurrence_indexes': item[1] }  )
			i += 1


if __name__ == "__main__":
	extractAndDecompose('sorted_labelled_photo_unixtime.csv')
