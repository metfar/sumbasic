#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
import io;
import math;
import os;
import queue;
import shutil;
import struct;
import subprocess;
import sys;
import threading;
import time;
import wave;


MIDDLE_C_HZ = 261.6255653005986;
GW_BASIC_TICKS_PER_SECOND = 18.2;
GW_BASIC_SOUND_MIN_HZ = 37.0;
GW_BASIC_SOUND_MAX_HZ = 32767.0;


def spectrum_pitch_frequency(pitch):
    return MIDDLE_C_HZ * (2.0 ** (float(pitch) / 12.0));


def spectrum_frequency_pitch(frequency):
    frequency = float(frequency);
    if frequency <= 0.0:
        raise ValueError("frequency must be positive");
    return 12.0 * math.log2(frequency / MIDDLE_C_HZ);


def gw_ticks_to_seconds(ticks):
    return float(ticks) / GW_BASIC_TICKS_PER_SECOND;


class SystemTonePlayer:
    """Portable monophonic tone backend shared by BEEP and SOUND.

    Both BASIC statements use exactly one tone renderer.  Requests are queued
    through one worker so a PC-speaker-style channel can never play two notes
    simultaneously.  A blocking request (Spectrum BEEP) waits for its queued
    note to finish; a background request (GW-BASIC SOUND) returns immediately
    while the same worker renders it in order.
    """
    def __init__(self, sample_rate=22050):
        self.sample_rate = max(8000, int(sample_rate));
        self._tone_queue = queue.Queue();
        self._worker = None;
        self._worker_lock = threading.Lock();

    def _ensure_worker(self):
        with self._worker_lock:
            if self._worker is None or not self._worker.is_alive():
                self._worker = threading.Thread(target=self._worker_loop, name="sumBASIC-tone", daemon=True);
                self._worker.start();
        return self._worker;

    def play(self, frequency, duration, blocking=True):
        frequency = float(frequency);
        duration = max(0.0, float(duration));
        if duration <= 0.0:
            return None;
        completed = threading.Event() if blocking else None;
        result = [];
        self._ensure_worker();
        self._tone_queue.put((frequency, duration, completed, result));
        if completed is not None:
            completed.wait();
            return result[0] if result else False;
        return None;

    def wait_for_background(self):
        """Wait until all queued SOUND requests have finished playing."""
        self._tone_queue.join();
        return None;

    def _worker_loop(self):
        while True:
            frequency, duration, completed, result = self._tone_queue.get();
            try:
                result.append(self._play_blocking(frequency, duration));
            except Exception:
                result.append(False);
            finally:
                if completed is not None:
                    completed.set();
                self._tone_queue.task_done();

    def _play_blocking(self, frequency, duration):
        if os.name == "nt":
            try:
                import winsound;
                winsound.Beep(max(37, min(32767, int(round(frequency)))), max(1, int(round(duration * 1000.0))));
                return True;
            except Exception:
                pass;
        player = shutil.which("play");
        if player:
            try:
                subprocess.run([player, "-q", "-n", "synth", "{:.6f}".format(duration), "sine", "{:.6f}".format(frequency)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
                return True;
            except OSError:
                pass;
        aplay = shutil.which("aplay");
        if aplay:
            try:
                payload = self._wav_bytes(frequency, duration);
                subprocess.run([aplay, "-q", "-"], input=payload, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
                return True;
            except OSError:
                pass;
        try:
            sys.stdout.write("\a");
            sys.stdout.flush();
        except Exception:
            pass;
        time.sleep(duration);
        return False;

    def _wav_bytes(self, frequency, duration):
        count = max(1, int(round(self.sample_rate * float(duration))));
        amplitude = 11000;
        frames = bytearray();
        for index in range(count):
            sample = int(amplitude * math.sin((2.0 * math.pi * float(frequency) * index) / self.sample_rate));
            frames.extend(struct.pack("<h", sample));
        stream = io.BytesIO();
        with wave.open(stream, "wb") as wav:
            wav.setnchannels(1);
            wav.setsampwidth(2);
            wav.setframerate(self.sample_rate);
            wav.writeframes(bytes(frames));
        return stream.getvalue();
