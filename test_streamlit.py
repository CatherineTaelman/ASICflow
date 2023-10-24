import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import tifffile as tf
from pathlib import Path
import mpld3
import streamlit.components.v1 as components

plt.close('all')

st.title('Near-real time automated sea ice mapping from space')
st.header('Ice-Water maps from Sentinel-1 SAR image', divider='blue')

# select AOI
area = st.selectbox(
    'Select area of interest',
    ('-', 'Fram Strait', 'Barents Sea', 'Northern Greenland'))

# select day
day = st.selectbox(
    'Select day',
    ('-', 'today', 'yesterday'))

# define image directory
feat_dir = Path('/media/cirfa/CIRFA_media/CNN_training_Catherine/inference_features')
results_dir = Path('/media/cirfa/CIRFA_media/CNN_training_Catherine/inference_results')

if area == 'Barents Sea' and day == 'today':
    S1_name = 'S1A_EW_GRDM_1SDH_20201201T070428_20201201T070533_035489_04261E_5EA0'
    # path to HH and HV features
    HH_filename = 'Sigma0_HH_NERSC_db_float16.tif'
    HH_path = feat_dir / S1_name / HH_filename
    HV_filename = 'Sigma0_HV_NERSC_db_float16.tif'
    HV_path = feat_dir / S1_name / HV_filename
    
    # path to classified image
    classified_image_filename = 'S1A_EW_GRDM_1SDH_20201201T070428_20201201T070533_035489_04261E_5EA0_labels_UNET_trained_NERSC_50.tif'
    classified_image_path = results_dir / S1_name / classified_image_filename
    
if area == 'Fram Strait':
    st.write('Not implemented yet - try again later!')
    
if area == 'Northern Greeland':
    st.write('Not implemented yet - try again later!')
 
if area == 'Barents Sea' and day == 'today':
    # path to HH and HV features
    HH_filename = 'Sigma0_HH_NERSC_db_float16.tif'
    HH_path = feat_dir / S1_name / HH_filename
    HV_filename = 'Sigma0_HV_NERSC_db_float16.tif'
    HV_path = feat_dir / S1_name / HV_filename
    
    # path to classified image
    classified_image_filename = 'S1A_EW_GRDM_1SDH_20201201T070428_20201201T070533_035489_04261E_5EA0_labels_UNET_trained_NERSC_50.tif'
    classified_image_path = results_dir / S1_name / classified_image_filename
    
    # import HH and HV features
    sigma0_hh = tf.imread(HH_path)
    sigma0_hv = tf.imread(HV_path)
    
    # import classified image
    classified_image = tf.imread(classified_image_path)
    
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
    # -----------------------------------------------------------------
    # prepare colormap
    class_colors = [
            'black',       # 0 - background 
            'royalblue',   # 1 - Open Water
            'whitesmoke'   # 2 - Sea Ice
            ]
    
    cmap = mpl.colors.ListedColormap(class_colors)
    
    # define level boundaries for colormap
    cmap_bounds = np.arange(0, len(class_colors)+1, 1)
    cmap_values = np.convolve(cmap_bounds, np.ones(2)/2, mode='valid').astype(int)
    
    # build a colormap index based on level boundaries
    cmap_norm = mpl.colors.BoundaryNorm(cmap_bounds, cmap.N)
    
    # build legend/labels for colorbar
    legend_entries = ['No Data', 'Open Water', 'Sea Ice']
    
    # -----------------------------------------------------------------
    # make figure
    fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12,6))
    axes = axes.ravel()
    fig.suptitle(f'{S1_name}')
    
    axes[0].imshow(sigma0_hh_normalized, cmap='gray')
    axes[0].set_title('Sigma0 HH')
    axes[0].set_ylabel('Distance [km]')
    axes[0].set_xlabel('Distance [km]')
    axes[0].set_xticks([0, 2500, 5000, 7500, 10000], ['0','100','200', '300', '400'])
    axes[0].set_yticks([0, 2500, 5000, 7500, 10000], ['0','100','200', '300', '400'])
    
    axes[1].imshow(sigma0_hv_normalized, cmap='gray')
    axes[1].set_title('Sigma0 HV')
    axes[1].set_xlabel('Distance [km]')
    
    s = axes[2].imshow(classified_image,  cmap=cmap, norm = cmap_norm, interpolation='nearest')
    axes[2].set_title('Classification result')
    axes[2].set_xlabel('Distance [km]')
    
    cbar = fig.colorbar(
      s,
      ax = axes,
      ticks = cmap_values + 0.5,
      shrink = 0.5
    )
    cbar.set_ticklabels(legend_entries)
    cbar.ax.tick_params(rotation=-45)
    
    #plt.show()
    
    st.pyplot(fig)
    
    # # make interactive plot
    #fig_html = mpld3.fig_to_html(fig)
    #components.html(fig_html, height=800)
    #plt.close('all')