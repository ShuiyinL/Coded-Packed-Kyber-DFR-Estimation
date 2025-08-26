### The decryption failure attack estimation for P_l Kyber 

The software used for this analysis [1] is available in: https://github.com/KULeuven-COSIC/PQCRYPTO-decryption-failures/tree/master/DecryptionFailureAttack
- run "P_Kyber_failureboost.py"
  - change the value of `XXXX` in `toplot = [XXXX]` to select the target, where `XXXX` can be one of: `P_Kyber768`, `P_Kyber1024`, `Kyber768`, or `Kyber1024`
- For reference, the precomputed values of α and β are stored in the files named "P_KyberXXXX.pkl" or "KyberXXXX.pkl"

[1] D’Anvers, JP., Guo, Q., Johansson, T., Nilsson, A., Vercauteren, F., Verbauwhede, I. (2019). Decryption Failure Attacks on IND-CCA Secure Lattice-Based Schemes. In: Lin, D., Sako, K. (eds) Public-Key Cryptography – PKC 2019. PKC 2019. Lecture Notes in Computer Science(), vol 11443. Springer, Cham. https://doi.org/10.1007/978-3-030-17259-6_19
