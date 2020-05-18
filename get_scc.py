from pathlib import Path
import os
import pandas as pd
import math as m

def fastMeanFilter():
    # to be implemented
    None

def vstran():
    # to be implemented
    None

def estSCC(dist):
    ffd1 = ffd2 = None

    for (i in 1:(ncol(smt_R1)-dist)):
        
        ffd1 = c(ffd1, smt_R1[i+dist, i])
        ffd2 = c(ffd2, smt_R2[i+dist, i])
        filt = which(ffd1 == 0 & ffd2 == 0)
        if (length(filt) == 0):
            ffd = cbind(ffd1, ffd2)
        else
            ffd = cbind(ffd1[-filt], ffd2[-filt])
    
    if (nrow(ffd) != 0):
        n = nrow(ffd)
        nd = vstran(ffd)
        
        if (length(unique(ffd[,1])) != 1 & length(unique(ffd[,2])) != 1):
            corr = cor(ffd[,1], ffd[,2])
            cov = cov(nd[,1], nd[,2])
            wei = sqrt(var(nd[,1])*var(nd[,2]))*n
        else:
            corr = None
            cov = None
            wei = None
    else:
        corr = None 
        cov = None
        wei = None

    return(list(corr = corr, wei = wei))

def getSCC(mat1, mat2, resol, h, lb):
if (h == 0):
    smt_R1 = mat1
    smt_R2 = mat2
else:
    smt_R1 = fastMeanFilter(mat1, h)
    smt_R2 = fastMeanFilter(mat2, h)

    lb = m.floor(lbr/resol)
    ub = m.floor(ubr/resol)
    corr = pd.Series(ub - lb + 1)
    cov = pd.Series(ub - lb + 1)
    wei = pd.Series(ub - lb + 1)
    n = pd.Series(ub - lb + 1)

    st = sapply(seq(lb,ub), est.scc)
    corr0 = unlist(st[1,])
    wei0 = unlist(st[2,])

    corr = corr0[!is.None(corr0)]
    wei = wei0[!is.None(wei0)]
    scc = corr %*% wei/sum(wei)
    std = sqrt(sum(wei^2*var(corr))/(sum(wei))^2)
  
    return(list(corr = corr, wei = wei, scc = scc, std = std))