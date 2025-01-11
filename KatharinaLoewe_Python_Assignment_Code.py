# This program reads from an ERA5 netcdf file (ERA5_2mT_SST_CBH.nc, reanalysis-era5-single-levels from 27.05.2023) the variable 2 m temperature at a ceratin geolocation. 
# Longitude (37 steps, 0 - 9°) and latitude (194 steps, 0 - 48.25°) have an increment of 0.25°. Time steps are hourly starting by 00:00 ending at 23:00 UTC (24 steps).
# 
# You can adjust the variables lon (longitude) and lat (latidute) and 
# the ERA5_2mT_SST_CBH.nc should be in the same folder with KatharinaLoewe_Python_Assignment_Code.py.
#
# Check requirements.txt before running the program.
#
# Reference data file: 
# Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2023): ERA5 hourly data on single levels from 1940 to present. 
# Copernicus Climate Change Service (C3S) Climate Data Store (CDS), DOI: 10.24381/cds.adbb2d47 (Accessed on 18-12-2024)
# 
# Author: Katharina Loewe, https://orcid.org/0000-0003-3574-7203
# Date: 11.01.2025

# clear variables
for name in dir():
    if not name.startswith('_'):
        del globals()[name]

# import needed libraries
import matplotlib.pyplot as plt
import numpy as np
from datetime  import datetime, timezone
import netCDF4 as nc


# -----------------------------------
# main
# -----------------------------------
# read and import data (netcdf file)
# ------------------------------------

file_path = 'ERA5_2mT_SST_CBH.nc'

# open data set
dataset = nc.Dataset(file_path, 'r')

# Read data variables 
variablename_T2m = 't2m'
variable_T2m_data = dataset.variables[variablename_T2m]

# Find out dimensions
print("No. of timesteps of T2m")
print(np.size(variable_T2m_data, 0))

print("No. of latitude steps of T2m")
print(np.size(variable_T2m_data, 1))

print("No. of longitude steps of T2m")
print(np.size(variable_T2m_data, 2))

# store lon, lat and time in an array
variabletime_name ='valid_time'
variablelat_name ='latitude'
variablelon_name ='longitude'

time_array = dataset.variables[variabletime_name][:]
new_time_array = np.array(time_array)
lat_array = dataset.variables[variablelat_name][:]
new_lat_array = np.array(lat_array)
lon_array = dataset.variables[variablelon_name][:]
new_lon_array = np.array(lon_array)

#----------------------------------------------
# Functions
#----------------------------------------------
# Create arrays for a variable of the data set at a certain geolocation
def var_arrays(lon,lat,variable_x_data):
    var_x = variable_x_data[:,lat,lon]
    new_var_x = var_x.reshape(-1)
    return new_var_x

# Convert Kelvin in Degree Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Function to convert epoch seconds to formatted date string with hours
def convert_epoch_to_date(epoch_seconds):
  return [datetime.fromtimestamp(ts, timezone.utc).strftime('%H:%M:%S') for ts in epoch_seconds]

#--------------------------------------------
# Analyzing
#--------------------------------------------
# Choose one lon lat position for analyzing

lat = 2
lon = 33

# create array at certain geolocation
T2m_time = var_arrays(lon,lat, variable_T2m_data)

# convert kelvin in degrees Celcius
T2m_time_Celsius = kelvin_to_celsius(T2m_time)

# find temperatures over 25°C at location lon, lat
cnt_hot = 0
for i_T2m in T2m_time_Celsius:
    if i_T2m >= 30:
        cnt_hot = cnt_hot + 1
        
print("Number of hot 2 m temperatures during the day",cnt_hot)

# ---------------------------------
# plot
# ---------------------------------
# prepare time axes, format

epoch_seconds = new_time_array

# Convert the time array
formatted_dates = convert_epoch_to_date(epoch_seconds)

#------------------------------------
# plot 2 m temperature over time

plt.plot(formatted_dates,T2m_time_Celsius, marker='o', linestyle = '--', color='purple')
plt.xlabel('Time (UTC)')
plt.ylabel('Temperature (°C)')
plt.title(f'Temperature on 27.05.2023 at longitute {lon_array[lon]}° and latitude {lat_array[lat]}°')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid()
plt.show()

