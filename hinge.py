import random
import subprocess
import os
import time
from pybooklid import LidSensor

SOUND_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

MIN_ANGLE = 20
MAX_ANGLE = 128
MOVE_THRESHOLD = 1.5

SLOW_SPEED = 2
FAST_SPEED = 15

STILL_POLLS_TO_STOP = 1

sounds = [f for f in os.listdir(SOUND_FOLDER) if f.endswith(".mp3")]

last_angle = None
last_direction = None  # 1 = opening, -1 = closing
last_sound = None
sound_process = None
still_counter = 0
last_play_time = 0
saved_volume = subprocess.run(
    ["osascript", "-e", "output volume of (get volume settings)"],
    capture_output=True, text=True
).stdout.strip()  # cached


def set_system_volume(vol):
    subprocess.Popen(["osascript", "-e", f"set volume output volume {vol}"])


def pick_sound():
    """Pick a random sound, avoiding the last one played."""
    global last_sound
    choices = [s for s in sounds if s != last_sound] or sounds
    picked = random.choice(choices)
    last_sound = picked
    return picked


def speed_to_volume(speed):
    """Map movement speed to volume (0.3 quiet … 2.0 loud)."""
    t = min((speed - MOVE_THRESHOLD) / (FAST_SPEED - MOVE_THRESHOLD), 1.0)
    return 0.5 + t * 1.5


def speed_to_rate(speed):
    """Map movement speed to playback rate (0.8 slow creak … 1.6 fast creak)."""
    t = min((speed - MOVE_THRESHOLD) / (FAST_SPEED - MOVE_THRESHOLD), 1.0)
    return 0.8 + t * 0.8


MIN_GAP = 0.3  


def play_sound(speed):
    global sound_process, last_play_time, saved_volume
    set_system_volume(100)
    sound = pick_sound()
    path = os.path.join(SOUND_FOLDER, sound)
    vol = speed_to_volume(speed)
    rate = speed_to_rate(speed)
    sound_process = subprocess.Popen(
        ["afplay", "-v", str(round(vol, 2)), "-r", str(round(rate, 2)), path]
    )
    last_play_time = time.monotonic()


def stop_sound():
    global sound_process
    if sound_process and sound_process.poll() is None:
        sound_process.kill() 
    sound_process = None
    set_system_volume(saved_volume)


with LidSensor() as sensor:
    for angle in sensor.monitor(interval=0.05):

        if last_angle is None:
            last_angle = angle
            continue

        speed = abs(angle - last_angle)

        hinge_moving = (
            MIN_ANGLE <= angle <= MAX_ANGLE and speed > MOVE_THRESHOLD
        )

        if hinge_moving:
            still_counter = 0
            now = time.monotonic()
            direction = 1 if angle > last_angle else -1
            direction_changed = last_direction is not None and direction != last_direction
            last_direction = direction

            sound_playing = sound_process is not None and sound_process.poll() is None

            if direction_changed:
                stop_sound()
                play_sound(speed)
            elif not sound_playing and (now - last_play_time) >= MIN_GAP:
                play_sound(speed)

        else:
            still_counter += 1
            if still_counter >= STILL_POLLS_TO_STOP:
                stop_sound()

        last_angle = angle
