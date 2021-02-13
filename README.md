# partialSHIC

Example files include bash scripts that are hardcoded for the Xue et al. paper. Many of the options, though undescribed in the bash, are similar to the options in diploSHIC. I have done my best to add detail to this repo. I dont guarantee that anything is 100% correct, check it, let me know, and use at your own risk.

## Training
Train data with discoal in same way as described in the diploSHIC [soup-to-nuts](https://github.com/kr-colab/diploSHIC/wiki/A-soup-to-nuts-example). For the partial sweeps, Xue et al., uses the range -Pc 0.2 0.99. If you have training sims already done for diploSHIC (hard, soft, neutral) then all you need is the partialHard and partialSoft. Use the same -x with the same 11 window locations and a default of 55000 bp.   

**IMPORTANT** to convert to feature vectors you also need a partial_stats.txt file. This is to normalize the nSL and iHS stats by allele frequency. You should use the calcStatsAndDataForEachSnpSingleMsFile.py on your neutral.msOut.gz file.  

*Note the pMisPol is the percentage of sites that are intentionally mispolarized in the training data. Xue et al., uses the results of running stairwayplot with a specific version [here](https://github.com/kr-colab/stairwayPlotMisorient). The percent mispolarized is in the header of the output file. You dont need to do it that way, but then try to find a reliable way to estimate the polarization error.*

### Simulated data to feature vectors  
 *sims should be gzipped and in ms format*  
 * `python training_convert_to_FVs.py trainingDataFileName chrArmsForMasking subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName statDir fvecFileName`
 * `python training_convert_to_FVs.py trainingData/hard_5.msOut.gz 3R 5000 11 0.25 0.01 neutral_partial_stats.txt genome_accessible.fa ancestral.fa simStats/ outFile.fvec`  

### Make training sets 
*I thought this made equal trainingsets, but it does not. If your training fvecs are of different length they will get caught in an assert statement in the code.*
 * `python training_sample_FVs.py neutTrainingFileName hardTrainingFilesPrefix softTrainingFilesPrefix partialHardTrainingFilesPrefix partialSoftTrainingFilesPrefix sweepTrainingWindow linkedTrainingWindows sampledFVsDir sampledFVsFiles`
 * `python training_sample_FVs.py trainingData/neut.fvec trainingData/hard/hard_ trainingData/soft/soft_ trainingData/partialHard/partialHard_ trainingData/partialSoft/partialSoft_ 5 0,1,2,3,4,6,7,8,9,10 trainingSets/ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec`  

### Train CNN classifier
 * `python training_deep_learning.py fvecDir fvecFiles numSubWins numSumStatsPerSubWin validationSize weightsFileName jsonFileName npyFileName`  
 * `python training_deep_learning.py trainingData/FVs default 11 90 0.1 classifier/model.hdf5 classifier/model.json classifier/model.npy`  
 * default here refers to all expected fvecs
   * neut.fvec
   * hard.fvec
   * linkedHard.fvec
   * soft.fvec
   * linkedSoft.fvec
   * partialHard.fvec
   * linkedPartialHard.fvec
   * partialSoft.fvec
   * linkedPartialSoft.fvec  

## Testing  
Evaluate the accuracy of your classification on test data. **Do not use the same data as training**
### Test data to feature vectors  
 * `python testing_convert_to_FVs.py neutral.msOut.gz 3R 5000 11 0.25 0.01 neutral_partial_stats.txt genome_accessible.fa ancestral.fa testStats/ neut.msOut.test.fvec` 
### Classify test data  
 * `python testing_deep_learning_classify.py classifierPickleFileName fvecDir numSubWins numSumStatsPerSubWin resultsDir accuracyFilesPrefix confusionMatrixFigFileName`  
 * `python testing_deep_learning_classify.py classifier/model.npy testingData/ 11 90 testingData/ accuracy confusion_matrix.pdf`  

## Empirical *(real data)*  
### Feature vectors from real data *(data should be in h5 format)*  
*(NOTE)Xue et al, did not detail how this was done (or I missed it). I am using scikit-allel to load a vcf and save as an h5* 
 * `python2 empirical_convert_to_FVs.py chrArmFileName chrArm chrLen [segmentStart segmentEnd] subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName sampleToPopFileName targetPop statFileName fvecFileName`  
 * `python2 empirical_convert_to_FVs.py ag1000g.phase1.ar3.haplotypes.2L.h5 2L 49364325 1 5000000 5000 11 0.25 0.01 AOM_partial_stats.txt Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa anc.meru_mela.2L.fa samples_pops.txt AOM 2L.1.stats 2L.1.fvec`  
 * `empirical_merge_FVs.sh`  *this is necessary only if you step through the VCF(h5) in segments*  
### Classify feature vectors from real data  
 * `python3 empirical_deep_learning_classify.py classifierPickleFileName fvecFileName numSubWins numSumStatsPerSubWin bedFileName`  
 * `python3 empirical_deep_learning_classify.py trainingData/pop.npy empiricalData/FVs/pop.chrArm.fvec 11 89 empiricalData/pop.chrArm.bed`  
