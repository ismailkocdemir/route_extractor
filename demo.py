from frequentroutes import prefixspan2 as ps2 
from frequentroutes import prefixspan as ps 
from frequentroutes import tester as t
from frequentroutes import decomposer as d

def runPS2():
	print('prefixspan2 running...')
	input_path = 'sorted_labelled_photo_unixtime.csv'
	output_path = 'out_ps2.txt'
	csv_path = 'frequent_routes.csv'
	itins =	ps2.PrefixSpan2.collectItinsFrom(input_path)
	model = ps2.PrefixSpan2.train(itins.getItinsAsList(), itins.getDestinations())
	sequences = model.freqSequences().collect()
	first_seq = sequences[0].sequence
	first_freq = sequences[0].freq 
	model.freqSequences().writeFrequenciesTo(output_path)
	print('  frequencies written to : ' + output_path )
	model.freqSequences().toCSV(csv_path)
	print('  csv result written to : ' + str(csv_path))

def runPS():
	print('prefixspan running...')
	input_path = 'sorted_labelled_photo_unixtime.csv'
	output_path = 'out_ps.txt'
	itins = ps.PrefixSpan.collectItinsFrom(input_path)
	itins = ps.PrefixSpan.toList(itins)
	model = ps.PrefixSpan.train(itins)
	model.freqSequences().writeTo(output_path)
	print('  frequencies written to : ' + str(output_path) )

def runTester():
	print('tester running...')
	ps2_output_path = 'out_ps2.txt'  
	result = t.checkEquality( ps2_output_path) # Returns 1 if equal to expected result, 0 if not equal, -1 if path does not exist.
	print ('  result : ' + str(result))

def runDecomposer():
	print('decomposer running...')
	input_path = 'sorted_labelled_photo_unixtime.csv'
	output_path = 'decomposed.csv'
	d.extractAndDecompose(input_path, output_path)
	print('  result written to : ' + str(output_path) )

if __name__ == "__main__":
	runPS() 
	#runPS2()
	#runTester()
	#runDecomposer()
