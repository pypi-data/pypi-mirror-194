import xarray_schema as xrs  # type: ignore
import numpy as np


HybridSpeedControl = xrs.DataArraySchema(
  dtype=np.float64, name="PB", dims=["STW_", "TWA_", "TWS_"])
HybridPowerControl = xrs.DataArraySchema(
  dtype=np.float64, name="STW", dims=["PB_", "TWA_", "TWS_"])
Sailing = xrs.DataArraySchema(
  dtype=np.float64, name="STW", dims=["PB_", "TWA_", "TWS_"], shape=(1, None, None))
Waves = xrs.DataArraySchema(
  dtype=np.float64, dims=["TWS_", "WA_", "Hs_"])
