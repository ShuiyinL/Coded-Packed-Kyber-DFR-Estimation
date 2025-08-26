### Coded-Packed-Kyber-DFR-Estimation
DFR estimation for the paper: Shuiyin Liu, Amin Sakzad "Compact Lattice-Coded (Multi-Recipient) Kyber without CLT Independence Assumption"
# Acknowledgements
This project uses the following codes 
- [Security Estimation Scripts for Kyber and Dilithium] in https://github.com/pq-crystals/security-estimates
- [Decryption Failure Attack Estimator] in https://github.com/KULeuven-COSIC/PQCRYPTO-decryption-failures/tree/master/DecryptionFailureAttack

### DFR Estimator is located in the `DFREstimator` folder
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
* p2_cyclotomic_final_error_distribution(ps,LloydCu,LloydCv, MMSE_Q): construct the final error distribution of Kyber
  * set MMSE_Q = 1 for MMSE quantization; MMSE_Q = 0 for original Kyber quantization
  * MMSE_Q = 1: Replace original Kyber compression error distribution by MMSE quantization noise distribution: (Rc=LloydCu, R2 =LloydCv)

Dataset: Cu9-11.mat, Cv3-6.mat
* The MMSE quantization noise distributions: LloydCu and LloydCv
* can be reproduced by MMSE_Quantization.m with dx= 3-6, 9-11

### DF Attack Estimator is located in the `DecryptionFailureAttack` folder

P_Kyber_failureboost.py
* change the value of `XXXX` in `toplot = [XXXX]` to select the target, where `XXXX` can be one of: `P_Kyber768`, `P_Kyber1024`, `Kyber768`, or `Kyber1024`
* For reference, the precomputed values of α and β are stored in the files named "P_KyberXXXX.pkl" or "KyberXXXX.pkl"
