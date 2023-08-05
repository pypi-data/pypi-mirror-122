import numpy as np
import math;
import benchmarkParameters as bp
import createGNNetworks as gn
import sys
import scipy
import scipy.signal
import os
import adjustText as at
import matplotlib.gridspec as gridspec
from adjustText import adjust_text;
from collections import OrderedDict
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

lineStyles = ['-' , '--' , '-.' , ':','-' , '--' , '-.' , ':'];
lineWidths = [3,3,3,3,1,1,1,1];

styles = [
	("#1f77b4","-"),
	("#ff7f0e","-"),
	("#2ca02c","-"),
	("#d62728","-"),
	("#9467bd","-"),
	("#8c564b","-"),
	("#e377c2","-"),
	("#7f7f7f","-"),
	("#bcbd22","-"),
	("#17becf","-"),
	("#aec7e8","-"),
	("#ffbb78","--"),
	("#98df8a","--"),
	("#ff9896","--"),
	("#c5b0d5","--"),
	("#c49c94","--"),
	("#f7b6d2","--"),
	("#c7c7c7","--"),
	("#dbdb8d","--"),
	("#9edae5","--"),
	("#1f77b4","-."),
	("#ff7f0e","-."),
	("#2ca02c","-."),
	("#d62728","-."),
	("#9467bd","-."),
	("#8c564b","-."),
	("#e377c2","-."),
	("#7f7f7f","-."),
	("#bcbd22","-."),
	("#17becf","-."),
	("#aec7e8","-."),
	("#ffbb78",":"),
	("#98df8a",":"),
	("#ff9896",":"),
	("#c5b0d5",":"),
	("#c49c94",":"),
	("#f7b6d2",":"),
	("#c7c7c7",":"),
	("#dbdb8d",":"),
	("#9edae5",":"),
	("#1f77b4","-"),
	("#ff7f0e","-"),
	("#2ca02c","-"),
	("#d62728","-"),
	("#9467bd","-"),
	("#8c564b","-"),
	("#e377c2","-"),
	("#7f7f7f","-"),
	("#bcbd22","-"),
	("#17becf","-"),
	("#aec7e8","-"),
	("#9467bd","-"),
	("#8c564b","-"),
	("#e377c2","-"),
	("#7f7f7f","-"),
	("#bcbd22","-"),
	("#17becf","-"),
	("#aec7e8","-"),
	("#ffbb78",":"),
	("#98df8a",":"),
	("#ff9896",":"),
	("#c5b0d5",":"),
	("#c49c94",":"),
	("#f7b6d2",":"),
	("#c7c7c7",":"),
	("#dbdb8d",":"),
	("#9edae5",":"),
	("#1f77b4","-"),
	("#ff7f0e","-"),
	("#2ca02c","-"),
	("#d62728","-"),
	("#9467bd","-"),
	("#8c564b","-"),
	("#e377c2","-"),
	("#7f7f7f","-"),
	("#bcbd22","-"),
	("#17becf","-"),
	("#aec7e8","-"),
	("#9467bd","-"),
	("#8c564b","-"),
	("#e377c2","-"),
	("#7f7f7f","-"),
	("#bcbd22","-"),
	("#17becf","-"),
	("#aec7e8","-"),
];

def plotData(ax,measurement,networkName,label,plotIndex):
	try:
		dataArray = np.loadtxt("../Data/Results/pairwise%s_%s_%s.txt"%(measurement,variant,networkName));
	except:
		print("!NOT FOUND: %s"%("../Data/Results/pairwise%s_%s_%s.txt"%(measurement,variant,networkName)));
		return;
	print("FOUND %s"%networkName);
	if(len(dataArray)==0):
		return;
	values = dataArray[:,0];
	errors = dataArray[:,1];
	alphaValues = np.linspace(0,1.0,len(values));
	currentStyle = styles[plotIndex%len(styles)];
	ax.plot(alphaValues,values,color=currentStyle[0],linestyle=currentStyle[1],label=label);
	ax.fill_between(alphaValues,values-errors,values+errors,color=currentStyle[0],alpha=0.2);
	




realNetworkNames = [
	("Airports", "Airports","Transport-Geographic"),
	("BA", "BA","Models"),
	("BA5000k18-P1", "BA k=18 p=1","Models"),
#	("BA5000k18-P2", "BA k=18 p=2","Models"),
#	("BA5000k18-P3", "BA k=18 p=3","Models"),
	("ER", "ER","Models"),
	("GEO", "GEO","Models"),
	("Oldenburg", "Oldenburg","Transport-Geographic"),
	("RVOR", "RVOR","Models"),
	("San Joaquin", "San Joaquin","Transport-Geographic"),
	("VOR", "VOR","Models"),
	("WAX", "WAX","Models"),
	("Wikipedia", "Wikipedia","Information"),
	("CollegeMsg-major", "CollegeMsg-major","Social"),
	("CA-HepTh", "CA-HepTh","Social"),
	("Cit-HepTh", "Cit-HepTh","Information"),
	("Email-Enron", "Email-Enron","Social"),
	("email-Eu-core", "email-Eu-core","Social"),
	("Wiki-Vote-major", "Wiki-Vote-major","Information"),
	("facebook_combined", "Facebook_combined","Social"),
	("soc-sign-bitcoinotc_positive", "soc-sign-bitcoinotc_positive","Social"),
	("CA-GrQc", "CA-GrQc","Social"),
# 	("robertson_1929", "robertson_1929","Social"),
	("USairport_2010", "USairport_2010","Transport-Geographic"),
	# ("kasthuri_graph_v4", "kasthuri_graph_v4"),
	("drosophila_medulla_1", "drosophila_medulla_1","Biological"),
	# ("net2m_2011-05-01", "net2m_2011-05-01"),
	# ("net2m_2010-10-01", "net2m_2010-10-01"),
	# ("net2m_2010-04-01", "net2m_2010-04-01"),
	# ("net2m_2009-06-01", "net2m_2009-06-01"),
	# ("net2m_2008-01-01", "net2m_2008-01-01"),
	# ("net2m_2002-12-01", "net2m_2002-12-01"),
	("roget", "roget","Information"),
	("quakers", "quakers","Social"),
	("LC_multiple", "LC_multiple","Biological"),
	("WesternUS_PowerGrid", "WesternUS_PowerGrid","Transport-Geographic"),
	("Collins", "Collins","Biological"),
	("wikispeedia_paths-and-graph", "wikispeedia_paths-and-graph","Information"),
# 	("soc-sign-bitcoinalpha_negative", "soc-sign-bitcoinalpha_negative","Social"),
	("soc-sign-bitcoinalpha_positive", "soc-sign-bitcoinalpha_positive","Social"),
# 	("soc-sign-bitcoinotc_negative", "soc-sign-bitcoinotc_negative","Social"),
	("CA-HepPh", "CA-HepPh","Social"),
	("ScientometricsAndJInformetrics","ScientometricsAndJInformetrics","Information"),
	("dep_2010_obstr_0.8_leidenalg_dist","dep_2010_obstr_0.8_leidenalg_dist","Social"),
	("wiki_PortugalandBrazil","wiki_PortugalandBrazil","Information"),
	("wiki_MarvelvsDC","wiki_MarvelvsDC","Information"),
	("email","email","Social"),
	("netscience","netscience","Information"),
	("mouse_retina_1","mouse_retina_1","Biological"),
	# ("autobahn","autobahn","Transport-Geographic"),
	("OClinks_w","OClinks_w","Social"),
	("AI_interactions","AI_interactions","Biological"),
	("OF_one-mode_weightedchar_Newman","OF_one-mode_weightedchar_Newman","Social"),
	("CA-heaberlin_dedeo_norm_network","CA-heaberlin_dedeo_norm_network","Biological"),
	("inf-euroroad","inf-euroroad","Transport-Geographic"),
	("road-euroroad","road-euroroad","Transport-Geographic"),
	("ia-crime-moreno","ia-crime-moreno","Information"),
	("rt_voteonedirection","rt_voteonedirection","Social"),
	("bn-mouse-kasthuri_graph_v4","bn-mouse-kasthuri_graph_v4","Biological"),
	("power-1138-bus","power-1138-bus","Transport-Geographic"),
	("bio-CE-GT","bio-CE-GT","Biological"),
	("rt_assad","rt_assad","Social"),
	("bio-CE-HT","bio-CE-HT","Biological"),
	("rt_occupywallstnyc","rt_occupywallstnyc","Social"),
	("rt_obama","rt_obama","Social"),
	("mammalia-voles-plj-trapping","mammalia-voles-plj-trapping","Biological"),
	("mammalia-voles-kcs-trapping","mammalia-voles-kcs-trapping","Biological"),
	("rt_damascus","rt_damascus","Social"),
	("rt_occupy","rt_occupy","Social"),
	("socfb-nips-ego","socfb-nips-ego","Social"),
	("rt_israel","rt_israel","Social"),
	("mammalia-voles-rob-trapping","mammalia-voles-rob-trapping","Biological"),
	("bio-grid-mouse","bio-grid-mouse","Biological"),
	("rt_islam","rt_islam","Social"),
	("rt_tlot","rt_tlot","Social"),
	("rt_lebanon","rt_lebanon","Social"),
	("bio-DM-HT","bio-DM-HT","Biological"),
	("mammalia-voles-bhp-trapping","mammalia-voles-bhp-trapping","Biological"),
	("rt_tcot","rt_tcot","Social"),
	("rt_gop","rt_gop","Social"),
	("power-bcspwr09","power-bcspwr09","Transport-Geographic"),
	("rt_libya","rt_libya","Social"),
	("bio-yeast-protein-inter","bio-yeast-protein-inter","Biological"),
	("rt_oman","rt_oman","Social"),
	("rt_p2","rt_p2","Social"),
	("rt_uae","rt_uae","Social"),
	("econ-mahindas","econ-mahindas","Economy"),
	("rt_gmanews","rt_gmanews","Social"),
	("rt_alwefaq","rt_alwefaq","Social"),
	("ia-email-univ","ia-email-univ","Social"),
	("rt_dash","rt_dash","Social"),
	("rt_onedirection","rt_onedirection","Social"),
	("rt_mittromney","rt_mittromney","Social"),
	("rt_barackobama","rt_barackobama","Social"),
	("econ-poli","econ-poli","Economy"),
	("rt_bahrain","rt_bahrain","Social"),
	("ia-fb-messages","ia-fb-messages","Social"),
	("bio-grid-plant","bio-grid-plant","Biological"),
	("rt_saudi","rt_saudi","Social"),
	("rt_ksa","rt_ksa","Social"),
	("tech-routers-rf","tech-routers-rf","Information"),
	("web-edu","web-edu","Information"),
	("ia-dnc-corecipient","ia-dnc-corecipient","Social"),
	("rt_qatif","rt_qatif","Social"),
	("rt_lolgop","rt_lolgop","Social"),
	("rt_justinbieber","rt_justinbieber","Social"),
	("inf-power","inf-power","Transport-Geographic"),
	("power-US-Grid","power-US-Grid","Transport-Geographic"),
	("ca-Erdos992","ca-Erdos992","Social"),
	("rt_http","rt_http","Social"),
	("ia-reality","ia-reality","Social"),
	("bio-HS-HT","bio-HS-HT","Biological"),
	("web-EPA","web-EPA","Information"),
	("power-eris1176","power-eris1176","Transport-Geographic"),
	("bio-grid-worm","bio-grid-worm","Biological"),
	("bio-SC-LC","bio-SC-LC","Biological"),
	("power-bcspwr10","power-bcspwr10","Transport-Geographic"),
	("soc-hamsterster","soc-hamsterster","Social"),
	("fb-pages-tvshow","fb-pages-tvshow","Social"),
	("bio-SC-GT","bio-SC-GT","Biological"),
	("bio-SC-CC","bio-SC-CC","Biological"),
	("bio-grid-fission-yeast","bio-grid-fission-yeast","Biological"),
	("tech-pgp","tech-pgp","Information"),
	("bio-HS-LC","bio-HS-LC","Biological"),
	("bio-dmela","bio-dmela","Biological"),
	("bio-CE-PG","bio-CE-PG","Biological"),
	("inf-openflights","inf-openflights","Transport-Geographic"),
	("socfb-Simmons81","socfb-Simmons81","Social"),
	("bio-CE-GN","bio-CE-GN","Biological"),
	("soc-advogato","soc-advogato","Social"),
	("web-spam","web-spam","Information"),
# 	("ia-escorts-dynamic","ia-escorts-dynamic","Social"), Bipartide
	("bio-SC-HT","bio-SC-HT","Biological"),
	("fb-pages-politician","fb-pages-politician","Social"),
	("bio-grid-fruitfly","bio-grid-fruitfly","Biological"),
	("web-indochina-2004","web-indochina-2004","Information"),
	("bio-DM-CX","bio-DM-CX","Biological"),
	("socfb-Haverford76","socfb-Haverford76","Social"),
	("tech-WHOIS","tech-WHOIS","Information"),
	("bio-DR-CX","bio-DR-CX","Biological"),
	("socfb-Swarthmore42","socfb-Swarthmore42","Social"),
	("econ-orani678","econ-orani678","Economy"),
	("bio-grid-human","bio-grid-human","Biological"),
	("socfb-USFCA72","socfb-USFCA72","Social"),
	("rec-movielens-user-movies-10m","rec-movielens-user-movies-10m","Information"),
	("fb-pages-public-figure","fb-pages-public-figure","Social"),
	("bio-HS-CX","bio-HS-CX","Biological"),
	("soc-wiki-elec","soc-wiki-elec","Social"),
	("bio-WormNet-v3-benchmark","bio-WormNet-v3-benchmark","Biological"),
	("socfb-Mich67","socfb-Mich67","Social"),
	("socfb-Bowdoin47","socfb-Bowdoin47","Social"),
	("socfb-Amherst41","socfb-Amherst41","Social"),
	("socfb-Oberlin44","socfb-Oberlin44","Social"),
	("fb-pages-government","fb-pages-government","Social"),
	("socfb-Wellesley22","socfb-Wellesley22","Social"),
	("socfb-Hamilton46","socfb-Hamilton46","Social"),
	("socfb-Smith60","socfb-Smith60","Social"),
	("socfb-Trinity100","socfb-Trinity100","Social"),
	("socfb-Williams40","socfb-Williams40","Social"),
	("socfb-Vassar85","socfb-Vassar85","Social"),
	("socfb-Middlebury45","socfb-Middlebury45","Social"),
	("socfb-Brandeis99","socfb-Brandeis99","Social"),
	("socfb-Wesleyan43","socfb-Wesleyan43","Social"),
	("socfb-Pepperdine86","socfb-Pepperdine86","Social"),
	("socfb-Santa74","socfb-Santa74","Social"),
	("socfb-Colgate88","socfb-Colgate88","Social"),
	("socfb-Bucknell39","socfb-Bucknell39","Social"),
	("socfb-UC64","socfb-UC64","Social"),
	("socfb-Rochester38","socfb-Rochester38","Social"),
	("bio-CE-CX","bio-CE-CX","Biological"),
	("socfb-Rice31","socfb-Rice31","Social"),
	("socfb-JohnsHopkins55","socfb-JohnsHopkins55","Social"),
	("socfb-Vermont70","socfb-Vermont70","Social"),
	("socfb-Lehigh96","socfb-Lehigh96","Social"),
	("socfb-Howard90","socfb-Howard90","Social"),
	("socfb-UChicago30","socfb-UChicago30","Social"),
	("socfb-American75","socfb-American75","Social"),
	("socfb-UCSC68","socfb-UCSC68","Social"),
	("socfb-Maine59","socfb-Maine59","Social"),
	("socfb-CMU","socfb-CMU","Social"),
	("socfb-Carnegie49","socfb-Carnegie49","Social"),
	("socfb-MIT","socfb-MIT","Social"),
	("socfb-MIT8","socfb-MIT8","Social"),
	("socfb-Tufts18","socfb-Tufts18","Social"),
	("socfb-William77","socfb-William77","Social"),
	("socfb-Wake73","socfb-Wake73","Social"),
	("socfb-Tulane29","socfb-Tulane29","Social"),
	("socfb-Princeton12","socfb-Princeton12","Social"),
	("socfb-Dartmouth6","socfb-Dartmouth6","Social"),
	("bio-grid-yeast","bio-grid-yeast","Biological"),
	("socfb-Villanova62","socfb-Villanova62","Social"),
	("socfb-Emory27","socfb-Emory27","Social"),
	("econ-psmigr2","econ-psmigr2","Economy"),
	("econ-psmigr1","econ-psmigr1","Economy"),
	("econ-psmigr3","econ-psmigr3","Economy"),
	("socfb-Bingham82","socfb-Bingham82","Social"),
	("socfb-WashU32","socfb-WashU32","Social"),
	("socfb-Brown11","socfb-Brown11","Social"),
	("socfb-Yale4","socfb-Yale4","Social"),
	("scc_twitter-copen","scc_twitter-copen","Social"),
	("socfb-Georgetown15","socfb-Georgetown15","Social"),
	("socfb-Vanderbilt48","socfb-Vanderbilt48","Social"),
	("scc_fb-messages","scc_fb-messages","Social"),
	("socfb-Duke14","socfb-Duke14","Social"),
	("scc_reality","scc_reality","Social"),
	("baselineN50M100","baselineN50M100","Models"),
	("baselineN100M50","baselineN100M50","Models"),
	("baselineN3M2000","baselineN3M2000","Models"),
	("baselineN5M1000","baselineN5M1000","Models"),
	("baselineN10M500","baselineN10M500","Models"),
	("ERIgraph", "ERIgraph", "Models"),
	("ERIgraphLoops", "ERIgraphLoops", "Models"),
	("ERNXSparse", "ERNXSparse", "Models"),
	("ERMine", "ERMine", "Models"),
	("ERNXDense", "ERNXDense", "Models"),
	("ER", "ER", "Models"),
	("hybrid5000k20R0.500","Hybrid R = 0.500", "Models"),
	("hybrid5000k20R0.250","Hybrid R = 0.250", "Models"),
	("hybrid5000k20R0.125","Hybrid R = 0.125", "Models"),
	("hybrid1000k10R0.500","Hybrid N1000 R = 0.500", "Models"),
	("hybrid1000k10R0.250","Hybrid N1000 R = 0.250", "Models"),
	("hybrid1000k10R0.125","Hybrid N1000 R = 0.125", "Models"),
]

realNetworkNames = [entry for entry in realNetworkNames if not entry[0][0:2]=="rt"] 

plotName = "all";

benchmarkNames = [];
for networkRealization in range(bp.networkRealizations):
	for tau1 in bp.t1Values:
		for tau2 in bp.t2Values:
			for mu in bp.muValues:
				benchmarkNames.append((bp.getNetworkName(mu,networkRealization,tau1,tau2),"$\\mu=%.3f$"%mu,"Benchmarks_t1-%.2f_t2-%.2f"%(tau1,tau2)));
		
# for networkRealization in range(bp.networkRealizations):
# 	for mu in [0.55,0.62,0.64,0.66,0.68,0.75]:
# 		benchmarkNames.append((bp.getNetworkName(mu,networkRealization),"$\\mu=%.3f$"%mu,"Benchmarks"));

for networkRealization in range(bp.networkRealizations):
	for mu in gn.muValues:
		# benchmarkNames.append(gn.getNetworkName(gn.P_in,P_out,networkRealization));
		benchmarkNames.append((gn.getNetworkName(gn.nodesCount,gn.communitiesCount,gn.avgk,mu,networkRealization),"$\\mu=%.3f$"%mu,"GN"));


# for mu in bp.muValues:
# 	networkName = bp.getNetworkName(mu,networkRealization);
# 	plotData(ax,"NMI",networkName,"$\\mu=%.3f$"%mu,plotIndex);
#bp.getNetworkName(0,networkRealization))
networkNames = []
networkNames += benchmarkNames;#+realNetworkNames;
networkNames += realNetworkNames;
def loadDistributionData(measurement,variant,networkName,bins=100):
	data = [];
	try:
		with gzip.open("../Data/Results/pairwise%s_distrib_%s_%s.txt.gz"%(measurement,variant,networkName),"rt") as fd:
			for line in fd:
				entry = [float(value) for value in line.strip().split(" ")];
				data.append(entry); #np.histogram(entry,range=(0,1),bins=bins)[0]);
	except:
		print("!NOT FOUND: %s"%("../Data/Results/pairwise%s_distrib_%s_%s.txt.gz"%(measurement,variant,networkName)));
		return None;
	data = np.array(data);
	if(data.shape[0]==0):
		return None;
	else:
		return data;

figureSize = 3.0

rewireMode="basic";
variants = ["infomap","multilevel","multilevelZero","SBMBasic"," "];
variants = ["infomap","multilevel"," ","SBMBasic"," "];
variants = ["infomap","multilevel"," ","SBMBasic"," "];
variants = ["infomap","multilevel","SBMBasic"];
# variants = ["SBMBasic"];

import gzip
from matplotlib.colors import LogNorm

bins = 100

measurements = [
"NMI",
"AMI",
"NVI",
# "ARI",
# "VME",
"NC",
"CS",
"ACS",
"S",
"SR",
"DS",
]


legends = False;
networkRealization = 0;
plotIndex = 0;
columns = 4;
trivialThreshold = 1.0

allDataByCategory = {};
for measurement in measurements:
	for variant in variants:
	# 	variant="fast_%s"%variant;
		labels = [];
		for networkName,label,category in networkNames:
			if(category not in allDataByCategory):
				allDataByCategory[category] = OrderedDict();
			distribData = loadDistributionData(measurement,"%s_%s"%(rewireMode,variant),networkName);
			if(distribData is not None):
				if(networkName not in allDataByCategory[category]):
					allDataByCategory[category][networkName] = OrderedDict();
				if(variant not in allDataByCategory[category][networkName]):
					allDataByCategory[category][networkName][variant] = OrderedDict();
				if(measurement not in allDataByCategory[category][networkName][variant]):
					allDataByCategory[category][networkName][variant][measurement] = OrderedDict();
				allDataByCategory[category][networkName]["LABEL"] = label;
				allDataByCategory[category][networkName][variant][measurement] = distribData;


networkSizes = {};
for variant in variants:
	labels = [];
	for networkName,label,category in networkNames:
		if(category not in allDataByCategory):
			allDataByCategory[category] = OrderedDict();
		if(category not in allDataByCategory):
			continue;
		if(networkName not in allDataByCategory[category]):
			continue;
		if(variant not in allDataByCategory[category][networkName]):
			continue;
		networkData = allDataByCategory[category][networkName][variant];
		if("S" not in networkData):
			continue
		if("NC" not in networkData or networkData["NC"] is None or
			"CS" not in networkData or networkData["CS"] is None):
			continue;
		# print("OK %s"%networkName);
		averageCommunitySizes = networkData["ACS"];
		averageEntropy = networkData["S"]
		communitySizes = networkData["CS"];
		numberOfCommunities = networkData["NC"];
		verticesCount = int(np.sum(communitySizes[0])/numberOfCommunities.shape[1]);
		networkSizes[networkName] = verticesCount;
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
				communitySizesDistrib = communitySizes[alphaIndex][startIndex:endIndex];
				avgSize = np.average(communitySizesDistrib);
				avgDiff = abs(avgSize - averageCommunitySizes[alphaIndex][i]);
				if(avgDiff>=1):
					print("MAJOR ERROR!!!!!!!! %f %f"%(avgSize,averageCommunitySizes[alphaIndex][i]));
				majorCommunitySizesDistrib.append(np.max(communitySizesDistrib));
				errorMajorCommunitySizesDistrib.append(np.std(communitySizesDistrib));
				trivialThresholdSize = trivialThreshold*verticesCount;
				if(np.max(communitySizesDistrib)>=trivialThresholdSize):
					trivialCount+=1;
				elif(len(communitySizesDistrib)>=trivialThresholdSize):
					trivialCount+=1;
			
			trivialRatios.append([trivialCount/len(communityIndices)]);
			majorCommunitySizes.append(majorCommunitySizesDistrib);
			errorMajorCommunitySizes.append(errorMajorCommunitySizesDistrib);
		distribData = np.array(majorCommunitySizes)/verticesCount;
		errorDistribData = np.array(errorMajorCommunitySizes)/verticesCount;
		if(networkName not in allDataByCategory[category]):
			allDataByCategory[category][networkName] = OrderedDict();
		if(variant not in allDataByCategory[category][networkName]):
			allDataByCategory[category][networkName][variant] = OrderedDict();
		if("MCS" not in allDataByCategory[category][networkName][variant]):
			allDataByCategory[category][networkName][variant]["MCS"] = OrderedDict();
		if("ECS" not in allDataByCategory[category][networkName][variant]):
			allDataByCategory[category][networkName][variant]["ECS"] = OrderedDict();
		if("TPR" not in allDataByCategory[category][networkName][variant]):
			allDataByCategory[category][networkName][variant]["TPR"] = OrderedDict();
		allDataByCategory[category][networkName]["LABEL"] = label;
		allDataByCategory[category][networkName][variant]["MCS"] = distribData;
		allDataByCategory[category][networkName][variant]["ECS"] = errorDistribData;
		allDataByCategory[category][networkName][variant]["TPR"] = trivialRatios;


measurements+=["MCS","ECS","TPR"];

from tqdm.auto import tqdm

dirName = "../Figures/NewCurves/%s/All"%(rewireMode);
try:
  os.makedirs(dirName)    
  print("Directory " , dirName ,  " Created ")
except FileExistsError:
  pass;

fig = plt.figure(figsize=(figureSize*1.61803398875,figureSize));
ax = fig.add_axes([0.18, 0.18, 0.65, 0.70]);
for j,variant in enumerate(variants):
  areasCategories = [];
  for category in tqdm(allDataByCategory,desc="Category"):
    areas = []
    labels = []
    networkKeys = sorted(list(allDataByCategory[category].keys()));
    for i,key in enumerate(tqdm(networkKeys,desc="Network")):
      networkData = allDataByCategory[category][key];
      networkLabel = allDataByCategory[category][key]["LABEL"];
      for j,variant in enumerate(variants):
        if(variant in networkData and measurement in networkData[variant] and networkData[variant][measurement] is not None):
          networkSize = networkSizes[key]
          values = networkData[variant][measurement]
          areas.append(1.0-np.trapz(values, alphaValues))
          labels.append(labels)
    ax.boxplot(CCAreasData,labels=labels,whis=[5,95],vert=False,showfliers=False,
    showcaps=False, showbox=False,
      boxprops={"alpha":0.25},capprops={"alpha":0.25},whiskerprops={"alpha":0.0});
  
for i in range(len(CCAreasData)):
	x = CCAreasData[i]
	y = np.random.normal(1+i, 0.04, size=len(x))
#   ax.scatter(x, y, alpha=1.0);
	plt.errorbar(x, y, xerr=CCAreasErrorsByCategory[labels[i]], fmt='o')
dirName = "../Figures/Curves/%s/%s/"%(variant,measurement);
try:
	os.makedirs(dirName)    
	print("Directory " , dirName ,  " Created ")
except FileExistsError:
	print("Directory " , dirName ,  " already exists") 

fig.savefig("%s/CcAreasBoxPlot.pdf"%(dirName));
plt.close(fig);

    fig.savefig("%s/%s_Distrib_%s.pdf"%(dirName,measurement,category));
    plt.close(fig);

      
