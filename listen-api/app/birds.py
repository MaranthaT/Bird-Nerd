import subprocess
import birdnet
import csv
import os
import tempfile
from functools import lru_cache
from dataclasses import dataclass
from datetime import date



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

def week_of(day):
    week_in_month = min((day.day-1) // 7 + 1, 4)
    weeks_before = (day.month-1) * 4
    return weeks_before + week_in_month

@lru_cache
def acoustic_model():
    return birdnet.load("acoustic", "2.4", "tf", library="litert")

@lru_cache
def geo_model():
    return birdnet.load("geo", "2.4", "tf", library="litert")

def identify(path, lat=None, lon=None, day=None):
    predictions = acoustic_model().predict(path)
    with tempfile.TemporaryDirectory() as folder:
        csv_path = os.path.join(folder, "predictions.csv")
        predictions.to_csv(csv_path)
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            detections = []
            allowed = None
            if lat is not None and lon is not None and day is not None:
                allowed = allowed_species(lat, lon, week_of(day))
            for row in reader:
                if float(row["confidence"]) < 0.25:
                    continue
                scientific_name, common_name = split_species(row["species_name"])
                if allowed is not None and scientific_name not in allowed:
                    continue
                detections.append(Detection(common_name, scientific_name, float(row["confidence"]), float(to_seconds(row["start_time"])), float(to_seconds(row["end_time"]))))
        return sorted(detections, key=lambda d: (d.confidence), reverse=True) 


def allowed_species(lat, lon, week=None):
    predictions = geo_model().predict(lat, lon, week=week)
    with tempfile.TemporaryDirectory() as folder:
        csv_path = os.path.join(folder, "predictions.csv")
        predictions.to_csv(csv_path)
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            species = set()
            for row in reader:
                if float(row["confidence"]) < 0.03:
                    continue
                scientific_name, common_name = split_species(row["species_name"])
                species.add(scientific_name)
        return species



