### The DFR estimation for P_l Kyber 

The software used for this analysis is available in: https://github.com/pq-crystals/security-estimates
- run "P_L_Kyber.py"
  - set MMSE_Q = 1 for MMSE quantization; or set MMSE_Q = 0 for original Kyber quantization`
  - change the value of `x` in `Kyber_type = x` to select the target Kyber variant
  - set packed_size = \ell. Lattice encoder available for \ell = 8 (E8 lattice), 16 (BW16 lattice), 24 (Leech lattice)
  
  
