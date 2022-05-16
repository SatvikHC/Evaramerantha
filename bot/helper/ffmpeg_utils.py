import asyncio
import os
import sys
import json
import anitopy
import time
from bot import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import subprocess
from subprocess import Popen, PIPE


async def run_subprocess(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    return await process.communicate()

async def encode(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + "R136A1_Encodes" + ".mkv"
    nam = filepath.replace("/home/runner/work/Auto-Renamer-Queue/Auto-Renamer-Queue/downloads/", " ")
    nam = nam.replace("_", " ")
    nam = nam.replace(".mkv", " ")
    nam = nam.replace(".mp4", " ")
    nam = nam.replace(".", " ")
    if "/bot/downloads/" in nam:
      nam = nam.replace("/bot/downloads", " ")
    new_name = anitopy.parse(nam)
    anime_name = new_name["anime_title"]
    joined_string = f"[{anime_name}]"
    if "anime_season" in new_name.keys():
      animes_season = new_name["anime_season"]
      joined_string = f"{joined_string}" + f" [Season {animes_season}]"
    if "episode_number" in new_name.keys():
      episode_no = new_name["episode_number"]
      joined_string = f"{joined_string}" + f" [Episode {episode_no}]"
    og = joined_string + " [@ANIXPO]" + ".mkv"
    ffmpeg = f'ffmpeg "{filepath}" -map 0 -c:s copy -c:v libx265 -b:v 600k -c:a libopus -ab 64k "{og}" -y'
    process = await run_subprocess(ffmpeg)
    if og:
      return og
    else:
      joined_string1 = joined_string + " [@ANIXPO]"
      return joined_string1

async def get_thumbnail(in_filename):
    out_filename = 'thumb1.jpg'
    cmd = '-map 0:v -ss 00:20 -frames:v 1'
    call(['ffmpeg', '-i', in_filename] + cmd.split() + [out_filename])
    return out_filename
  
async def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

async def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720
