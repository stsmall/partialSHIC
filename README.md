# partialSHIC

Example files include bash scripts that are hardcoded for the Xue et al. paper. Many of the options, though undescribed in the bash, are similar to the options in diploSHIC. I have done my best to add detail to this repo ... it was very confusing. I dont guarantee that anything is 100% correct, check it, let me know, and use at your own risk.

## Training
### Simulated data to feature vectors  
 *sims should be gzipped and in ms format*  
 * `training_convert_to_FVs.sh`  
 * `training_convert_to_FVs.py`
### Make equal training sets 
 * `training_sample_FVs.sh`
 * `training_sample_FVs.py`  
#### *(optional)* Visualze heatmap of vector images for each state
 * `training_visualize_FVs.sh`  
### Train CNN classifier
 * `training_deep_learning.sh`  
 * `training_deep_learning.py`  
#### *(alternative)* Train CNN for five-state classification only (i.e. without partial sweeps, similar to disploSHIC) 
 * `training_deep_learning_5-state-complete-sweeps-only.sh`  
 * `training_deep_learning_5-state-complete-sweeps-only.py`  

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
### Feature vectors from real data *(data should be in h5 format)  
*(NOTE)Xue et al, did not detail how this was done (or I missed it). I am using scikit-allel to load a vcf and save as an h5* 
 * `empirical_convert_to_FVs.sh`  
 * `empirical_convert_to_FVs.py`  
 * `empirical_merge_FVs.sh`  
### Classify feature vectors from real data  
 * `empirical_deep_learning_classify.sh`
 * `empirical_deep_learning_classify.py`
