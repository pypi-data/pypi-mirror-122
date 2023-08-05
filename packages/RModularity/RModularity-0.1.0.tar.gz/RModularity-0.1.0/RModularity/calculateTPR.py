import benchmarkParameters as bp
import createGNNetworks as gn
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
from matplotlib import patheffects
import igraph as ig


matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rc('font', family='sans-serif')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rc('axes', labelsize=16)
plt.rc('legend', fontsize=14)

categoriesInOrder = [
 'Biological',
 'Transport-Geographic',
 'Information',
 'Social',
 'Benchmarks_t1-2.00_t2-1.00',
 'GN',
 'Models'
]

variant = "SBMBasic"
rewireMode = "basic"
alphaPoints = 51
alphaValues = np.linspace(0,1.0,alphaPoints);
networkList = ut.getNetworkList()
trivialThreshold = 1.0

with open("../Data/networkProperties.json","rt") as fd:
    networkProperties = json.load(fd)

with open("../Data/majorSizes_%s.json"%rewireMode,"rt") as fd:
    majorSizesByNetwork = json.load(fd)

for entry in tqdm(networkList,leave=False):
    networkName,label,category  =  entry
    majorSizes = []
    communitySizes = ut.loadDistributionData("CS","%s_%s"%(rewireMode,variant),networkName)
    numberOfCommunities = ut.loadDistributionData("NC","%s_%s"%(rewireMode,variant),networkName)
    if(communitySizes is None or numberOfCommunities is None or networkName not in networkProperties):
        continue;
    verticesCount = networkProperties[networkName]["Node count"]
    majorCommunitySizes = [];
    errorMajorCommunitySizes = [];
    trivialRatios = [];
    for alphaIndex in range(len(numberOfCommunities)):
        communityIndices = np.cumsum(numberOfCommunities[alphaIndex]);
        majorCommunitySizesDistrib=[];
        errorMajorCommunitySizesDistrib=[];
        trivialCount = 0;
        for i in range(len(communityIndices)):
            if(i>0):
                startIndex = int(communityIndices[i-1]);
            else:
                startIndex=0;
            endIndex = int(communityIndices[i]);
            if(networkName in majorSizesByNetwork):
                trivialMax = majorSizesByNetwork[networkName][alphaIndex][i]
            else:
                trivialMax = verticesCount
            # assert (trivialMax<=verticesCount)
                
            communitySizesDistrib = communitySizes[alphaIndex][startIndex:endIndex];
            majorCommunitySizesDistrib.append(np.max(communitySizesDistrib));
            trivialThresholdSize = trivialThreshold*trivialMax;
            if(np.max(communitySizesDistrib)>=trivialThresholdSize):
                trivialCount+=1;
            elif(len(communitySizesDistrib)>=trivialThresholdSize):
                trivialCount+=1;
        trivialRatios.append(trivialCount/len(communityIndices));
    networkProperties[networkName]["TPR Data"] = trivialRatios;
    networkProperties[networkName]["TPR Area"] = (1.0-np.trapz(trivialRatios, alphaValues))




df = pd.DataFrame.from_dict(networkProperties).T
df["Category"] = df["Category"].replace("Economy","Information") #merged economy and Information
# fig, ax = plt.subplots(1, 1, figsize=(9, 9))

df["Modularity Diff"] = df["Modularity"] - df["ERModularity"]
df["ModularityCPM Diff"] = df["ModularityCPM"] - df["ERModularityCPM"]
df["ModularityRBER Diff"] = df["ModularityRBER"] - df["ERModularityRBER"]
df["ModularitySignificance Diff"] = df["ModularitySignificance"] - df["ERModularitySignificance"]
df["ModularitySurprise Diff"] = df["ModularitySurprise"] - df["ERModularitySurprise"]


df["Modularity Config Diff"] = df["Modularity"] - df["ConfigModularity"]
df["ModularityCPM Config Diff"] = df["ModularityCPM"] - df["ConfigModularityCPM"]
df["ModularityRBER Config Diff"] = df["ModularityRBER"] - df["ConfigModularityRBER"]
df["ModularitySignificance Config Diff"] = df["ModularitySignificance"] - df["ConfigModularitySignificance"]
df["ModularitySurprise Config Diff"] = df["ModularitySurprise"] - df["ConfigModularitySurprise"]


df["Modularity Z-Score"] = (df["Modularity"] - df["ConfigModularityAverage"])/df["ConfigModularityStd"]

df["MDL-DC Diff. By Sum."] = (df["MDL-DC SBM"] - df["MDL-DC Single"]) / (df["MDL-DC SBM"] + df["MDL-DC Single"])
df["MDL-DC One Minus Ratio"] = 1.0 - df["MDL-DC Ratio"]
df["MDL-DC Ratio"] = 1.0/df["MDL-DC Ratio"]
# df["Modularity Norm"] = df["Modularity Diff"]/df["Modularity"]
# df["ModularityCPM Norm"] = df["ModularityCPM Diff"]/df["ModularityCPM"]
# df["ModularityRBER Norm"] = df["ModularityRBER Diff"]/df["ModularityRBER"]
# df["ModularitySignificance Norm"] = df["ModularitySignificance Diff"]/df["ModularitySignificance"]
# df["ModularitySurprise Norm"] = df["ModularitySurprise Diff"]/df["ModularitySurprise"]


fig = plt.figure(figsize=(9, 9))
ax = fig.gca()
cmap = matplotlib.cm.tab10
grouped = df.groupby('Category')
for index,(key, group) in enumerate(grouped):
    group.plot.scatter(x="Modularity",y="TPR Area",
    color=cmap(index),
    ax=ax,
    label=key,
    s=30)\
        .legend(loc='center left',bbox_to_anchor=(1.0, 0.5))

fig.savefig("../Figures/AllTPR_%s.pdf"%rewireMode)
plt.close(fig)


fig, ax = plt.subplots(1, 1, figsize=(9, 9))
cmap = matplotlib.cm.tab10
grouped = df.groupby('Category')
for index,(key, group) in enumerate(grouped):
    group.plot.scatter(x="Average degree",y="TPR Area",color=cmap(index),ax=ax,label=key)

ax.set_xscale("log")
fig.savefig("../Figures/AllTPRvsAvgDegree_%s.pdf"%rewireMode)
plt.close(fig)


fig, ax = plt.subplots(1, 1, figsize=(9, 9))
cmap = matplotlib.cm.tab10
grouped = df.groupby('Category')
for index,(key, group) in enumerate(grouped):
    group.plot.scatter(x="Node count",y="TPR Area",color=cmap(index),ax=ax,label=key)

ax.set_xscale("log")
fig.savefig("../Figures/AllTPRvsSize_%s.pdf"%rewireMode)
plt.close(fig)


dforig = df



from scipy import stats
# firstProperty = "MDL-DC Ratio"
# firstProperty = "MDL-DC One Minus Ratio"
# firstProperty = "TPR Area"
firstProperty = "Modularity Config Diff"
# firstProperty = "Modularity"
useRanks = False

removeNetworks = set([
    # "bench_n5000_t2.000_T1.000_mu0.700_minc20_maxc500_k20.000_maxk250-r0",
    # "bench_n5000_t2.000_T1.000_mu0.800_minc20_maxc500_k20.000_maxk250-r0",
    # "bench_n5000_t2.000_T1.000_mu0.900_minc20_maxc500_k20.000_maxk250-r0",
    # "bench_n5000_t2.000_T1.000_mu1.000_minc20_maxc500_k20.000_maxk250-r0"
    ])

df = dforig[~dforig.index.isin(removeNetworks)].dropna().copy()
# df["MDL-DC Diff. Norm."] = -df["MDL-DC Diff. Norm."]
for secondProperty in [
    "MDL-DC Diff. Norm.",
    "MDL-nonDC Diff. Norm.",
    "MDL-DC Diff. By Sum.",
    # "MDL-nonDC Diff. Norm.Avg.",
    "Average degree",
    "Node count",
    "Edges count",
    "Modularity",
    # "ModularityCPM",
    # "ModularityRBER",
    # "ModularitySignificance",
    # "ModularitySurprise",
    "Modularity Diff",
    "Modularity Config Diff",
    "Modularity Z-Score",
    "MDL-DC Ratio",
    "MDL-DC One Minus Ratio",
    "TPR Area",
    # "ModularityCPM Diff.",
    # "ModularityRBER Diff.",
    # "ModularitySignificance Diff.",
    # "ModularitySurprise Diff."
    ]:
    fig, ax = plt.subplots(1, 1, figsize=(9, 9))
    cmap = matplotlib.cm.tab10
    # secondProperty = "TPR Area"
    if(useRanks):
        df[firstProperty+" Ranks"] = df[firstProperty].rank(ascending=False)
        df[secondProperty+" Ranks"] = df[secondProperty].rank(ascending=False)
        firstPropertyFinal = firstProperty+" Ranks"
        secondPropertyFinal = secondProperty+" Ranks"
    else:
        firstPropertyFinal = firstProperty
        secondPropertyFinal = secondProperty
    grouped = df.groupby('Category')
    groupedDictionary = {key: group for key, group in grouped}

    for index,key in enumerate(categoriesInOrder):
        group = groupedDictionary[key]
        # group.plot.scatter(x=firstProperty,y=secondProperty,color=cmap(index),ax=ax,label=key)
        if (key.startswith("Benchmarks") or key == "GN"):
            ax.plot(group[firstPropertyFinal],group[secondPropertyFinal],color=cmap(index),lw=2)
        ax.scatter(group[firstPropertyFinal],group[secondPropertyFinal],label=key,color=cmap(index))

    for label,x,y in zip(df["Label"],df[firstPropertyFinal],df[secondPropertyFinal]):
        if(np.isfinite(x)):
            ax.text(x,y,label,fontsize=6)
    # ax.scatter(group[firstPropertyFinal],group[secondPropertyFinal],label=key,color=cmap(index))
    ax.set_xlabel(firstPropertyFinal)
    ax.set_ylabel(secondPropertyFinal) 
    ax.legend(prop={'size': 6})
    spearmanCoeff = stats.spearmanr(df.dropna()[firstPropertyFinal].dropna(),df.dropna()[secondPropertyFinal]).correlation
    pearsonCoeff = stats.pearsonr(df.dropna()[firstPropertyFinal].dropna(),df.dropna()[secondPropertyFinal])[0]
    ax.set_title("Corr.= %.2f , Spearman: %.2f"%(pearsonCoeff,spearmanCoeff))
    
    print("Spearman: %s x %s: %f"%(firstPropertyFinal,secondPropertyFinal,stats.spearmanr(df.dropna()[firstPropertyFinal].dropna(),df.dropna()[secondPropertyFinal]).correlation))
    print("Pearson: %s x %s: %f"%(firstPropertyFinal,secondPropertyFinal,stats.pearsonr(df.dropna()[firstPropertyFinal].dropna(),df.dropna()[secondPropertyFinal])[0]))
    # ax.set_xscale("log")
    fig.savefig("../Figures/All_%s_%s_vs_%s_.pdf"%(rewireMode,firstPropertyFinal,secondPropertyFinal))
    plt.close(fig)







fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10,3.5),sharey="all")
benchmarkNames = [];
networkRealization = 0
tau1 = 2.0
tau2 = 1.0
vmin = np.min(bp.muValues)
vmax = np.max(bp.muValues)
cmap=matplotlib.cm.plasma

norm = matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)
for mu in bp.muValues:
    networkName = bp.getNetworkName(mu,networkRealization,tau1,tau2)
    # "$\\mu=%.3f$"%mu
    if("TPR Data" in networkProperties[networkName]):
        trivialRatios = networkProperties[networkName]["TPR Data"]
        ax1.plot(alphaValues,trivialRatios,color = cmap(norm(mu)),label = "$\\mu=%.2f$"%mu)

ax1.legend(fontsize="small",frameon=False)
ax1.set_xlabel("$\\alpha$")
ax1.set_ylabel("TPR")
ax1.text(-0.15, -0.15,'a LFR',
     horizontalalignment='left',
     verticalalignment='center',
     transform = ax1.transAxes,
     path_effects=[patheffects.withStroke(linewidth=3,foreground="w")])

vmin = np.min(gn.muValues)
vmax = np.max(gn.muValues)
norm = matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)
for mu in gn.muValues:
    networkName = gn.getNetworkName(gn.nodesCount,gn.communitiesCount,gn.avgk,mu,networkRealization)
    # "$\\mu=%.3f$"%mu
    if("TPR Data" in networkProperties[networkName]):
        trivialRatios = networkProperties[networkName]["TPR Data"]
        ax2.plot(alphaValues,trivialRatios,color = cmap(norm(mu)),label = "$\\mu=%.2f$"%mu)
ax2.legend(fontsize="small",frameon=False)
ax2.set_xlabel("$\\alpha$")
# ax2.set_ylabel("TPR")


ax2.text(-0.15, -0.15,'b SBM',
     horizontalalignment='left',
     verticalalignment='center',
     transform = ax2.transAxes,
     path_effects=[patheffects.withStroke(linewidth=3,foreground="w")])

plt.tight_layout()
fig.savefig("../Figures/TPR_Benchmarks_%s.pdf"%rewireMode)
plt.close(fig)


# for networkRealization in range(bp.networkRealizations):
#     for mu in gn.muValues:
#         # benchmarkNames.append(gn.getNetworkName(gn.P_in,P_out,networkRealization));
#         benchmarkNames.append((gn.getNetworkName(gn.nodesCount,gn.communitiesCount,gn.avgk,mu,networkRealization),"$\\mu=%.3f$"%mu,"GN"));



# alphaPoints = 51
# alphaValues = np.linspace(0,1.0,alphaPoints);

# networkName = bp.getNetworkName(0.8,networkRealization,tau1,tau2)
# sizes = []
# for alpha in alphaValues[-20:]:
#     for perturbationIndex in range(bp.perturbationRealizations):
#         g = ut.getPerturbedNetwork(networkName,rewireMode,alpha,perturbationIndex)
#         majorSize = g.clusters().giant().vcount()
#         mcs = np.max(list(Counter(g.vs["basic_SBMBasic"]).values()))
#         tpr = mcs/majorSize
#         sizes.append(tpr)
#         if(tpr<1.0):
#             break;
#     if(tpr<1.0):
#         break;
#     print("%g : %.2f ± %.2f"%(alpha,np.average(sizes),np.std(sizes)))
    




# def SBMMinimizeMembership(vertexCount,edges,directed=False):
# 	g = gt.Graph(directed=directed);
# 	for _ in range(0,vertexCount):
# 		g.add_vertex();
		
# 	for edge in edges:
# 		g.add_edge(edge[0],edge[1]);
# 	state = gtInference.minimize.minimize_blockmodel_dl(g,deg_corr=True);
# 	S2 = state.entropy();
# 	B2 = state.get_Be();
# 	return (list(state.get_blocks()),S2,B2);



# networkName = bp.getNetworkName(0.1,networkRealization,tau1,tau2)
# originalNetwork = ut.getPerturbedNetwork(networkName,rewireMode,0.0,perturbationIndex)

# originalNetwork = originalNetwork.simplify().clusters(mode="WEAK").giant()

# for alpha in [0.0]:
#     originalEdges = [(edge.source, edge.target) for edge in originalNetwork.es];
#     vertexCount = originalNetwork.vcount();
#     degrees = originalNetwork.degree();
#     directed = originalNetwork.is_directed()
#     edgesCount = len(originalEdges);
#     newEdges = np.array(originalEdges);
#     selectedEdgesIndices = np.where(np.random.random(edgesCount)<alpha)[0];
#     # plt.figure()
#     # plt.hist(selectedEdgesIndices)
#     # plt.savefig("tests/%s_TEST_Alpha_%.2f_hist.pdf"%(networkName,alpha))
#     # plt.close()
#     generatedSelectedEdges = np.array(np.random.randint(0,vertexCount,(len(selectedEdgesIndices),2)));
#     newEdges[selectedEdgesIndices] = generatedSelectedEdges;
#     newEdges = [(fromIndex,toIndex) for fromIndex,toIndex in newEdges];
#     perturbedNetwork = ig.Graph(n=vertexCount,edges=list(newEdges),directed=False);
#     membership,_,_ = SBMMinimizeMembership(vertexCount,newEdges)
#     perturbedNetwork.vs["SBMBasic"] = [str(entry) for entry in membership]
#     xn.igraph2xnet(perturbedNetwork,"tests/%s_TEST_Alpha_%.2f.xnet"%(networkName,alpha)) 

# networkName = "bio-CE-HT"
# print(networkProperties[networkName]["Node count"])
# print(networkProperties[networkName]["Average degree"])
# print(networkProperties[networkName]["TPR Area"])

# counts =[]
# degrees = []
# tpr = []
# for networkName,data in networkProperties.items():
#     if(networkName.startswith("socfb")):
#         if("TPR Area" in data):
#             counts.append(data["Node count"])
#             degrees.append(data["Average degree"])
#             tpr.append(data["TPR Area"])

# print("socfb")
# print(np.average(counts),"±",np.std(counts))
# print(np.average(degrees),"±",np.std(degrees))
# print(np.average(tpr),"±",np.std(tpr))


import matplotlib.patches as mpl_patches
import pandas as pd


for networkName in networkProperties.keys():
    data = networkProperties[networkName]
    if("TPR Data" not in data):
        print("Skipping %s ..."%networkName)
        continue
    fig = plt.figure(figsize=(3*1.61803398875,3))
    ax = plt.axes((0.2, 0.2, 0.70, 0.70), facecolor='w')
    nodeCount = data["Node count"]
    averageDegree = data["Average degree"]
    TPRArea = data["TPR Area"]
    trivialRatios = data["TPR Data"]
    ax.plot(alphaValues,trivialRatios,color = "#262626",lw=2.0)
    ax.fill_between(alphaValues,trivialRatios,1,color = "#E8EAEA")
    ax.set_xlabel("$\\alpha$")
    ax.set_ylabel("TPR")
    ax.set_title(networkName)
    ax.set_xlim(-0.00,1.02)
    ax.set_ylim(-0.020,1.020)
    
    # create a list with two empty handles (or more if needed)
    handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                    lw=0, alpha=0)] * 3

    # create the corresponding number of labels (= the text you want to display)
    labels = []
    labels.append("$N$ = %d"%nodeCount)
    labels.append("$\\langle k\\rangle$ = %.2f"%averageDegree)
    labels.append("$Q_{r}$ = %.2f"%TPRArea)

    # create the legend, supressing the blank space of the empty line symbol and the
    # padding between symbol and label by setting handlelenght and handletextpad
    ax.legend(handles, labels, loc='best', 
            fancybox=False, framealpha=0, 
            handlelength=0, handletextpad=0)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    for axis in ['bottom','left']:
        ax.spines[axis].set_linewidth(1.5)
    ax.tick_params(width=1.5)
    fig.savefig("../Figures/all/TPR_%s_%s.pdf"%(rewireMode,networkName))
    plt.close(fig)





fig = plt.figure(figsize=(3*1.61803398875,3))
ax = plt.axes((0.2, 0.2, 0.70, 0.70), facecolor='w')
socfbNodeCounts = []
socfbAverageDegrees = []
socfbTPRAreas = []
for networkName,data in networkProperties.items():
    #only network names starting with socfb are interesting
    if(not (networkName.startswith("socfb") and ("TPR Data" in networkProperties[networkName]))):
        print("Skipping %s ..."%networkName)
        continue
    if(networkName=="socfb-nips-ego"): #ego network
        continue
    socfbNodeCounts.append(data["Node count"])
    socfbAverageDegrees.append(data["Average degree"])
    socfbTPRAreas.append(data["TPR Area"])
    trivialRatios = data["TPR Data"]
    
    ax.plot(alphaValues,trivialRatios,color = "#262626",lw=2.0,alpha=0.3)
    ax.fill_between(alphaValues,trivialRatios,1,color = "#E8EAEA",alpha=0.3,ec="face",lw=2.0)
ax.set_xlabel("$\\alpha$")
ax.set_ylabel("TPR")
ax.set_title("All socfb")
ax.set_xlim(-0.00,1.02)
ax.set_ylim(-0.020,1.020)

# create a list with two empty handles (or more if needed)
handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                lw=0, alpha=0)] * 3

# create the corresponding number of labels (= the text you want to display)
labels = []
labels.append("$N$ = %d $\\pm$ %d"%(np.mean(socfbNodeCounts),np.std(socfbNodeCounts)))
labels.append("$\\langle k\\rangle$ = %.2f $\\pm$ %.2f"%(np.mean(socfbAverageDegrees),np.std(socfbAverageDegrees)))
labels.append("$Area_{\\mathrm{TPR}}$  %.2f $\\pm$ %.2f"%(np.mean(socfbTPRAreas),np.std(socfbTPRAreas)))

    # create the legend, supressing the blank space of the empty line symbol and the
    # padding between symbol and label by setting handlelenght and handletextpad
ax.legend(handles, labels, loc='best', 
        fancybox=False, framealpha=0, 
        handlelength=0, handletextpad=0)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
for axis in ['bottom','left']:
    ax.spines[axis].set_linewidth(1.5)
ax.tick_params(width=1.5)
fig.savefig("../Figures/all/TPR_%s_All_socfb.pdf"%(rewireMode))
plt.close(fig)



import matplotlib.patches as mpl_patches

allCategoriesData = {
 'Benchmarks_t1-2.00_t2-1.00':{'name': "LFR", "data":[]},
 'Biological':{'name': "Biological", "data":[]},
 'GN':{'name': "SBM", "data":[]},
 'Information/Economy':{'name': "Information_Economy", "data":[]},
 'Models':{'name': "Models", "data":[]},
 'Social':{'name': "Social", "data":[]},
 'Transport-Geographic':{'name': "Transport-Geographic", "data":[]},
 }
allCategoriesData["Economy"] = allCategoriesData["Information/Economy"]
allCategoriesData["Information"] = allCategoriesData["Information/Economy"]
import math

networkPropertiesByCategory = {}
for networkName,data in networkProperties.items():
    #Remove Hybrid R = 0.001 N = 1000   
    if(networkName=="hybrid-r-0.001-n-1000"):
        continue;
    if("TPR Data" in data):
        allCategoriesData[data["Category"]]["data"].append(networkName)

borders = 0.75
spacing = 0.75
scale = 1.5
goldenRatio = (1+math.sqrt(5))/2
columnsCount = 6

for category,categoryData in allCategoriesData.items():

    networkNames = categoryData["data"]
    networkCount = len(networkNames)
    rowsCount = math.ceil(networkCount/columnsCount)
    totalWidth = scale*goldenRatio*columnsCount+spacing*(columnsCount-1)+borders*2
    totalHeight = scale*rowsCount+spacing*(rowsCount-1)+borders*2
    fig,axes = plt.subplots(rowsCount,columnsCount,
        figsize=(
            totalWidth,
            totalHeight
            ),
    sharey="row",sharex="col",
    gridspec_kw={
    "wspace":spacing/totalWidth*(columnsCount-1),
    "hspace":spacing/totalHeight*(rowsCount-1),
    "left":borders/totalWidth,
    "right":1.0-borders/totalWidth,
    "top":1.0-borders/totalHeight,
    "bottom":borders/totalHeight,
    })
    tableData = {
        "Network":[],
        "N":[],
        "$\\langle k\\rangle$":[],
        "$Q_r$":[],
    }
    for i in range(columnsCount*rowsCount):
        ax = axes[int(i/columnsCount),i%columnsCount]
        ax.axis('off')
    for networkIndex,networkName in enumerate(networkNames):
        data = networkProperties[networkName]
        if("TPR Data" not in data):
            print("Skipping %s ..."%networkName)
            continue
        # ax = plt.axes((0.2, 0.2, 0.70, 0.70), facecolor='w')
        rowIndex = int(networkIndex/columnsCount)
        columnIndex = networkIndex%columnsCount
        nextNetworkIndex = networkIndex+columnsCount
        ax = axes[rowIndex,columnIndex]
        ax.axis('on')
        nodeCount = data["Node count"]
        averageDegree = data["Average degree"]
        TPRArea = data["TPR Area"]
        trivialRatios = data["TPR Data"]
        ax.plot(alphaValues,trivialRatios,color = "#262626",lw=2.0)
        ax.fill_between(alphaValues,trivialRatios,1,color = "#E8EAEA")
        if(rowIndex==(rowsCount-1) or nextNetworkIndex>=networkCount):
            ax.set_xlabel("$\\alpha$")
            ax.tick_params(labelbottom=True)
        if(columnIndex==0):
            ax.set_ylabel("TPR")
        ax.set_title(data["Label"])
        ax.set_xlim(-0.00,1.02)
        ax.set_ylim(-0.020,1.020)
        # create a list with two empty handles (or more if needed)
        handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                        lw=0, alpha=0)] * 3

        # create the corresponding number of labels (= the text you want to display)
        labels = []
        labels.append("$N$ = %d"%nodeCount)
        labels.append("$\\langle k\\rangle$ = %.2f"%averageDegree)
        labels.append("$Q_{r}$ = %.2f"%TPRArea)
        tableData["Network"].append(data["Label"])
        tableData["N"].append(nodeCount)
        tableData["$\\langle k\\rangle$"].append(averageDegree)
        tableData["$Q_r$"].append(TPRArea)
        # create the legend, supressing the blank space of the empty line symbol and the
        # padding between symbol and label by setting handlelenght and handletextpad
        ax.legend(handles, labels, loc='best', 
                fancybox=False, framealpha=0, 
                handlelength=0, handletextpad=0)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        for axis in ['bottom','left']:
            ax.spines[axis].set_linewidth(1.5)
        ax.tick_params(width=1.5)
    pd.DataFrame(tableData) \
    .sort_values("$Q_r$",ascending=False) \
    .to_latex("../Figures/table_TPR_byCategory_%s_%s.tex"%(rewireMode,categoryData["name"]), \
    index=False,
    formatters={
        "$Q_r$": lambda value:"%.2f"%value,
        "$\\langle k\\rangle$": lambda value:"%.1f"%value,
        "N": lambda value:"%d"%value,
    })
    fig.savefig("../Figures/TPR_byCategory_%s_%s.pdf"%(rewireMode,categoryData["name"]))
    plt.close(fig)

