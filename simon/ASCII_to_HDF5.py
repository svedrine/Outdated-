# ASCII --> HDF5 v.2.0

import os, argparse
import h5py
import numpy as np

from gprMax.exceptions import CmdInputError

# Parse command line arguments
parser = argparse.ArgumentParser(description='ASCII --> HDF5 format')
parser.add_argument('filename', help='name of ASCII file including path')
args = parser.parse_args()

filename = args.filename
outputfile = filename.replace('.a.ASC', '.out')



# Open the ASCII file 
f = open(filename, 'r')
mylist = f.readlines()
while '\n' in mylist: mylist.remove('\n')

# Format data
modelruns = np.shape(mylist)[0]
data = []
for row in range(modelruns):
	data.append(list(map(int, mylist[row].split())))

f.close()

# Create an HDF5 ouptut file
fout = h5py.File(outputfile, 'w')

# Write some attributes
iterations = np.size(data[0])
fout.attrs['Modelruns'] =  modelruns
fout.attrs['Iterations'] = iterations

nrx = 1
dx = 6.67e-3
fout.attrs['nrx'] = nrx
fout.attrs['dt'] = 0.018654e-9
fout.attrs['Positions'] = np.linspace(0, 1, modelruns) * (modelruns * dx)


path = '/rxs/rx%s/' % str(nrx)
output = 'Ez'
for model in range(modelruns):
	# Write properties on first iteration
	if model == 0:
		grp = fout.create_group(path)
		grp.create_dataset(output, (iterations, modelruns), dtype='<f4')

	# Write dataset
	fout['%s%s' % (path, output)][:,model] = data[model]
	
fout.close()
























