import os,aiohttp,asyncio,sys,time
from requests import head as rhead
exts=['mkv','mp4','mp3','m4a','mov','rst','html','php','tar','gz','gzip','md','py','cxx','cpp','3gp','3gpp','rar','7z','pdf','jpg','png','webm','weba','webp','zip','rar','mobi','epub','winzip','jpeg','apk','m4v','mka']
from urllib.parse import unquote,urlparse
import urllib.request
import re

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

def url_filter(url):
  filt=re.findall(r'(https?://\S+)', url)
  #returns a list 
  return filt

def url2name(url):
  filename=unquote(urlparse(url).path.split("/")[-1])
  if len(filename) == 0:
    filename="DefaultName.txt"
  elif len(filename)>255:
    filename=filename[:249]+'.'+ filename.split('.')[-1]
  else:
    pass
  fnam=filename.encode('raw-unicode-escape').decode('utf-8')
  return make_safe_filename(fnam)

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def spd(start,down):
   diff=time.time()-start
   ge=down/diff
   speed=f"""{humanbytes(ge)}/s"""
   return speed

#dl_header=rhead(url).headers
#filename=str(dl_header.get("content-disposition")).split('filename="')[-1].replace('"',"").encode('raw-unicode-escape').decode('utf-8')


def url2name_head(url):
 try:
  req = urllib.request.Request(url, method='HEAD')
  r = urllib.request.urlopen(req)
  return r.info().get_filename()
 except Exception:
   cont_disp=str(rhead(url).headers.get('content-disposition'))
   if "filename" in cont_disp.lower():
     filename=make_safe_filename(cont_disp.split('filename=')[-1].replace('"','').encode('raw-unicode-escape').decode('utf-8'))
     return filename

async def direct_dl_async(download_url, filename=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                cont_disp=str(response.headers.get('content-disposition'))
                if "filename" in cont_disp.lower():
                   filename=make_safe_filename(cont_disp.split('filename=')[-1].replace('"','').encode('raw-unicode-escape').decode('utf-8'))
                else:
                   filename=url2name(download_url)      
            filename = os.path.join(os.getcwd(), unquote(filename))
            total_size = int(response.headers.get("content-length", 1)) or 1024
            downloaded_size = 0
            with open(filename, "wb") as f:
                start=time.time()
                async for chunk in response.content.iter_chunked(8*1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
            return filename

async def ddad(download_url, filename=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                cont_disp=str(response.headers.get('content-disposition'))
                if "filename" in cont_disp.lower():
                   filename=make_safe_filename(cont_disp.split('filename=')[-1].replace('"','').encode('raw-unicode-escape').decode('utf-8'))
                else:
                   filename=url2name(download_url)
            filename = os.path.join(os.getcwd(), unquote(filename))
            total_size = int(response.headers.get("content-length", 1)) or 1024
            downloaded_size = 0
            with open(filename, "wb") as f:
                start=time.time()
                print("Downloading",filename,'\n')
                async for chunk in response.content.iter_chunked(8*1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        speed=spd(start,downloaded_size)
                        print(f""" {humanbytes(downloaded_size)}/{humanbytes(total_size)} {str((downloaded_size/total_size)*100)[:4]}%  {speed} """,end="\r")
            print("\n")
            print("Downloaded Successfully✓")
            print(f"""File: {filename}""")
            return filename

def direct_dl(url,filename=None):
 loop=asyncio.get_event_loop()
 r=loop.run_until_complete(ddad(url,filename))
 return r

async def head_async(url):
  async with aiohttp.ClientSession() as session:
    e=await session.head(url)
    return e.headers
