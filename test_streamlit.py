import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import tifffile as tf
from pathlib import Path
import mpld3
import streamlit.components.v1 as components
from utils import load_normalize_HH_HV
from datetime import datetime, timedelta
import glob
from PIL import Image

# -------------------------------------------------------------
plt.close('all')

st.title('Near-real time automated sea ice mapping from space')

st.header('Areas of interest', divider='blue')
image_AOI = Image.open('/home/cirfa/work/projects/streamlit/AOIs/overview_AOIs.png')
st.image(image_AOI, caption='Overview map showing areas of interest')

st.header('Ice-Water maps from Sentinel-1 SAR imagery', divider='blue')

# select AOI
area = st.selectbox(
    'Select area of interest',
    ('-', '[1] - Fram Strait', '[2] - Barents Sea'))

# select day
day = st.selectbox(
    'Select day',
    ('-', 'today', 'yesterday'))

# define image directory
feat_dir = Path('/media/cirfa/CIRFA_media/CNN_training_Catherine/inference_features')
results_dir = Path('/media/cirfa/CIRFA_media/CNN_training_Catherine/inference_results')

if area == '[2] - Barents Sea':
    if day == 'today':
        # define today's date
        date = datetime.now().strftime('%Y%m%d')
        #print(f'Looking for S1 images on: {date}')
        
        # for testing, hardcode date of test image
        date = '20201201'
        # get list of all S1 images on this date
        S1_basename_list = glob.glob((feat_dir / f'*{date}*').as_posix())
        
        if S1_basename_list == []:
            st.write('No S1 imagery on this date')
        
        else:
            # loop over all S1 images found for this date
            for S1_feat_path in S1_basename_list:
                # convert string to Pathlib path
                S1_feat_path = Path(S1_feat_path)
                # get S1 basename
                S1_basename = S1_feat_path.stem
                st.write(f'Processing {S1_basename} ...')
                
                # construct paths to HH and HV features 
                HH_filename = 'Sigma0_HH_NERSC_db_float16.tif'
                HH_path = S1_feat_path / HH_filename
                
                HV_filename = 'Sigma0_HV_NERSC_db_float16.tif'
                HV_path = S1_feat_path / HV_filename
    
                # load features into memory + normalize for plotting
                sigma0_hh_normalized, sigma0_hv_normalized = load_normalize_HH_HV(HH_path, HV_path)    
            
                # path to classified image
                classified_image_filename = f'{S1_basename}_labels_UNET_trained_NERSC_50.tif'
                classified_image_path = results_dir / S1_basename / classified_image_filename
            
                # import classified image
                classified_image = tf.imread(classified_image_path)[::4, ::4]
    
                # -----------------------------------------------------------------
                ### PLOT ###
                
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
                fig.suptitle(f'{S1_basename}')
                
                axes[0].imshow(sigma0_hh_normalized, cmap='gray')
                axes[0].set_title('Sigma0 HH')
                axes[0].set_ylabel('Distance [km]')
                axes[0].set_xlabel('Distance [km]')
                
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
                cbar.ax.tick_params(rotation=-35)
                
                #plt.show()
                
                st.pyplot(fig)
                
                # # # make interactive plot
                # fig_html = mpld3.fig_to_html(fig)
                # components.html(fig_html, height=500)
                
                #plt.close('all')
        
        
    if day == 'yesterday':
        st.write('Not implemented yet - try again later!')
        
        # define date of yesterday
        yesterday = datetime.now() - timedelta(1)
        yesterday = yesterday.strftime('%Y%m%d')
        print(f'Looking for S1 images on {yesterday}')
        
if area == '[1] - Fram Strait':
    st.write('Not implemented yet - try again later!')



