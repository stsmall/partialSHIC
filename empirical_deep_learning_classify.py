# -*- coding: utf-8 -*-
"""
python3 empirical_deep_learning_classify.py training.npy AOM.2L.fvec 11 90 AOM.2L.bed .90
"""
import numpy as np
import keras
import sys

if len(sys.argv) != 7:
    sys.exit("usage:\npython3 empirical_deep_learning_classify.py classifierPickleFileName fvecFileName numSubWins numSumStatsPerSubWin bedFileName\n")
else:
    classifierPickleFileName, fvecFileName, numSubWins, numSumStatsPerSubWin, bedFileName, prob = sys.argv[1:]

# load model
netlayers = keras.models.load_model(classifierPickleFileName)
# load data
fvecFile = open(fvecFileName)
fvec = fvecFile.readlines()
fvecFile.close()

fvec = fvec[1:]
coords, fvecData = [], []
numSubWins, numSumStatsPerSubWin = int(numSubWins), int(numSumStatsPerSubWin)
for example in fvec:
    if "nan" not in example:
        coords.append(example.strip().split("\t")[:-(numSubWins*numSumStatsPerSubWin)])
        exampleData = example.strip().split("\t")[-(numSubWins*numSumStatsPerSubWin):]
        currVector = []
        for i in range(len(exampleData)):
            currVector.append(float(exampleData[i]))
        fvecData.append(currVector)
if not fvecData:
    sys.exit("Weird: no nan-less features in input file. Terminating...\n")

# standardize shape
fvecData = np.reshape(np.array(fvecData), (np.array(fvecData).shape[0], numSumStatsPerSubWin, numSubWins, 1))

# make preds
preds = netlayers.predict(fvecData)
predictions = np.argmax(preds, axis=1)  # best class

labelToClassName = {0: "Neutral", 1: "Hard", 2: "linkedHard", 3: "Soft", 4: "linkedSoft",
                    5: "PartialHard", 6: "linkedPartialHard", 7: "PartialSoft", 8: "linkedPartialSoft"}
predictionCounts = {}
for i in range(9):
    predictionCounts[labelToClassName[i]] = 0

# write out predictions
if bedFileName.lower() in ["none", "false", "default"]:
    bedFileName = fvecFileName.split('/')[-1].replace(".fvec", "")+".bed"

bedFile = open(bedFileName, "w")
bedFile.write('chrom\tclassifiedWinStart\tclassifiedWinEnd\tpredClass\t'
              'prob(neutral)\tprob(Hard)\tprob(linkedHard)\tprob(Soft)\t'
              'prob(linkedSoft)\tprob(PartialHard)\tprob(linkedPartialHard)\t'
              'prob(PartialSoft)\tprob(linkedPartialSoft)\thq90\n')
for i in range(len(predictions)):
    chrom, start, end = coords[i][:3]
    start, end = int(start), int(end)
    predictedClass = labelToClassName[predictions[i]]
    predictionCounts[predictedClass] += 1
    probs_ls = "\t".join(map(str, preds[i]))
    hq = np.where(preds[i] > float(prob))[0]
    if len(hq) > 1:
        hq_pred = labelToClassName[hq[0]]
    else:
        hq_pred = "None"
    bedFile.write(f"{chrom}\t{start-1}\t{end}\t{predictedClass}\t{probs_ls}\t{hq_pred}\n")
bedFile.close()

# stats
sys.stderr.write("\n\n#####---Stats Out---#####\n")
sys.stderr.write(f"made predictions for {len(predictions)} total instances\n")
nc = predictionCounts["Neutral"]
nf = predictionCounts["Neutral"]/len(predictions)
sys.stderr.write(f"predicted {nc} neutral regions ({nf} of all classified regions)\n")
for i in range(1, 9):
    pc = predictionCounts[labelToClassName[i]]
    pl = labelToClassName[i]
    pf = predictionCounts[labelToClassName[i]]/len(predictions)
    sys.stderr.write(f"predicted {pc} {pl} sweep regions ({pf} of all classified regions)\n")
