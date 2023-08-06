import typing as ty

import xarray as xr
import numpy as np
import numpy.typing as npt


def make(name: str,
         content: npt.NDArray[np.float64],
         dimensions: ty.List[ty.Tuple[str, npt.NDArray[np.float64]]],
         unit: ty.Optional[str] = None,
         dimension_units: ty.Optional[ty.List[str]] = None) -> xr.DataArray:
             
    coords = [(name, value, {}) for name, value in dimensions]  # type: ty.List[ty.Tuple[str, npt.NDArray[np.float64], ty.Dict[str, ty.Any]]]
    coords_units = {}  # type: ty.Dict[str, str]
    coords_swap = {}  # type: ty.Dict[str, str]
    if dimension_units is not None:
        coords_units = {}
        coords = []
        for (dim_name, dim_value), dim_unit in zip(dimensions, dimension_units):
            coords.append((dim_name, dim_value, {'units': dim_unit}))
            coords_units[dim_name] = dim_unit
            coords_swap[dim_name] = dim_name + "_"
    
    da = xr.DataArray(
        name=name,
        data=content,
        dims=[name for name, _ in dimensions],
        coords=coords,
        attrs={} if unit is None else {"units": unit}
    )
    return da.swap_dims(coords_swap).pint.quantify(coords_units)


def coordinates(da: xr.DataArray) -> ty.List[str]:
    return [str(coord) for coord in da.coords]


# def variables(ds: xr.Dataset) -> ty.List[str]:
#     coords = coordinates(ds)
#     variables = []
#     for v in ds.variables:
#         if v in coords:
#             continue
#         variables.append(v)
#     return variables


def to_mship(propulsion: xr.DataArray) -> xr.Dataset:
    # MShip only support STW control at the moment
    assert("PB_kW" not in propulsion.coords)
    
    stw = propulsion.STW_kt.values
    tws = propulsion.TWS_kt.values
    twa = propulsion.TWA_deg.values
    wa = np.array([0])
    hs = np.array([0])
    propulsion_power = propulsion.transpose("STW_kt", "TWS_kt", "TWA_deg").values

    propulsion_power = propulsion_power.reshape(
        stw.shape[0], tws.shape[0], twa.shape[0], wa.shape[0], hs.shape[0])

    return xr.DataArray(
        name="BrakePower",
        data=propulsion_power,
        dims=["STW_kt", "TWS_kt", "TWA_deg", "WA_deg", "Hs_m"],
        coords={
            "STW_kt": stw,
            "TWS_kt": tws,
            "TWA_deg": twa,
            "WA_deg": wa,
            "Hs_m": hs
        },
        attrs={
            "polar_type": "ND",
            "control_variable": "STW_kt"
        }
    ).to_dataset(promote_attrs=True)
