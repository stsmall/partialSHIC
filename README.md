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
If you use [scikit-allel](http://alimanfoo.github.io/2017/06/14/read-vcf.html) to make an h5 file you can run `allel.vcf_to_hdf5('example.vcf', 'example.h5', fields='*', alt_number=1, group=chrom, overwrite=True)` .The script, empirical_convert_to_FVs, expects a group name matching the chromosome and only 1 alternate allele. scikit-allel by default stores 3 which throws an error when the script tries to polarize with an ancestral file.  
### Feature vectors from real data *(data should be in h5 format)*  
 * `python empirical_convert_to_FVs.py chrArmFileName chrArm chrLen [segmentStart segmentEnd] subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName sampleToPopFileName targetPop statFileName fvecFileName`  
 * `python empirical_convert_to_FVs.py species.chr2.h5 2 49000000 1 5000000 5000 11 0.25 0.01 neutral_partial_stats.txt genome_accessible.fa ancestral.fa samples_pops.txt POP1 chr2.1-5mb.stats chr2.1-5mb.fvec`  
### Classify feature vectors from real data  
*WARNING I can not get this working ... will update when I figure it out*
 * `python empirical_deep_learning_classify.py classifierPickleFileName fvecFileName numSubWins numSumStatsPerSubWin bedFileName`  
 * `python empirical_deep_learning_classify.py classifier/model.npy empiricalData/pop1.chr2.fvec 11 90 results/pop1.chr2.bed`  
