from proba_util import *
from proba_util2 import *
from math import sqrt
import scipy.io


# P-Kyber: lattice encoder + MMSE quantization
P_Kyber768 = {}
P_Kyber768['thres'] = 3329 / 2**2 #lower bound for E8 lattice
P_Kyber768['s'] = build_centered_binomial_law(2)
#MMSE quantization noise for u
u ={-1.5: 0.0772, -1: 0.2304, -0.5: 0.0772, 0:0.2304, 0.5: 0.0772, 1: 0.2304,  1.5:0.0772}
#u = build_mod_switching_error_law(3329, 2**10) #Original Kybe quantization noise for u
P_Kyber768['e'] = P_Kyber768['s'] #The public key remain uncompressed
#Kyber768['e'] = law_convolution(Kyber768['s'], u)

P_Kyber768['sprime'] = P_Kyber768['s']
P_Kyber768['eprime'] = law_convolution(P_Kyber768['s'], u)

#MMSE quantization noise for v
mat_contents = scipy.io.loadmat('Cv4.mat')
u2 = dict(zip(mat_contents['Ll_range'].flatten(), mat_contents['pmf_Ll'].flatten()))
#u2 = build_mod_switching_error_law(3329, 2**4) # original Kybe quantization noise for v
P_Kyber768['eprimeprime'] = law_convolution(P_Kyber768['s'], u2)
P_Kyber768['n'] = 256 * 3
P_Kyber768['n2'] = 256
P_Kyber768['name'] = 'P_Kyber768'


P_Kyber1024 = {}
P_Kyber1024['thres'] = 3329 / 2**2 #lower bound for E8 lattice
P_Kyber1024['s'] = build_centered_binomial_law(2)
#MMSE quantization noise for u
u={-0.5:0.3848,0:0.2304 ,0.5:0.3848} 
#u = build_mod_switching_error_law(3329, 2**11) #Original Kybe quantization noise for u

P_Kyber1024['e']=P_Kyber1024['s'] #The public key remain uncompressed
#Kyber1024['e'] = law_convolution(Kyber1024['s'], u)

P_Kyber1024['sprime'] = P_Kyber1024['s']
P_Kyber1024['eprime'] = law_convolution(P_Kyber1024['s'], u)

#MMSE quantization noise for v
mat_contents = scipy.io.loadmat('Cv5.mat')
u2 = dict(zip(mat_contents['Ll_range'].flatten(), mat_contents['pmf_Ll'].flatten()))
#u2 = build_mod_switching_error_law(3329, 2**5) #original Kybe quantization noise for v

P_Kyber1024['eprimeprime'] = law_convolution(P_Kyber1024['s'], u2)
P_Kyber1024['n'] = 256 * 4
P_Kyber1024['n2'] = 256
P_Kyber1024['name'] = 'P_Kyber1024'


# Latest version of Kyber
Kyber768 = {}
Kyber768['thres'] = 3329 / 2**2
Kyber768['s'] = build_centered_binomial_law(2)
u = build_mod_switching_error_law(3329, 2**10) #original Kybe quantization noise for u
Kyber768['e'] = Kyber768['s'] #In the latest version, public key remain uncompressed
#Kyber768['e'] = law_convolution(Kyber768['s'], u)
Kyber768['sprime'] = Kyber768['s']
Kyber768['eprime'] = law_convolution(Kyber768['s'], u)
u2 = build_mod_switching_error_law(3329, 2**4) # original Kybe quantization noise for v
Kyber768['eprimeprime'] = law_convolution(Kyber768['s'], u2)
Kyber768['n'] = 256 * 3
Kyber768['n2'] = 256
Kyber768['name'] = 'Kyber768'


Kyber1024 = {}
Kyber1024['thres'] = 3329 / 2**2
Kyber1024['s'] = build_centered_binomial_law(2)
u = build_mod_switching_error_law(3329, 2**11)
Kyber1024['e']=Kyber1024['s']
#Kyber1024['e'] = law_convolution(Kyber1024['s'], u)
Kyber1024['sprime'] = Kyber1024['s']
Kyber1024['eprime'] = law_convolution(Kyber1024['s'], u)
u2 = build_mod_switching_error_law(3329, 2**5)
Kyber1024['eprimeprime'] = law_convolution(Kyber1024['s'], u2)
Kyber1024['n'] = 256 * 4
Kyber1024['n2'] = 256
Kyber1024['name'] = 'Kyber1024'


