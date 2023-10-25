#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:19:30 2023

@author: cirfa
"""
import tifffile as tf
import numpy as np

def load_normalize_HH_HV(HH_path, HV_path):
    # import HH and HV features, downsample with factor 2
    sigma0_hh = tf.imread(HH_path)[::4, ::4]
    sigma0_hv = tf.imread(HV_path)[::4, ::4]
    
    # -----------------------------------------------------------------
    # normalize Sigma0 HH and HV data for visualization
    
    def normalize(X, new_min, new_max):
            # normalize array X in range (new_min, new_max)
    
            # find nan percentiles of array X
            Xmin = np.nanpercentile(X , 0.1)
            Xmax = np.nanpercentile(X , 99.9)
    
            # clip min-max values of X
            X[X<Xmin] = Xmin
            X[X>Xmax] = Xmax
    
            # scale X to new range
            X_scaled = (X - Xmin) / (Xmax - Xmin) * (new_max - new_min) + new_min
    
            return X_scaled
    
    sigma0_hh_normalized = normalize(sigma0_hh, 0, 255)
    sigma0_hv_normalized = normalize(sigma0_hv, 0, 255)
    
    return sigma0_hh_normalized, sigma0_hv_normalized