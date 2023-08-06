from functools import partial
from asyncio import get_running_loop
import re

async def run_cmds_on_cr(func, *args, **kwargs):
    """
    Execute blocking functions asynchronously
    """
    loop = get_running_loop()
    return await loop.run_in_executor(
        None,
        partial(func, *args, **kwargs)
    )

def hbs(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def make_safe_filename(filename):
    ext=filename.split('.')[-1]
    # Remove characters that are not letters, digits, spaces, or dots
    filename = re.sub(r'[^\w\s\.]', '', filename)
    # Replace consecutive spaces with single spaces
    filename = re.sub(r'\s+', ' ', filename)
    #filename = re.sub(r'[^\w\s]', '', filename)
    filename = filename.replace(f'.{ext}','').strip()
    MAX_FILENAME_LENGTH = 245 #255
    filename = filename[:MAX_FILENAME_LENGTH] + '.' + ext
    # Check for reserved names
    RESERVED_NAMES = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1', 'LPT2', 'LPT3', 'CLOCK$']
    if filename.upper() in RESERVED_NAMES:
        filename='DefaultName'+'.'+ext
    return filename

