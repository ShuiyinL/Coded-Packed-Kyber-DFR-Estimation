### DFR estimator of P-L Kyber
# This project uses codes from [Security Estimation Scripts for Kyber and Dilithium] in https://github.com/pq-crystals/security-estimates
# 

from math import log, exp, sqrt
from Kyber_failure import p2_cyclotomic_error_probability
from Kyber_failure import *
#from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
#from proba_util import build_mod_switching_error_law
#from proba_util import *
#py -m pip install scipy

import numpy as np
import scipy.io
#import matplotlib.pyplot as plt

class KyberParameterSet:
    def __init__(self, n, m, ks, ke,  q, rqk, rqc, rq2, ke_ct=None):
        if ke_ct is None:
            ke_ct = ke
        self.n = n
        self.m = m
        self.ks = ks     # binary distribution for the secret key
        self.ke = ke    # binary distribution for the ciphertext errors
        self.ke_ct = ke_ct    # binary distribution for the ciphertext errors
        self.q = q
        self.rqk = rqk  # 2^(bits in the public key)
        self.rqc = rqc  # 2^(bits in the first ciphertext)
        self.rq2 = rq2  # 2^(bits in the second ciphertext


def summarize(ps,LloydCu,LloydCv):
    print ("params: ", ps.__dict__)
    #print ("com costs: ", communication_costs(ps))
    F, f, Cu = p2_cyclotomic_error_probability(ps,LloydCu,LloydCv)
    #Recall the calculation of F: drop element of the support with proba less than 2^-400
    print ("failure: %.1f = 2^%.1f"%(f, 8+log(f + 2.**(-400))/log(2)))


def logdomain_sum(x, y):
    #Example: logdomain_sum(2, 3)= log(exp(2)+exp(3))
    if x<y:
        z=y+log(1+exp(x-y))
    else:
        z=x+log(1+exp(y-x))
            
    return z


def Chernoff_bound(F, decoding_r_square,theta,packed_size, MMSE_Q):
    #Lemma 6, return \delta_\ell for a given theta
    
    ma = max(F.keys())
    s_log=log(F.get(-ma,0))+theta*(ma*ma)

    #With MMSE quanization, the (LloydCu, LloydCv) are half integers, e.g.,
    #LloydCu={-1.5: 0.0772, -1: 0.2304, -0.5: 0.0772, 0:0.2304, 0.5: 0.0772, 1: 0.2304,  1.5:0.0772} #du=10
    #Therefore, the total decryption decoding noise are half integers

    if MMSE_Q==1:
        for i in (range(-int(2*ma)+2, int(ma*2))):
            s_log= logdomain_sum(s_log, log(F.get(i/2,0))+theta*pow(i/2, 2))
    else:
        for i in (range(-int(ma), int(ma))):
            s_log= logdomain_sum(s_log, log(F.get(i,0))+theta*pow(i, 2))
    
##            
    #Recall the calculation of F: drop element of the support with proba less than 2^-400
    delta =logdomain_sum((-theta*decoding_r_square+packed_size*s_log),-400*log(2))/log(2) 
    #delta =(-theta*decoding_r_square+packed_size*s_log)/log(2)
            
            
    return delta  


if __name__ == "__main__":
    # Parameter sets
    #ps_light = KyberParameterSet(256, 2, 3, 3, 3329, 2**12, 2**10, 2**4, ke_ct=2) #512
    #ps_recommended  = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**10, 2**4)   #768
    #ps_recommended  = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**11, 2**5)  #1024
   
    ## Choose variant of Kyber and (t, \ell, d_u,d_v)
    Kyber_type=3 #1:KYBER512; 2: KYBER768; 3: KYBER1024
    ##due to the strong errorr correction capability of lattice encoder, we can use smaller (d_u,d_v)
    du=11;
    dv=5;

    ## Lattice encoder available for \ell = 8 (E8 lattice), 16 (BW16 lattice), 24 (Leech lattice)
    packed_size=8 #\ell: number of packed ciphertext
    t_trunc=32;  #t: P_{t,\ell}-Kyber: (t=32,\ell=8) (1 AES key), (t=64,\ell=8) (2 AES keys)

    ## set MMSE_Q = 1 for MMSE q=quantization; MMSE_Q = 0 for original Kyber quantization
    MMSE_Q=1;

    if MMSE_Q == 0:
        print("Quantization Model: Original Kyber Quantization")
    else:
        print("Quantization Model: MMSE Quantization")
 
    
    if Kyber_type==1:
        Ktag="KYBER512"
        k=2
        ps_recommended = KyberParameterSet(256, 2, 3, 3, 3329, 2**12, 2**du, 2**dv, ke_ct=2)
    elif Kyber_type==2:
        Ktag="KYBER768"
        k=3
        ps_recommended  = KyberParameterSet(256, 3, 2, 2, 3329, 2**12, 2**du, 2**dv)   #768            
    else:
        Ktag="KYBER1024"
        k=4
        ps_recommended  = KyberParameterSet(256, 4, 2, 2, 3329, 2**12, 2**du, 2**dv)  #1024

    print("Parameters: %s with" % (Ktag), "du =", du, ", dv =", dv)
    print("packed_size =", packed_size)

    ## MMSE Qaunization Noise Distribution: DFR will be computed based on (LloydCu, LloydCv)
    if dv==6:
        mat_contents = scipy.io.loadmat('Cv6.mat')
    elif dv==5:
        mat_contents = scipy.io.loadmat('Cv5.mat')
    elif dv==4:
        mat_contents = scipy.io.loadmat('Cv4.mat')
    elif dv==3:
        mat_contents = scipy.io.loadmat('Cv3.mat')

    LloydCv = dict(zip(mat_contents['Ll_range'].flatten(), mat_contents['pmf_Ll'].flatten()))

        

    if du==11:
        mat_contents_2 = scipy.io.loadmat('Cu11.mat')
    elif du==10:
            mat_contents_2 = scipy.io.loadmat('Cu10.mat')
    elif du==9:
            mat_contents_2 = scipy.io.loadmat('Cu9.mat')
            
    LloydCu = dict(zip(mat_contents_2['Ll_range'].flatten(), mat_contents_2['pmf_Ll'].flatten()))
  

    ## Examples of LloydCu
    #LloydCu={-0.5:0.3848,0:0.2304 ,0.5:0.3848} #du=11
    #LloydCu={-1.5: 0.0772, -1: 0.2304, -0.5: 0.0772, 0:0.2304, 0.5: 0.0772, 1: 0.2304,  1.5:0.0772} #du=10
    ## Obtain the decryption noise distribtuin: F; the uncoded DFR with \ell=1: f
    #summarize(ps_recommended,LloydCu,LloydCv)
    F, f, Cu = p2_cyclotomic_error_probability(ps_recommended, LloydCu, LloydCv, MMSE_Q)


    ## Output the DFR of uncoded P_{\ell} Kyber
    print("Uncoded P_{%d}-%s: DFR = %d, Plaintext size = %d bytes, CER =%f" % (packed_size, Ktag, logdomain_sum(log(f),-400*log(2))/log(2)+8+log(packed_size)/log(2), packed_size*32, (du*k+packed_size*dv)/packed_size))
 

    ############### Lemma 6: DFR of P_{\ell} Kyber via Chernoff Bound
    Encoder_List=[8,16,24] #\ell=8: E8 lattice, \ell=16: BW16 lattice, \ell=24: Leech lattice
    K_p_List=[8,20,36]  #num of information bits per latice codeword, see Table 5 

    ## Lattice encoder available for \ell = 8 (E8 lattice), 16 (BW16 lattice), 24 (Leech lattice)
    if packed_size in Encoder_List: 

        #Initial values 
        delta_packed=1
        step_theta=0.000001
        decoding_r_square=pow(round(3329/4)*sqrt(2),2)

        #search the best theta
        for i in (range(1, 10000000)): 
           
            tempt=Chernoff_bound(F, decoding_r_square, i*step_theta,packed_size,MMSE_Q)
            if  delta_packed > tempt:
                delta_packed =tempt
                theta_opt=i*step_theta

            if tempt > delta_packed+5:
                break

        delta_packed=delta_packed+8 #log2(n)=8, union bound    
        print("Coded P_{%d}-%s: DFR = %d, Plaintext size = %d bytes, CER =%f" % (packed_size, Ktag, delta_packed, K_p_List[Encoder_List.index(packed_size)]*32, (du*k+packed_size*dv)/K_p_List[Encoder_List.index(packed_size)]))
        
        ## DFR of P(t,\ell)-Kyber: \ell=8, t=32 or 64
        if t_trunc==32 and packed_size ==8 and Kyber_type==3:
            print("P_{%d,%d}-%s: DFR = %d, Plaintext size = %d bytes, CER =%f" % (t_trunc, packed_size, Ktag, delta_packed-3, t_trunc, du*k+dv))
        elif t_trunc==64 and packed_size ==8:
            print("P_{%d,%d}-%s: DFR = %d, Plaintext size = %d bytes, CER =%f" % (t_trunc, packed_size, Ktag, delta_packed-2, t_trunc, (du*k+2*dv)/2))
        

        print("theta_opt =", theta_opt)

       
##    ## Plot the decryption decoding noise distribution
##    width = 1.0
##    plt.bar(F.keys(), F.values(), color='g')
##
##    plt.ylim((min(F.values()),max((F.values()))))
##    #plt.yscale('log')
##
##    plt.autoscale(True, axis = 'both')
##    plt.title("Probability Mass Function of Decoding Noise Coefficient")
##    #plt.hist(F.keys(), F.values())
##    #plt.yscale('log')
##    #plt.gca().set_yticks([pow(10,-5), pow(10,-4), pow(10,-3), pow(10,-2),pow(10,-1)])
##    #plt.gca().set_yticks([pow(10,-4), pow(10,-3), pow(10,-2),pow(10,-1)])
##
##    plt.show()
##
##    ## Save the decoding noise distribution
##    arrF = np.array(list(F.values()))
##    scipy.io.savemat('F.mat', {'F':arrF})
##    #savemat('F.mat', {'F':arrF})

    
    print ()
