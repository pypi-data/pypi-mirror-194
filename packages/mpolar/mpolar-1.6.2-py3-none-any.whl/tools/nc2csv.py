#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import argparse
import os
import xarray as xr
import csv

__version__ = "0.1"

"""
** nc2csv **
** D-ICE ENGINEERING -- 2022 **

This python utility allows to convert an ESPERADO (or Shiplify) polar in NetCDF file format into a csv file readable
by Satori. This is a quick fix utility while waiting Satori to be able to directly use NetCDF files.

Important
=========
Satori file format is a representation of a performance polar in 3D. There is no room for wave effects. When 
conversion is done between NetCDF and Satori CSV file, only performance in calm water (no waves) are exported.
Thus values for null significant wave height and null wave angle must be present in the netCDF file.

Usage
=====

This file must be used as a command line python utility. The syntax is:

    nc2csv.py path_to_netcdf_file.nc
    
If conversion is successful, a new file named path_to_netcdf_file_satori.csv is created next to the original netCDF 
file.

Requirements
============

This tool requires the following Python libraries to be available into the current Python environment:

* argparse
* xarray
* netcdf4

We advice to use Python conda distribution.
"""


def main():
    parser = argparse.ArgumentParser(
        description=""" -- CONVERT ND polar NetCDF file to legacy CSV Satori format --""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('nc_file', type=str,
                        help="""NetCDF ND polar file from ESPERADO or Shiplify""")

    args = parser.parse_args()

    nc_filename = args.nc_file
    nc_filename = os.path.abspath(nc_filename)
    basename, _ = os.path.splitext(nc_filename)

    sat_filename = basename
    if os.path.exists(sat_filename):
        i = 1
        while os.path.exists(sat_filename + "_" + str(i) + ".csv"):
            i += 1
        sat_filename += "_%u" % i

    sat_filename += ".csv"

    print(nc_filename, "\t-->\t", sat_filename)

    # Reading file
    ds = xr.open_dataset(nc_filename)
    ds = ds.sel(Hs_m=0, WA_deg=0).drop(["Hs_m", "WA_deg"])["BrakePower"]

    with open(sat_filename, 'w') as f:
        writer = csv.writer(f, delimiter=";")

        header = []
        for STW_kt in ds.STW_kt.values:
            header += [STW_kt] + list(ds.TWS_kt.values) + [""]
        writer.writerow(header)

        for TWA_deg in ds.TWA_deg.values:
            row = []
            for STW_kt in ds.STW_kt.values:
                row += [TWA_deg] + list(ds.sel(TWA_deg=TWA_deg, STW_kt=STW_kt).values) + [""]
            writer.writerow(row)


if __name__ == '__main__':
    main()
