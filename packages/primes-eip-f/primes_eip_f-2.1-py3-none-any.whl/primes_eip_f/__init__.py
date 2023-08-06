#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:14:22 2021

@author: feemjo
"""

import rpy2.robjects as ro


def es_primo(n):
    res = True
    for i in range(2,n):
        if(n%i==0):
            res=False
    return res

def numeros_primos(n):
    for i in range(2, n):
        if(es_primo(i)):
            print("El numero", i, "es primo")

primos_r = """
primos <- function(n){
    print("Numeros primos")
    for(i in 2:n){
        res<-TRUE
        for(j in 2:i){
            if(i%%j==0 && j!=i){
                res<-FALSE
            }
        }
        if(res==TRUE){
            print(i)
        }
    }
}
"""
def numeros_primos_r(n):
    ro.r(primos_r)
    primos_py = ro.globalenv['primos']
    primos_py(n)