####
## Title: 	Precipitable Water Data Extraction Module
## Author: 	Spencer Riley / Vicki Kelsey
## Documentation Page: https://git.io/fjVHo
####
import os
import csv
import sys
import requests
from numpy import *
import pandas as pd

import time
import datetime
from datetime import date as dte
from datetime import datetime as dt

from metpy.units import units
from siphon.simplewebservice.wyoming import WyomingUpperAir

from mesowest import MesoWest

from rich import print, box
from rich.panel import Panel
from rich.table import Table
from rich.progress import track

from rich.progress import BarColumn, TextColumn, TimeRemainingColumn, Progress, track

progress = Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    TimeRemainingColumn())
progress.print(Panel(
    "[bold deep_sky_blue2]Good Morning\nWelcome to the Data Extraction Module of the Precipitable Water Model. For more information about the model and the purpose of this tool, please visit the [link=https://git.io/fj5Xr]documentation page[/link]"))

## Timeout Retry
REQUESTS_MAX_RETRIES = int(os.getenv("REQUESTS_MAX_RETRIES", 10))
adapter = requests.adapters.HTTPAdapter(max_retries=REQUESTS_MAX_RETRIES)

## Imports Wyoming and MesoWest Site IDs
config = "../../data/import.conf"
cnfg = loadtxt(config, dtype=str, delimiter=":")

## Imports Sensor information
instr = "../../data/instruments.conf"
intr = loadtxt(instr, dtype=str, delimiter=",", unpack=True)[0]
## Data file used for model input
fname = '../../data/master_data.csv'
## Data file used for user input
wname = '../../data/cool_data.csv'

## Stations used
wy_station = cnfg[1][1].split(",")
mw_station = cnfg[0][1].split(",")
## Hours to pull
hour = [00, 12]

## Retrives column index for sensors
headr = pd.read_csv(wname, delimiter=",").columns
indx = [[], []]
for i in range(len(headr)):
    if "Sky" in headr[i]:
        indx[0].append(i)
    elif "Ground" in headr[i] or "Standard" in headr[i]:
        indx[1].append(i)


## A function that computes the closest value
def closest(lst, K, d):
    lst = asarray(lst)
    list = []
    tmp2 = dt.combine(d, K)
    for i in range(len(lst)):
        list.append(abs(dt.combine(d, lst[i]) - tmp2))
    idx = asarray(list).argmin()
    return lst[idx]


## Imports Wyoming Data for specified site and date
def wyoming_import(end_date, station):
    try:
        df_12 = WyomingUpperAir.request_data(dt.combine(end_date, datetime.time(12, 0)), station)
        pw12 = df_12.pw[0]
    except (ValueError, IndexError):
        pw12 = "NaN"
    except requests.exceptions.HTTPError:
        pw12 = "Error"
    try:
        df_00 = WyomingUpperAir.request_data(end_date + datetime.timedelta(days=1), station)
        pw00 = df_00.pw[0]
    except (ValueError, IndexError):
        pw00 = "NaN"
    except requests.exceptions.HTTPError:
        pw00 = "Error"
    return [station, [end_date, pw12, pw00]]


def mesowest_import(end_date, station, in_time):
    df_mw = MesoWest.request_data(end_date + datetime.timedelta(days=1), station.strip(" "))
    mw_header = df_mw.columns
    for i in range(len(mw_header)):
        if "time(" in mw_header[i]:
            tau = i
        else:
            continue

    if (str(in_time) in ['00:00:00', 'NaT']) or (str(df_mw[mw_header[tau]][0]) == 'NaT'):
        rh = "NaN"
        temp = "NaN"
        thyme = "NaT"
    else:
        df_tm = df_mw.loc[(df_mw[mw_header[tau]] == closest(df_mw[mw_header[tau]], in_time, end_date))]

        thyme = df_tm[mw_header[tau]].values[0]
        rh = df_tm['relative_humidity'].values[0]
        temp = round((float(df_tm['temperature'].values[0]) * units.degF).to(units.degC).magnitude, 2)

        if str(rh) == "nan":
            rh = "NaN"
        if str(temp) == "nan":
            temp = "NaN"
    return [thyme, rh, temp]


def impt(end_date, idx):
    cool_data = []
    with filew as csvfile:
        next(csv.reader(csvfile, delimiter=","))
        for row in readw:
            sky = [[] for _ in range(len(indx[0]))]
            gro = [[] for _ in range(len(indx[1]))]
            mtime = row[1].split('/')
            condition = row[2].split('/')
            for j in range(len(indx[0])):
                sky[j] = row[indx[0][j]].split('/')
            for k in range(len(indx[1])):
                gro[k] = row[indx[1][k]].split('/')
            comments = row[-1].split('/')
            cool_data.append([mtime, condition, sky, gro, comments])
    i = 0
    wy_data = []
    for j in wy_station:
        i = 0
        wy_out = wyoming_import(end_date, j.strip(" "))
        while "Error" in wy_out[1]:
            progress.console.log("[bold yellow] (001) Wyoming Sever Disconnected")
            time.sleep(100)
            wy_out = wyoming_import(end_date, j.strip(" "))
            i = + 1
        wy_data.append(wy_out)

    neat = []
    for i in range(idx, idx + 1):
        neat.append(cool_data[i])
    neat = neat[::-1]

    mw_data = []
    for j in mw_station:
        mw_data.append(mesowest_import(end_date, j, pd.to_datetime(neat[0][0][0]).time()))

    if str(neat[0][0][0]) == "00:00":
        fin_tme = "NaT"
    else:
        fin_tme = neat[0][0][0]

    d = {'Date': end_date.strftime("%-m/%-d/%Y"),
         'Condition': neat[0][1][0],
         'Time': fin_tme}
    for i in range(len(mw_data)):
        if str(mw_data[i][0]) == "NaT":
            d[str(mw_station[i]).strip(" ") + "_" + "Time"] = "NaT"
        else:
            d[str(mw_station[i]).strip(" ") + "_" + "Time"] = mw_data[i][0].strftime("%H:%M")
        d[str(mw_station[i]).strip(" ") + "_" + "RH"] = mw_data[i][1]
        d[str(mw_station[i]).strip(" ") + "_" + "Temp"] = mw_data[i][2]
    for i in range(len(wy_data)):
        d["PW " + str(wy_station[i]).strip(" ") + "_" + "12Z"] = wy_data[i][1][1]
        d["PW " + str(wy_station[i]).strip(" ") + "_" + "00Z"] = wy_data[i][1][2]
    for i in range(len(sky)):
        d[str(headr[indx[0]][i])] = neat[0][2][i]
    for i in range(len(gro)):
        d[str(headr[indx[1]][i])] = neat[0][3][i]
    d["comments"] = str(neat[0][4][0])
    out = pd.DataFrame(d)

    if os.stat(fname).st_size == 16:
        out.to_csv(fname, index=False, header=True)
    else:
        out.to_csv(fname, index=False, mode="a", header=False)


full_len = len(loadtxt(wname, delimiter=",", dtype=str, usecols=0)) - 1
try:

    last = list(loadtxt(wname, delimiter=",", dtype=str, usecols=0)).index(
        str(loadtxt(fname, delimiter=",", dtype=str, usecols=0)[-1]))
except IndexError:
    last = 0
with progress:
    progress.log("[bold white]Script Started")
    task_id = progress.add_task("download", filename="Data Import")
    for i in range(last, full_len - 1):
        filew = open(wname, "r")
        readw = csv.reader(filew, delimiter=",")
        impt(dt.strptime(str(loadtxt(wname, delimiter=",", dtype=str, usecols=(0))[i + 1]), "%m/%d/%Y"), i)
        progress.update(task_id, advance=(100. / ((full_len - 1) - last)), refresh=True)
    progress.log("[bold white]Script Complete")
