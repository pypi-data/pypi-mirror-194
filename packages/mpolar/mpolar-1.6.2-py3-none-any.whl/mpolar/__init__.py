import xarray as xr

import cf_xarray.units  # must be imported before pint_xarray
import pint_xarray  # type: ignore
from pint_xarray import unit_registry as ureg

xr.set_options(display_expand_data=False)
ureg.define('kn = kt')  # Note: on many projects we use kn instead kt for knots
ureg.define('percent = 0.01 = %')

from mpolar import table_format, list_format, polar


def parse(path: str, sep: str = ";", **kwargs):
    try:
        retval = table_format.parse(path, sep, **kwargs)
    except Exception:
        retval = list_format.parse(path, sep)
    return retval


from mpolar import propulsion, schema
