# Slingshot in Python

This is a Python implementation of the Slingshot pseudotime algorithm (Street et al., 2018).

An complete working example is located in `slingshot.ipynb`, using a synthetically generated dataset.

Requirements: 

- `numpy`, `scipy`, `sklearn`
- My fork of `pcurvepy` (https://github.com/mossjacob/pcurvepy):
  
  `pip install git+https://github.com/mossjacob/pcurvepy`


[1] Street, K., Risso, D., Fletcher, R.B., Das, D., Ngai, J., Yosef, N., Purdom, E. and Dudoit, S., 2018. Slingshot: cell lineage and pseudotime inference for single-cell transcriptomics. BMC genomics, 19(1), pp.1-16.