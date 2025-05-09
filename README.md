# Coded-Packed-Kyber-DFR-Estimation
Source codes for the paper: Shuiyin Liu, Amin Sakzad "P_\ell-Kyber: Packing \ell Plaintexts and Lattice Coding for Kyber"
https://www.arxiv.org/pdf/2504.17185
# Acknowledgements
This project uses codes from [Security Estimation Scripts for Kyber and Dilithium] in https://github.com/pq-crystals/security-estimates

P_L_Kyber.py
* Compute the DFR and CER for 
  * Uncoded P_{\ell}-Kyber, for any \ell >=1
  * Coded P_{\ell}-Kyber, for \ell= 8 (E8 lattice), 16 (BW16 lattice), 24 (Leech latice)
  * P_{t,\ell}-Kyber, for \ell= 8 (E8 lattice) and t=32 (N=32 bytes), 64 (N=64 bytes)

Some small changes in the original functions in https://github.com/pq-crystals/security-estimates

proba_util.py
* clean_dist(A):  Clean a distribution to accelerate further computation (drop element of the support with proba less than 2^-300)
  * change: We change 2^-300 to 2^-400.

Kyber_failure.py
* p2_cyclotomic_final_error_distribution(ps,LloydCu,LloydCv): construct the final error distribution of Kyber
  * change: Replace original Kyber compression error distribution by MMSE quantization noise distribution: (Rc=LloydCu, R2 =LloydCv)

Dataset: Cu9-11.mat, Cv3-6.mat
* The MMSE quantization noise distributions: LloydCu and LloydCv
* can be reproduced by MMSE_Quantization.m with dx= 3-6, 9-11
