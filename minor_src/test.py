from numpy import *
import serial, time
from datetime import datetime, timedelta
import os
from netCDF4 import Dataset


loc_lat = 1
loc_lon = 1
loc = "test"

commit_message = "'Data dump for test location'"

fname = "../data/file.txt"
dat = "../data/cool_data.csv"

header = open(dat).readline().split(",")
data = loadtxt(dat, dtype=str, unpack=True, skiprows=1, delimiter=",")

def github():
    add     = os.system("git add {}".format(fname))
    commit  = os.system("git commit -m {}".format(commit_message))
    push    = os.system("git push origin auto")
    add
    commit
    push

def iter_dat(str):
    list = []
    for i in range(len(header)):
        if str in header[i]:
            list.append(data[i])
    return list

def write_netcdf():
    try: ncfile.close()
    except: pass

    ncfile     = Dataset(fname.replace(".txt", ".nc"), mode='w')

    ncfile.title    = "Dataset for {}".format(loc)
    ncfile.subtitle = "Subtitle"


    lat_dim    = ncfile.createDimension('lat', loc_lat)
    lon_dim    = ncfile.createDimension('lon', loc_lon)
    time_dim   = ncfile.createDimension('time', None)


    lat             = ncfile.createVariable('lat', float32, ('lat', ))
    lat.units       = "degrees_north"
    lat.long_name   = "latitude"

    lon             = ncfile.createVariable('lon', float32, ('lon', ))
    lon.units       = "degrees_east"
    lon.long_name   = "longitude"

    ele             = ncfile.createVariable('ele', float32, ('ele', ))
    ele.units       = "meters above sea level"
    ele.long_name   = "Surface Elevation"

    time            = ncfile.createVariable('time', float64, ('time', ))
    time.units      = "hours since 1800-01-01"
    time.long_name  = "time"

    air_temp            = ncfile.createVariable('air_temp', float64, ('time', 'time'))
    air_temp.units      = "C"
    air_temp.standard_name = "air_temperature"

    air_temp[:,:] = iter_dat("(Sky)")

    std_temp            = ncfile.createVariable('std_temp', float64, ('time', 'time'))
    std_temp.units      = "C"
    std_temp.standard_name = "standardized_temperature"

    std_dat = []
    for i in range(len(header)):
        if "(Ground)" in header[i] or "(Standard)" in header[i]:
            std_dat.append(data[i])

    std_temp[:,:] = array(std_dat)
    ncfile.close()
write_netcdf()
