# -----------------------------------------------------------------------------
# - ZUSS -  ZD USB SWITCH SDK
# - File              zuss.py
# - Owner             Zhengkun Li
# - Version           1.1
# - Date              09.06.2021
# - Classification    command line
# - Brief             command line for ZD USB Switch
# - History        
#       2021.06.09    Initial version.                   Zhengkun Li
#       2021.09.27    Add set_relay/set_power commands.  Yu-Ling Xie
# ----------------------------------------------------------------------------- 
name = "zuss"
__version__ = '2.1.0'
__all__ = [
    'detect_comports',
    'get_version',
    'reboot_sys',
    'save_config',
    'clr_config',
    'disp_config',
    'set_host_port',
    'get_host_port',
    'set_dev_port',
    'get_dev_port',
    'set_relay_mask',
    'get_relay_mask',
    'set_pwr_mask',
    'get_pwr_mask',
    'set_relay',
    'get_relay',
    'set_pwr',
    'get_pwr'
]
from .usbswsdk import *
