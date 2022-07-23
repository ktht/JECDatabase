import subprocess
import shutil
import itertools
import os

from JERCHelpers import *


def createSingleYearJSON(jerList, jecList, algosToConsider, outputName):
    jerAlgoList = list(itertools.product(jerList, algosToConsider))
    jecAlgoList = list(itertools.product(jecList, algosToConsider))

    if "2017_UL" in outputName: #manual fix as UL17_JRV2 only contains AK4PFchs SF/PtResolution
        jerAlgoList = list(itertools.product(jerList, ["AK4PFchs"]))

    for p in jecAlgoList:
        jec,algo=p
        subprocess.run(["wget","-q","-O","{}.tar.gz".format(jec), "https://github.com/cms-jet/JECDatabase/raw/master/tarballs/{}.tar.gz".format(jec)])
        shutil.unpack_archive("{}.tar.gz".format(jec),jec)
        subprocess.run(["python3", "JEC2JSON.py", "-a",algo, jec])

    for p in jerAlgoList:
        jer,algo=p
        ext = 'tgz' if jer == 'Autumn18_V7_MC' else 'tar.gz'
        subprocess.run(["wget", "-q", "-O","{}.tar.gz".format(jer), "https://github.com/cms-jet/JRDatabase/raw/master/tarballs/{}.{}".format(jer, ext)])
        shutil.unpack_archive("{}.tar.gz".format(jer),'' if ('Legacy' in outputName and '2017' in outputName) else jer)
        subprocess.run(["python3", "JER2JSON.py", "-a",algo,jer])
    
    print("Done generating individual jsons. Will merge into single year files now")
    
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAlgoList+jecAlgoList)] + [">", "{}.json".format(outputName)])

    outputDirName = os.path.dirname(outputName)
    if not os.path.isdir(outputDirName):
        os.makedirs(outputDirName)
    
    print(command)#subprocess seems to not work with long command?
    os.system(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputName,outputName))
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputName,outputName))
    print("rm -f {}.json.gz".format(outputName))
    os.system("rm -f {}.json.gz".format(outputName))
    print("gzip {}.json".format(outputName))
    os.system("gzip {}.json".format(outputName))
    name = outputName.split("/")[0]

    jerAK4List = list(itertools.product(jerList, ["AK4PFchs"]))
    jecAK4List = list(itertools.product(jecList, ["AK4PFchs"]))
    outputNameAK4 = "{name}/{name}_jet_jerc".format(name = name)
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAK4List+jecAK4List)] + [">", "{}.json".format(outputNameAK4)])
    print(command)#subprocess seems to not work with long command?
    os.system(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK4,outputNameAK4))
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK4,outputNameAK4))
    print("rm -f {}.json.gz".format(outputNameAK4))
    os.system("rm -f {}.json.gz".format(outputNameAK4))
    print("gzip {}.json".format(outputNameAK4))
    os.system("gzip {}.json".format(outputNameAK4))

    jerAK8List = list(itertools.product(jerList, ["AK8PFPuppi"]))
    if "2017_UL" in outputName: #manual fix as UL17_JRV2 only contains AK4PFchs SF/PtResolution
        jerAK8List = []
    jecAK8List = list(itertools.product(jecList, ["AK8PFPuppi"]))
    outputNameAK8 = "{name}/{name}_fatJet_jerc".format(name = name)
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAK8List+jecAK8List)] + [">", "{}.json".format(outputNameAK8)])

    print(command)#subprocess seems to not work with long command?
    os.system(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK8,outputNameAK8))
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK8,outputNameAK8))
    print("rm -f {}.json.gz".format(outputNameAK8))
    os.system("rm -f {}.json.gz".format(outputNameAK8))
    print("gzip {}.json".format(outputNameAK8))
    os.system("gzip {}.json".format(outputNameAK8))



    
print(JER2016,JEC2016)
print(JER2017,JEC2017)
print(JER2018,JEC2018)

#JEC2016,JEC2017,JEC2018=[],[],[] 
#JER2016,JER2017,JER2018=[],[],[] 
createSingleYearJSON(JER2016,       JEC2016,        algosToConsider,"2016Legacy/2016Legacy_jerc")
createSingleYearJSON(JER2017,       JEC2017,        algosToConsider,"2017Legacy/2017Legacy_jerc")
createSingleYearJSON(JER2018,       JEC2018,        algosToConsider,"2018Legacy/2018Legacy_jerc")

