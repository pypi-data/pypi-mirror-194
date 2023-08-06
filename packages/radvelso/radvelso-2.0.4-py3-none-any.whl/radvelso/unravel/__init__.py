"""
UNRAVEL module
"""
import os

## SAVE the numba cache in the BALTRAD USER SPACE if it exists
# _numba_cache_dir=os.getenv("NUMBA_CACHE_DIR")
# if _numba_cache_dir is None:
#     _blt_user_path = os.getenv("BLT_USER_PATH")
#     if _blt_user_path is not None:
#         _numba_cache_dir = os.path.join(_blt_user_path,"cache/numba")
#         if not os.path.isdir(_numba_cache_dir):    
#             os.makedirs(_numba_cache_dir)
#         os.environ["NUMBA_CACHE_DIR"] = _numba_cache_dir

from .dealias import (
    unravel_3D_pyart,
    unravel_3D_pyodim,
    dealias_long_range,
    dealiasing_process_2D,
    unravel_3D_pyart_multiproc,
)
