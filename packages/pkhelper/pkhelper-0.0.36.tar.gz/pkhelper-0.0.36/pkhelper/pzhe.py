import os,subprocess,time
from subprocess import run as srun,call as scall
from os.path import exists,getsize,isfile,isdir,join as osjoin
from random import randint,random
from .utils import run_cmds_on_cr

class pzip:
  def __init__(self):
     self.message='hello'
  def extract_with_full_path(file,pswd=None,outf=None):
    cmd=['7z','x',file]
    if outf:
      cmd+=[f'-o{outf}']
    else:
      outf=str(time.time())
      cmd+=[f'-o{outf}']
    if pswd:
       cmd+=[f'-p{pswd}']
    peo=srun(cmd,capture_output=True)
    if peo.returncode==0:
      if isdir(outf):
        return osjoin(os.getcwd(),outf)
    else:
      return  None
  def extract_all(file,pswd=None,outf=None):
    cmd=['7z','e',file]
    if outf:
      cmd+=[f'-o{outf}']
    else:
      outf=str(time.time())
      cmd+=[f'-o{outf}']
    if pswd:
       cmd+=[f'-p{pswd}']
    peo=srun(cmd,capture_output=True)
    if peo.returncode==0:
      if isdir(outf):
        return osjoin(os.getcwd(),outf)
    else:
      return  None
  def zip_archive(file,pswd=None):
    out=f'{file}.zip'
    cmd=['7z','a',out,'-tzip',file]
    if pswd:
      cmd+=[f'-p{pswd}']
    peo=srun(cmd,capture_output=True)
    if peo.returncode==0:
      if isfile(out):
        return osjoin(os.getcwd(),out)
    else:
      return None
  def archive_7z(file,pswd=None):
    out=f'{file}.7z'
    cmd=['7z','a',out,'-t7z',file]
    if pswd:
      cmd+=[f'-p{pswd}']
    peo=srun(cmd,capture_output=True)
    if peo.returncode==0:
      if isfile(out):
        return osjoin(os.getcwd(),out)
    else:
      return None
  def split_archive(file,size_in_bytes=1992294400):
    #7z a outfolder/s.7z -v500b|m|g|k file
    #I have set the default file_size of 1900mb
    out=str(time.time())
    cmd=['7z','a',f'{out}/{file.split("/")[-1]}.7z','-v{size_in_bytes}b',file]
    peo=srun(cmd,capture_output=True)
    if peo.returncode==0:
      if isdir(out):
        return osjoin(os.getcwd(),out)
    else:
      return None
  async def extract_with_full_path_async(file,pswd=None,outf=None):
    return await run_cmds_on_cr(p7zip.extract_with_full_path,file,pswd,outf)
  async def extract_all_async(file,pswd=None,outf=None):
    return await run_cmds_on_cr(p7zip.extract_all,file,pswd,outf)
  async def zip_archive_async(file,pswd=None):
    return await run_cmds_on_cr(p7zip.zip_archive,file,pswd)
  async def archive_7z_async(file,pswd=None):
    return await run_cmds_on_cr(p7zip.archive_7z,file,pswd)
  async def split_archive_async(file,size_in_bytes=1992294400):
    return await run_cmds_on_cr(p7zip.split_archive,file,size_in_bytes)

