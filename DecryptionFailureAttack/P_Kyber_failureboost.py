# -*- coding: utf-8 -*-
from proba_util import *
from proba_util2 import *
from scipy.stats import norm
from math import log


'''
Decryption Failure Attack Estimator [DGJNVV19, PKC]
-Original codes: https://github.com/KULeuven-COSIC/PQCRYPTO-decryption-failures/tree/master
-The Kyber parameters have been updated according to FIPS 203
--The public key remains uncompressed.
-P-Kyber with MMSE quantization is provided
--The decoding threshold P KyberXXX[’thres’] at q/4, which serves as a lower
  bound on the decoding radius per dimension for the E8 lattice encoder.
--Therefore, the computed attck cost is a lower bound on the true cost.
'''

def Probl(n, s, sprime, e, eprime):
    # get the variance of the secrets
    varS = distvariance(s)
    varE = distvariance(e)

    # calculate the distribution of var(S^T C)_ijk
    abss = {}
    abse = {}
    for i in sprime.keys():
        abss[i**2 * varE] = abss.get(i**2 * varE, 0) + sprime[i]
    for i in eprime.keys():
        abse[i**2 * varS] = abse.get(i**2 * varS, 0) + eprime[i]

    abss = iter_law_convolution_simplify(abss, n, 2**12)
    abse = iter_law_convolution_simplify(abse, n, 2**12)
    res = law_convolution(abss, abse)
    res = simplifyDistribution2(res)

    return clean_dist(res)


def Failgivenl(variance):
    # gaussian approximation of the distribution of the error based on the variance
    return lambda thres: norm.sf(thres, loc=0, scale=sqrt(variance))


def failureboosting(n, n2, thres, s, sprime, e, eprime, eprimeprime, errorCorrection=False, n3=1, **args):
    # only abs of eprimeprime is important
    absepp = law_abs(eprimeprime)

    # calculate the distribution of var(S^T C)_ijk
    probl = Probl(n, s, sprime, e, eprime)

    # calculate the distribution of the failure prob for each value of var(S^T C)_ijk
    thelist = []
    for varl in probl.keys():
        eppfail = {}
        fail = Failgivenl(varl)
        for i in absepp.keys():
            eppfail[fail(thres - i) + fail(thres + i)] = absepp[i]
        eppfail = iter_law_convolution_simplify(eppfail, n2, 2**8)
        for i in eppfail.keys():
            thelist.append((eppfail[i], varl, i))

    # avarage over the values of var(S^T C)_ijk
    faildist = {}
    for pepp, l, failprob in thelist:
        faildist[failprob] = faildist.get(failprob, 0) + probl[l] * pepp

    # final convolution
    faildist = iter_law_convolution_simplify(faildist, n3, 2**13)

    # sort the list by failure probability
    thelist = sorted(faildist.keys(), reverse=True)

    # calculate alpha and beta
    alpha, beta = [], []
    alphatmp, betatmp = 0, 0

    for i in thelist:
        alphatmp += faildist[i]
        alpha.append(alphatmp)

        betatmp += i * faildist[i]
        beta.append(betatmp / alphatmp)

    # cutoff values of alpha smaller than 2**-256 (not useful)
    beta2 = [b for (b, a) in zip(beta, alpha)]
    alpha2 = [a**-1 for a in alpha]

    if errorCorrection:
        beta2 = errorCorrection[0](beta2, **errorCorrection[1])

    return alpha2, beta2


from Parameters_P_Kyber import P_Kyber768,  P_Kyber1024, Kyber768, Kyber1024 

toplot = [P_Kyber1024] # change to Kyber768, P_Kyber1024, Kyber768, Kyber1024 
import pickle
import os.path
for i in toplot:
    if os.path.exists(i['name'] + "-2.pkl"):
        continue
    alpha, beta = failureboosting(**i)
    with open(i['name'] + "-2.pkl", "wb") as f:
        pickle.dump([alpha, beta], f)

for i in toplot:
    with open(i['name'] + "-2.pkl", "rb") as f:
        alpha, beta = pickle.load(f)
        

workforonefailure = np.log2([ sqrt(a) * b**-1 for a,b in zip(alpha, beta)])
place = np.log2(beta[np.argmin(workforonefailure)])
print ('failure boosting cost: 2^' + str(min(workforonefailure)) + ' at DFR: 2^' + str(place))

