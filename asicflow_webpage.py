import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import glob
from PIL import Image

# streamlit run asicflow_webpage.py --server.fileWatcherType none

# ------------------------------------------------------------- # 
# DEFINE DATA DIRECTORY

# path to main directory with images (pngs) to plot on webpage
DATA_DIR = Path('./image_database')

# ------------------------------------------------------------- # 
# ------------------------------------------------------------- # 
# BUILD WEBPAGE

user_input = False

st.set_page_config(
    page_title="CIRFA demo",
    page_icon=":cold_face:",
    layout="centered",
    menu_items={
        'Get help': None,
        'Report a bug': "mailto:catherine.c.taelman@uit.no",
        'About': "CIRFA demo, more about CIRFA: https://cirfa.uit.no"
    }
)

# title
st.title('Near-real time automated sea ice mapping')

# ------------------------------------------------------------- # 
# show AOI map
st.header('Areas of interest', divider='blue')

# define path to AOI overview map
image_AOI_path = DATA_DIR / 'overview_AOIs.png'
image_AOI = Image.open(image_AOI_path.as_posix())

# display AOI map on webpage
st.image(image_AOI, caption='Overview areas of interest')

# ------------------------------------------------------------- # 
# define timestamps 

# define today's date
crrt_date = datetime.now().strftime("%d/%m/%Y")

# define previous 6 days
crrt_date_min_1 = (datetime.now() - timedelta(1)).strftime("%d/%m/%Y")
crrt_date_min_2 = (datetime.now() - timedelta(2)).strftime("%d/%m/%Y")
crrt_date_min_3 = (datetime.now() - timedelta(3)).strftime("%d/%m/%Y")
crrt_date_min_4 = (datetime.now() - timedelta(4)).strftime("%d/%m/%Y")
crrt_date_min_5 = (datetime.now() - timedelta(5)).strftime("%d/%m/%Y")
crrt_date_min_6 = (datetime.now() - timedelta(6)).strftime("%d/%m/%Y")

# ------------------------------------------------------------- # 
# create toggle-down menus for area and time selection (user input)

# select AOI
area = st.selectbox(
    'Select area of interest',
    ('-', '[1] - Fram Strait', '[2] - Barents Sea'))

# select day
day = st.selectbox(
    'Select day',
    ('-', 
     f'{crrt_date}', 
     f'{crrt_date_min_1}',
     f'{crrt_date_min_2}',
     f'{crrt_date_min_3}',
     f'{crrt_date_min_4}',
     f'{crrt_date_min_5}',
     f'{crrt_date_min_6}',
     ))

# ------------------------------------------------------------- # 
# convert human-readable timestamp into S1 datetime format (YYYYmmdd)

if day != '-':
    
    date_S1 = datetime.strptime(f"{day}", "%d/%m/%Y").strftime('%Y%m%d')
    
    user_input=True
    
elif day == '-':
    user_input=False
    
# ------------------------------------------------------------- # 
# configure area results directory based on user input

if area == '[1] - Fram Strait':
    
    aoi = 'Fram Strait'
    
    # path to pngs for Fram Strait
    figure_dir = DATA_DIR / 'Fram_Strait'

elif area == '[2] - Barents Sea':
    
    aoi = 'Barents Sea'
    
    # path to pngs for Barents Sea
    figure_dir = DATA_DIR / 'Barents_Sea'

elif area == '-':
    user_input=False
        
# ------------------------------------------------------------- # 
# GRAB RESULTS FROM DISK AND FORWARD TO WEBPAGE

if user_input:

    st.header('Results', divider='blue')
     
    # get list of all S1 images on specified date
    S1_basename_list = glob.glob((figure_dir / f'*{date_S1}*').as_posix())
    
    
    if S1_basename_list == []:
        st.write('No Sentinel-1 imagery / results found on this date')
    
    else:
        nr_products = len(S1_basename_list)
        st.subheader(f'Found {nr_products} Sentinel-1 products for {aoi} on {day}!')
        
        # loop over all S1 images found for this date
        for S1_path in S1_basename_list:
            
            S1_path = Path(S1_path)
            # grab S1 basename
            S1_basename = S1_path.stem
            st.markdown(f'**Visualizing {S1_basename}**')
        
            # load HH and HV intensity images
            HH_HV_intensities_path = S1_path / 'S1_intensities_on_map.png'
            HH_HV_intensities = Image.open(HH_HV_intensities_path.as_posix())
            
            # load classification result
            classification_result_path = S1_path / 'classification_result_on_map.png'
            classification_result = Image.open(classification_result_path.as_posix())
            
            # display images on webpage
            st.image(HH_HV_intensities, caption= 'Sentinel-1 backscatter intensities in dB')
            st.image(classification_result, caption= f'Classification result for {S1_basename}')
    
            st.divider()




