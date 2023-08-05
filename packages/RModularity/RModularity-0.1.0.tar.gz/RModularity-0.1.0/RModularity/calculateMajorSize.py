
import benchmarkParameters as bp
import utilities as ut
import importlib
import numpy as np
from multiprocessing import Process, Manager, Pool
import multiprocessing
import json
from tqdm.auto import tqdm
import pandas as pd
importlib.reload(ut)
import matplotlib.gridspec as gridspec
from adjustText import adjust_text;
import matplotlib
#Disable Matplotlib interface
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rc('font', family='sans-serif')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rc('axes', labelsize=16)
plt.rc('legend', fontsize=14)

variant = "SBMBasic"
rewireMode = "basic"
alphaPoints = 51
alphaValues = np.linspace(0,1.0,alphaPoints);
networkList = ut.getNetworkList()
trivialThreshold = 1.0

majorSizesByNetwork = {}

with open("../Data/majorSizes_%s.json"%rewireMode,"rt") as fd:
    majorSizesByNetwork = json.load(fd)

networkList = [(networkName,label,category) for networkName,label,category in networkList if networkName not in majorSizesByNetwork]

num_processors = multiprocessing.cpu_count()

# print('will use processors = ', str(num_processors))

# print('starting at', dt_string)
def processForAlpha(parameters):
    alpha,networkName = parameters
    majorForAlpha = []
    try:
        for perturbationIndex in range(bp.perturbationRealizations):
            g = ut.getPerturbedNetwork(networkName,rewireMode,alpha,perturbationIndex)
            majorForAlpha.append(g.clusters(mode="WEAK").giant().vcount())
            # data = ut.loadDistributionData("NC","%s_%s"%(rewireMode,variant),networkName)
            # data = ut.loadDistributionData("NC","%s_%s"%(rewireMode,variant),networkName)
            # data = ut.loadDistributionData("NC","%s_%s"%(rewireMode,variant),networkName)
    except OSError:
        print("Problem with %s"%networkName)
    return majorForAlpha

pool = Pool(processes=num_processors)

for entry in tqdm(networkList,leave=False):
    networkName,label,category  =  entry
    majorSizes = []
    majorSizesByNetwork[networkName] = majorSizes
    for majorForAlpha in tqdm(pool.imap(func=processForAlpha, iterable=[(alpha,networkName) for alpha in alphaValues]), total=len(alphaValues),leave=False):
        if(majorForAlpha):
            majorSizes.append(majorForAlpha)
        else:
            del majorSizesByNetwork[networkName]
            break
    with open("../Data/majorSizes_%s_NEW.json"%rewireMode,"wt") as fd:
        json.dump(majorSizesByNetwork,fd)


with open("../Data/majorSizes_%s.json"%rewireMode,"wt") as fd:
    json.dump(majorSizesByNetwork,fd)


pool.close()
pool.terminate()



