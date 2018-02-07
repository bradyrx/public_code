"""
NPGO Index
Author: Riley X. Brady
Date: 12/13/2017

Computes the NPGO index for a given CESM-LE ensemble member, as defined by the
second PC of SSTs from 25N-62N and 180W-110W.

Command Line Inputs:
INPUT 1: Str indicating the ensemble member (e.g. 001)
INPUT 2: Starting year for NPGO index (e.g. 1920)
INPUT 3: Ending year for NPGO index (e.g. 2015)

Reference:
1. Di Lorenzo, E. and N. Mantua, 2016: Multi-year persistence of the 2014/15
North Pacific marine heatwave. Nature Climate Change, 6(11) 1042-+,
doi:10.1038/nclimate3082.
2. Joh, Y., & Di Lorenzo, E. (2017). Increasing coupling between NPGO and PDO 
leads to prolonged marine heatwaves in the Northeast Pacific. Geophysical Research 
Letters, 44. https://doi.org/10.1002/2017GL075930
3. Personal Communication with Manu Di Lorenzo (2017)
"""
import numpy as np
import pandas as pd
import xarray as xr
import esmtools as et
from eofs.xarray import Eof
import sys

def main():
    ens = sys.argv[1]
    sYear = sys.argv[2]
    eYear = sys.argv[3]
    if int(sYear) < 1920:
        raise ValueError("Starting year must be 1920 or later.")
    if int(eYear) > 2100:
        raise ValueError("End year must be 2100 or earlier.")
    print("Computing NPGO for ensemble number " + ens + "...")
    filepath = ('/glade/scratch/rbrady/EBUS_BGC_Variability/' +
        'global_residuals/SST/remapped/remapped.SST.' + ens +
        '.192001-210012.nc')
    print("Global residuals loaded...")
    ds = xr.open_dataset(filepath)
    ds = ds['SST'].squeeze()
    # Make time dimension readable through xarray.
    ds['time'] = pd.date_range('1920-01', '2101-01', freq='M')
    # Reduce to time period of interest.
    ds = ds.sel(time=slice(sYear + '-01', eYear + '-12'))
    # Slice down to Northeast Pacific domain.
    ds = ds.sel(lat=slice(25, 62), lon=slice(180,250))
    # Take annual JFM means.
    month = ds['time.month']
    JFM = (month <= 3)
    ds_winter = ds.where(JFM).resample('A', 'time')
    # Compute EOF
    coslat = np.cos(np.deg2rad(ds_winter.lat.values))
    wgts = np.sqrt(coslat)[..., np.newaxis]
    solver = Eof(ds_winter, weights=wgts, center=False)
    print("NPGO computed.")
    eof = solver.eofsAsCorrelation(neofs=2)
    variance = solver.varianceFraction(neigs=2)
    # Reconstruct the monthly index of SSTa by projecting
    # these values onto the annual PC timeseries.
    pseudo_pc = solver.projectField(ds, neofs=2, eofscaling=1)
    # Set up as dataset.
    ds = eof.to_dataset()
    ds['pc'] = pseudo_pc
    ds['variance_fraction'] = variance
    ds = ds.rename({'eofs': 'eof'})
    ds = ds.sel(mode=1)
    # Invert to the proper values for the bullseye.
    if ds.sel(lat=45.5, lon=210).eof < 0:
        pass
    else:
        ds['eof'] = ds['eof'] * -1
        ds['pc'] = ds['pc'] * -1
    # Change some attributes for the variables.
    ds['eof'].attrs['long_name'] = 'Correlation between PC and JFM SSTa'
    ds['pc'].attrs['long_name'] = 'Principal component for NPGO'
    # Add a description of methods for clarity.
    ds.attrs['description'] = 'Second mode of JFM SSTa variability over 25-62N and 180-110W.'
    ds.attrs['anomalies'] = 'Anomalies were computed by removing the ensemble mean at each grid cell.'
    ds.attrs['weighting'] = ('The native grid was regridded to a standard 1deg x 1deg (180x360) grid.' +
                             'Weighting was computed via the sqrt of the cosine of latitude.')
    print("Saving to netCDF...")
    ds.to_netcdf('/glade/p/work/rbrady/NPGO/NPGO.' + ens + '.' + str(sYear) +
                 '-' + str(eYear) + '.nc')

if __name__ == '__main__':
    main()
