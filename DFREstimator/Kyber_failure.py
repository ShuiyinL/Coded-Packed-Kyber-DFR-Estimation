### Acknowledgements
# This project uses codes from [Security Estimation Scripts for Kyber and Dilithium] in https://github.com/pq-crystals/security-estimates

import operator as op
from math import factorial as fac
from math import sqrt, log
import sys
from proba_util import *

def p2_cyclotomic_final_error_distribution(ps,LloydCu,LloydCv, MMSE_Q):
    """ construct the final error distribution in our encryption scheme
    :param ps: parameter set (ParameterSet)
    """
    #Replace original Kyber compression error distribution with MMSE quantization noise distribution (Rc=LloydCu, R2 =LloydCv)
    
    chis = build_centered_binomial_law(ps.ks)           # LWE error law for the key
    chie = build_centered_binomial_law(ps.ke_ct)        # LWE error law for the ciphertext      e_2
    chie_pk = build_centered_binomial_law(ps.ke)
    Rk = build_mod_switching_error_law(ps.q, ps.rqk)    # Rounding error public key                  c_u

    #Rc: Cu in Kyber
    #Rc = build_mod_switching_error_law(ps.q, ps.rqc)    # rounding error first ciphertext Cu
    #Rc=LloydCu

    if MMSE_Q==1:
        Rc=LloydCu
    else:
        Rc = build_mod_switching_error_law(ps.q, ps.rqc)
        
    
    chiRs = law_convolution(chis, Rk)                   # LWE+Rounding error key                   e_1+c_u
    chiRe = law_convolution(chie, Rc)                   # LWE + rounding error ciphertext

    B1 = law_product(chie_pk, chiRs)                       # (LWE+Rounding error) * LWE (as in a E*S product)  
    B2 = law_product(chis, chiRe)

    C1 = iter_law_convolution(B1, ps.m * ps.n)
    C2 = iter_law_convolution(B2, ps.m * ps.n)

    C=law_convolution(C1, C2)

    #R2: Cv in Kyber
    #R2 = build_mod_switching_error_law(ps.q, ps.rq2)    # Rounding2 (in the ciphertext mask part)
    #R2 =LloydCv

    if MMSE_Q==1:
        R2 =LloydCv
    else:
        R2 = build_mod_switching_error_law(ps.q, ps.rq2)

   
    
    F = law_convolution(R2, chie)                       # LWE+Rounding2 error                              e_2+c_v
    D = law_convolution(C, F)                           # Final error
  
    return D, Rc


def p2_cyclotomic_error_probability(ps,LloydCu,LloydCv,MMSE_Q):
    F,Cu = p2_cyclotomic_final_error_distribution(ps, LloydCu,LloydCv, MMSE_Q)
    proba = tail_probability(F, round(ps.q/4)) #DFR per symbol, no union bound
    #return F, ps.n*proba
    return F, proba,Cu
