import subprocess
import birdnet
from functools import lru_cache
from dataclasses import dataclass


@dataclass
class Detection:
    common_name: str
    scientific_name: str
    confidence: float
    start_second: float
    end_second: float

def to_wav(src, dst):
    subprocess.run(["ffmpeg", "-y", "-i", src, "-ac", "1", "-ar", "48000", "-t", "60", dst], check=True)

def split_species(species_name):
    first, second =species_name.split("_", 1)
    return first, second

def to_seconds(timestamp):
    hours,minutes, seconds = map(float, timestamp.split(":"))
    return hours * 3600 + minutes * 60 + seconds

@lru_cache
def acoustic_model():
    return birdnet.load("acoustic", "2.4", "tf", library="litert")