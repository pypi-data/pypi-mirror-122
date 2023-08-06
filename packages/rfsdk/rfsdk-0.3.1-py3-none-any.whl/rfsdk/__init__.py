# rfsdk
import os
import sys

rfsdk_root_path = os.path.dirname(os.path.abspath(__file__))
# ant_root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ant')
if rfsdk_root_path not in sys.path:
    sys.path.append(rfsdk_root_path)

__version__ = '0.3.0'
