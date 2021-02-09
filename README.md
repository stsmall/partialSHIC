# partialSHIC

Example files include bash scripts that are hardcoded for the Xue et al. paper. Many of the options, though undescribed in the bash, are similar to the options in diploSHIC. I have done my best to add detail to this repo ... it was very confusing. I dont guarantee that anything is 100% correct, check it, let me know, and use at your own risk.

## Training
### Simulated data to feature vectors  
 *sims should be gzipped and in ms format*  
 * `python2 training_convert_to_FVs.py trainingDataFileName chrArmsForMasking subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName statDir fvecFileName`
 * `python2 training_convert_to_FVs.py trainingData/sp* 2L,2R,3L,3R 5000 11 0.25 0.01 mosquito_data_files/pop_partial_stats.txt mosquito_data_files/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa mosquito_data_files/anc.meru_mela.fa trainingData/sumstats/ trainingData/FVs/pop.fvec`  
### Make equal training sets 
 * `python2 training_sample_FVs.py neutTrainingFileName hardTrainingFilesPrefix softTrainingFilesPrefix partialHardTrainingFilesPrefix partialSoftTrainingFilesPrefix sweepTrainingWindow linkedTrainingWindows sampledFVsDir sampledFVsFiles`
 * `python2 training_sample_FVs.py trainingData/FVs/spNeut.fvec trainingData/FVs/spHard_ trainingData/FVs/spSoft_ trainingData/FVs/spPartialHard_ trainingData/FVs/spPartialSoft_ 5 0,1,2,3,4,6,7,8,9,10 trainingData/FVs/ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec`  
#### *(optional)* Visualze heatmap of vector images for each state
 * `training_visualize_FVs.sh`  
### Train CNN classifier
 * `python3 training_deep_learning.py fvecDir fvecFiles numSubWins numSumStatsPerSubWin validationSize weightsFileName jsonFileName npyFileName`  
 * `python3 training_deep_learning.py trainingData/FVs default 11 89 0.1 trainingData/pop.hdf5 trainingData/pop.json trainingData/pop.npy`  
 * default here refers to all expected fvecs: neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec  
#### *(alternative)* Train CNN for five-state classification only (i.e. without partial sweeps, similar to disploSHIC) 
 * `python3 training_deep_learning_5-state-complete-sweeps-only.py trainingData/FVs default 11 89 0.1 trainingData/pop.hdf5 trainingData/pop.json trainingData/pop.npy`  
 * default here refers to all but the partial ones: neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec  


## Testing
### Test data to feature vectors  
 * `testing_convert_to_FVs.sh`  
 * `testing_convert_to_FVs.py`  
### Classify test data  
 * `testing_deep_learning_classify.sh`  
 * `testing_deep_learning_classify.py`  
#### *(alternative)* Classify test data using five-state classifier (see above)  
 * `testing_deep_learning_classify_5-state-complete-sweeps-only.sh`  
 * `testing_deep_learning_classify_5-state-complete-sweeps-only.py`  

## Empirical *(real data)*  
### Feature vectors from real data *(data should be in h5 format)*  
*(NOTE)Xue et al, did not detail how this was done (or I missed it). I am using scikit-allel to load a vcf and save as an h5* 
 * `python2 empirical_convert_to_FVs.py chrArmFileName chrArm chrLen [segmentStart segmentEnd] subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName sampleToPopFileName targetPop statFileName fvecFileName`  
 * `python2 empirical_convert_to_FVs.py ag1000g.phase1.ar3.haplotypes.2L.h5 2L 49364325 1 5000000 5000 11 0.25 0.01 AOM_partial_stats.txt Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa anc.meru_mela.2L.fa samples_pops.txt AOM 2L.1.stats 2L.1.fvec`  
 * `empirical_merge_FVs.sh`  *this is necessary only if you step through the VCF(h5) in segments*  
### Classify feature vectors from real data  
 * `python3 empirical_deep_learning_classify.py classifierPickleFileName fvecFileName numSubWins numSumStatsPerSubWin bedFileName`  
 * `python3 empirical_deep_learning_classify.py trainingData/pop.npy empiricalData/FVs/pop.chrArm.fvec 11 89 empiricalData/pop.chrArm.bed`  
