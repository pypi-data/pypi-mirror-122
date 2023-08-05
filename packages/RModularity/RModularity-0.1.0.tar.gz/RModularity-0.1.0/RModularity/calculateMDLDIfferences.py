
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
import xnet as xn
importlib.reload(ut)
import matplotlib.gridspec as gridspec
from adjustText import adjust_text;
import matplotlib
#Disable Matplotlib interface
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patheffects
import igraph as ig

import graph_tool as gt;
import graph_tool.inference as gtInference;

importlib.reload(ut)


matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rc('font', family='sans-serif')
# plt.rc('text', usetex=True)
plt.rc('xtick', labelsize=15)
plt.rc('ytick', labelsize=15)
plt.rc('axes', labelsize=16)
plt.rc('legend', fontsize=14)


def SBMMinimizeAndEntropy(gigraph,degreeCorrected=True):
    vertexCount = gigraph.vcount()
    directed = gigraph.is_directed()
    edges = gigraph.get_edgelist()    
    g = gt.Graph(directed=directed);
    for _ in range(0,vertexCount):
        g.add_vertex();
    for edge in edges:
        g.add_edge(edge[0],edge[1]);
    state = gtInference.minimize.minimize_blockmodel_dl(g,deg_corr=degreeCorrected);
    S1 = state.entropy();
    S2 = 0
    if("Community" in gigraph.vertex_attributes()):
        membershipProperty = g.new_vertex_property("int64_t")
        membershipProperty.a = [int(a) for a in gigraph.vs["Community"]]
        # S3 = gtInference.blockmodel.BlockState(g,B=1).entropy()
        S2 = gtInference.blockmodel.BlockState(g,b=membershipProperty,deg_corr=degreeCorrected).entropy()
    S3 = gtInference.blockmodel.BlockState(g,B=1,deg_corr=degreeCorrected).entropy()
    return (S1,S2,S3);

muValues = bp.muValues

for k in bp.ks:
    for nodesCount in bp.nodesCounts:
        benchmarkNames = [];
        S1s = []
        S2s = []
        S3s = []
        for networkRealization in range(bp.networkRealizations):
            for tau1 in bp.t1Values:
                for tau2 in bp.t2Values:
                    for mu in tqdm(muValues):
                        networkName = (bp.getNetworkName(mu,networkRealization,tau1,tau2,k=k,nodesCount=nodesCount),"$\\mu=%.3f$, $N=%d$, $k=%d$"%(mu,nodesCount,k),"Benchmarks_t1-%.2f_t2-%.2f"%(tau1,tau2))[0];
                        g = ut.getNetwork(networkName)
                        S1,S2,S3 = SBMMinimizeAndEntropy(g)
                        S1s.append(S1)
                        S2s.append(S2)
                        S3s.append(S3)


        fig = plt.figure()

        plt.plot(muValues,S1s,label="SBM")
        plt.plot(muValues,S2s,label="Planted")
        plt.plot(muValues,S3s,label="Single")

        plt.legend()
        plt.xlabel("$\mu$")
        plt.ylabel("MDL")
        plt.tight_layout()
        plt.savefig("../Figures/MDL_benchmarks_New-DC_N%d_k%d.pdf"%(nodesCount,k))
        plt.close()

        fig = plt.figure()
        plt.plot(muValues,-(np.array(S1s)-np.array(S3s))/np.array(S3s))
        # plt.legend()
        plt.xlabel("$\mu$")
        plt.ylabel("MDL Norm. Diff")
        plt.tight_layout()
        plt.savefig("../Figures/Norm_MDL_benchmarks_New-DC_N%d_k%d.pdf"%(nodesCount,k))
        plt.close()

        # print(SBMMinimizeAndEntropy(g))



gnS1s = []
gnS2s = []
gnS3s = []
for networkRealization in range(bp.networkRealizations):
    for mu in tqdm(gn.muValues):
        # benchmarkNames.append(gn.getNetworkName(gn.P_in,P_out,networkRealization));
        networkName = (gn.getNetworkName(gn.nodesCount,gn.communitiesCount,gn.avgk,mu,networkRealization),"$\\mu=%.3f$"%mu,"GN")[0]
        g = ut.getNetwork(networkName)
        g.vs["Community"] = [i%gn.communitiesCount for i in range(g.vcount())]
        S1,S2,S3 = SBMMinimizeAndEntropy(g)
        gnS1s.append(S1)
        gnS2s.append(S2)
        gnS3s.append(S3)


fig = plt.figure()

plt.plot(gn.muValues,gnS1s,label="SBM")
plt.plot(gn.muValues,gnS2s,label="Planted")
plt.plot(gn.muValues,gnS3s,label="Single")

plt.legend()
plt.xlabel("$\mu$")
plt.ylabel("MDL")
plt.tight_layout()
plt.savefig("../Figures/MDL_GN-DC.pdf")
plt.close()


fig = plt.figure()
plt.plot(muValues,-(np.array(gnS1s)-np.array(gnS3s))/np.array(gnS3s))
# plt.legend()
plt.xlabel("$\mu$")
plt.ylabel("MDL Norm. Diff")
plt.tight_layout()
plt.savefig("../Figures/Norm_MDL_GN-DC.pdf")
plt.close()


# networkName = (gn.getNetworkName(gn.nodesCount,gn.communitiesCount,gn.avgk,0.1,networkRealization),"$\\mu=%.3f$"%mu,"GN")[0]
# g = ut.getNetwork(networkName)
# g.vs["Community"] = [i%gn.communitiesCount for i in range(g.vcount())]
# xn.igraph2xnet(g,"test.xnet")




selectedNetworks = {
    # "soc-advogato",
    # "bio-dmela",
    # "OClinks_w",
    # "ia-fb-messages",
    # "fb-pages-public-figure",
    # "socfb-nips-ego",
    # "RVOR",
    # "mammalia-voles-kcs-trapping",
    # "tech-routers-rf",
    # "econ-orani678",
    # "socfb-Oberlin44",
    # "econ-poli",
    # "Airports",
    # "bio-yeast-protein-inter",
    # "power-eris1176",
    # "Facebook_combined",
    # "fb-pages-politician",
    # "web-EPA",
    # "ca-Erdos992"
    # "bio-CE-HT",
    # "mammalia-voles-rob-trapping",
    # "road-euroroad",
    # "USairport_2010",
    # "bio-yeast-protein-inter",
    # "netscience",
    # "Facebook_combined",
    # "fb-pages-politician",
    # "ca-Erdos992",
    # "tech-WHOIS",
    # "bio-CE-HT",
    # "mammalia-voles-rob-trapping",
    # "bio-dmela",
    # "bio-WormNet-v3-benchmark",
    # "road-euroroad",
    # "WesternUS_PowerGrid",
    # "Airports",
    # "power-eris1176",
    # "econ-poli",
    # "netscience",
    # "tech-WHOIS",
    # "econ-orani678",
    # "ca-Erdos992",
    # "ia-fb-messages",
    # "facebook_combined",
    # "bio-DR-CX",
    "CA-HepPh",
}

def SBMMinimizeMembership(gigraph,degreeCorrected=True):
    vertexCount = gigraph.vcount()
    directed = gigraph.is_directed()
    edges = gigraph.get_edgelist()    
    g = gt.Graph(directed=directed);
    for _ in range(0,vertexCount):
        g.add_vertex();
    for edge in edges:
        g.add_edge(edge[0],edge[1]);
    state = gtInference.minimize.minimize_blockmodel_dl(g,deg_corr=degreeCorrected);
    return list(state.get_blocks());

for networkName in selectedNetworks:
    g = xn.xnet2igraph("../Data/Networks/%s.xnet"%networkName)
    membership = SBMMinimizeMembership(g)
    g.vs["SBM Membership"] = [str(entry) for entry in membership]
    xn.igraph2xnet(g,"../Data/SelectedNetworks/%s.xnet"%networkName)
