import xarray as xr
import numpy as np

import mpolar


def make_hybrid(da: xr.DataArray) -> xr.DataArray:
    # remove pint units to fallback to raw xarray format
    da = da.pint.dequantify()

    twa = np.arange(0, 360, 22.5)
    tws = np.array([0, 50])
    
    variable_name = da.name
    variable = da.values
    variable_unit = da.attrs.get("units", None)

    coordinate_name = mpolar.polar.coordinates(da)[0]
    coordinate = da[coordinate_name].values

    updated_variable = np.zeros((coordinate.shape[0], twa.shape[0], tws.shape[0]))
    for cidx, _ in enumerate(coordinate):
        for twaidx, _ in enumerate(twa):
            for twsidx, _ in enumerate(tws):
                updated_variable[cidx, twaidx, twsidx] = variable[cidx]

    return mpolar.polar.make(
        name=str(variable_name),
        content=updated_variable,
        dimensions=[(coordinate_name, coordinate), ("TWA", twa), ("TWS", tws)],
        unit=variable_unit,
        dimension_units=[
            da[coordinate_name].attrs.get("units", ""),
            "°", "kt"
        ]
    )
