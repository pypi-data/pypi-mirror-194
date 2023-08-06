from asyncio.subprocess import PIPE as asyncPIPE
from asyncio import create_subprocess_shell as asyncrunapp
from subprocess import run as srun 


async def bash_async(cmd):
  fetch = await asyncrunapp(
            cmd,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
          )
  stdout, stderr = await fetch.communicate()
  result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())
  return result

def bash(cmd):
 #r = subprocess.run(['mediainfo', '--output=HTML', file], stdout=subprocess.PIPE).stdout.decode('utf-8')
 r = srun(cmd,shell=True,capture_output=True)
 stdout,stderr= r.stdout,r.stderr
 resu=str(stdout.decode().strip()) + str(stderr.decode().strip())
 return resu
