from window import *
from preprocess import *


def checkEquality( output_ps2 = 'out_ps2.txt', min_sup = 0.005):
	r = Routes.start('sorted_labelled_photo_unixtime.csv')
	r.process()
	itin_list = r.itineraries.values()
	itin_list = [list(itin) for itin in itin_list]
	model = Window.train(itin_list, min_sup)
	seqs = model.FrequentSequences().collect()
	with open('output_window.txt', 'wb') as out:
		for fs in seqs:
			out.write('{}: {}'.format(list(fs.sequence), fs.frequence))
			out.write('\n')
	equal = 1
	try:
		with open('output_window.txt') as w, open(output_ps2) as ps2:
			wlines = set(w.readlines())
			ps2lines = set(ps2.readlines())
			
			if wlines != ps2lines:
				equal = 0
	except IOError:
		equal = -1
	
	return equal

if __name__ == "__main__":
	checkEquality()
