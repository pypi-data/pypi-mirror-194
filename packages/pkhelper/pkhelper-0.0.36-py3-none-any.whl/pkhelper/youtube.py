"""from .ffmpeg import ffmpeg
import yt_dlp,time
import os,asyncio,random,re
import requests,sys,io,subprocess
from yt_dlp.utils import DownloadError
from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from functools import partial
from subprocess import Popen, PIPE
from youtube_transcript_api.formatters import SRTFormatter
from youtube_transcript_api import YouTubeTranscriptApi 
from subprocess import run as srun,call as scall
from os.path import exists,getsize
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
from .utils import hbs


def get_yt_id(url, ignore_playlist=False):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
        if not ignore_playlist:
            with suppress(KeyError):
                return parse_qs(query.query)['list'][0]
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
        if query.path[:8] == '/shorts/':return query.path.split('/')[2]

def ddl_srt_captions(url):
  vid_id=get_yt_id(url)
  if vid_id:
    try:
      try:
        transcript = YouTubeTranscriptApi.get_transcript(f"{vid_id}",['en'])
      except:
        transcript=""
      if len(transcript) != 0 :
        formatter=SRTFormatter()
        vtt = formatter.format_transcript(transcript)
        file=f"{os.getcwd()}/{vid_id}.srt"
        with open(file,"w") as duf:
          duf.write(vtt)
        if exists(file):
          return file
        else:
          return None
      else:
        transcript_list = YouTubeTranscriptApi.list_transcripts(vid_id)
        try:
          transcript = transcript_list.find_generated_transcript(['en'])
        except:
          transcript=''
        if len(transcript) != 0 :
          formatter=SRTFormatter()
          vtt = formatter.format_transcript(transcript)
          file=f"{os.getcwd()}/{vid_id}.srt"
          with open(file,"w") as g:
            g.write(vtt)
          if exists(file):
            return file
          else:
            return None
        else:
          for transcript in transcript_list:
            if transcript.is_translatable:
              translated_transcript = transcript.translate('en')
              vtt=translated_transcript.fetch()
              if len(vtt)!=0:
                formatter=SRTFormatter()
                vtt = formatter.format_transcript(vtt)
                file=f"{os.getcwd()}/{vid_id}.srt"
                with open(file,"w") as g:
                  g.write(vtt)
                if exists(file):
                  return file
                else:
                  return None
    except Exception as e:
      print(str(e))
      return None

class downyut:
  def __init__(self,title,format_,format_id,ext,size,thumb,url,is_dash=False):
    self.url=url
    self.format_=format_
    self.format_id=format_id
    self.ext=ext
    self.title=title
    self.is_dash=is_dash
    self.size=size
    self.filename=f'{title}.{ext}'
    self.thumb=thumb
  def __repr__(self):
    return(f'{self.format_}_{hbs(self.size)}_{self.ext}_{"pr" if not self.is_dash else "" }')
  @property
  async def download(self):
    thum=os.path.join(os.getcwd(),f'{time.time()}.jpg')
    with open(thum,'wb') as th:
      th.write(requests.get(self.thumb).content)
    if not self.is_dash:
      cmd=f'''yt-dlp -q -f {self.format_id} --write-subs --write-auto-subs {self.url} --force-overwrites -o "{self.filename}" '''
      fer=await asyncrunapp(cmd)
      await fer.communicate()
      filename=os.path.join(os.getcwd(),self.filename)
      if exists(filename and thum):
        return filename,thum
      elif (exists(filename) and not exists(thum)):
        thum=None
        return filename,thum
      else:
        return None
    else:
      if 'audio' in self.format_.lower():
        cmd=f'''yt-dlp -q -f {self.format_id} {self.url} --force-overwrites -o "{self.filename}" '''
        fer=await asyncrunapp(cmd)
        await fer.communicate()
        filename=os.path.join(os.getcwd(),self.filename)
        if exists(filename and thum):
          return filename,thum
        elif (exists(filename) and not exists(thum)):
          thum=None
          return filename,thum
        else:
          return None
      else:
        audio=await yutudown(self.url).download_best_audio
        cmd=f'''yt-dlp -q -f {self.format_id} --write-subs  {self.url} -o "{self.filename}" '''
        fer=await asyncrunapp(cmd)
        await fer.communicate()
        video=os.path.join(os.getcwd(),self.filename)
        subt=ddl_srt_captions(self.url)
        file=ffmpeg.merge_streams(video=video,audio=audio,subtitle=subt)
        return file,thum


class yutudown:
  def __init__(self,url):
      self.url=url
      self.jssn=None
      self.keyb=[]
      self.title=''
      self.thumbnail_url=''
  @property
  def streams(self):
    with yt_dlp.YoutubeDL() as ydl:
      self.jssn=ydl.extract_info(self.url,download=False)
    self.thumbnail_url=self.jssn.get('thumbnail')
    self.title=self.jssn.get('title')
    forms=self.jssn.get('formats')
    for ent in forms:
      if 'storyboard' in str(self.jssn.get('format')).lower():
        forms.remove(ent)
    for ent in forms:
         #if 'dash' in str(ent.get('container')).lower():
         self.keyb.append(downyut(
           title=self.title,
           format_=ent.get('format'),
           format_id=ent.get('format_id'),
           ext=ent.get('ext'),
           size=ent.get('filesize'),
           thumb=self.thumbnail_url,
           is_dash=True if ('dash' in str(ent.get('container')).lower()) else False,
           url=self.url)
           )
    return self.keyb
  @property
  def audio_stream(self):
    li=[]
    for ent in self.streams:
      if 'audio' in str(ent):
        li.append(ent)
      else:
        del ent
    return li
  @property
  def video_stream(self):
    li=[]
    for ent in self.streams:
      if not (('audio' in str(ent)) or ('storyboard' in str(ent))):
        li.append(ent)
      else:
        del ent
    return li
  @property
  def progressive_only(self):
    li=[]
    for ent in self.streams:
      if not ent.is_dash:
        li.append(ent)
      else:
        del ent
    return li
  @property
  async def download_best_audio(self):
    unkjhg={}
    kjur=[]
    for ent in self.audio_stream:
      kjur.append(ent.size)
      unkjhg[ent.size]=ent
    bestie=max(kjur)
    if bestie is not None:
      k,_=await unkjhg[bestie].download
      return k
    else:
      stream=self.progressive_only[0]
      video,_=await stream.download
      audio=ffmpeg.extract_audio(video)
      return audio"""
