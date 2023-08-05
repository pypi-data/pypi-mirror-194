import warnings
import torch
import whisper
import numpy as np
from typing import List, Optional, Tuple, Union
from whisper.audio import SAMPLE_RATE, N_FRAMES, HOP_LENGTH, pad_or_trim
from whisper.utils import exact_div, format_timestamp
from whisper.tokenizer import get_tokenizer, LANGUAGES, TO_LANGUAGE_CODE
from whisper import DecodingOptions, DecodingResult, Whisper, log_mel_spectrogram
from types import MethodType
from itertools import repeat
from tqdm import tqdm
from .audio import prep_wf_mask, remove_lower_quantile, finalize_mask
from .stabilization import stabilize_timestamps, add_whole_word_ts
from .decode_word_level import decode_word_level
from dataclasses import dataclass
import re


@dataclass
class TimestampInfo:
    time: float
    word_match: str = ''
    word_to_match: str = ''
    full_text: list = None
    no_speech_prob: float = None


def is_in_end(word: str, string: str):
    return bool(re.findall(word + '.*$', string))


def timestamp(audio: str, model: "Whisper", language: str = None):
    resolution = 0.05
    dtype = next(model.parameters()).dtype
    audio = whisper.load_audio(audio)
    mel = log_mel_spectrogram(audio)[None]
    sec2mel = SAMPLE_RATE/HOP_LENGTH
    total_frames = mel.shape[-1]
    resolution_mel = int(resolution * sec2mel)
    text = model.transcribe(audio, temperature=0, without_timestamps=True)['text']
    words = [i.strip().lower().replace(',', '').replace('.', '') for i in text.split(' ') if i]
    options = DecodingOptions(language=language, temperature=0, without_timestamps=True)
    timestamps = []
    prev_seek = 0
    for i in range(0, total_frames, resolution_mel):
        seek = i+resolution_mel
        curr_time = seek/sec2mel
        segment = pad_or_trim(mel[..., prev_seek:seek], N_FRAMES).to(device=model.device, dtype=dtype)

        no_speech = model.decode(segment, options)[0].no_speech_prob
        prev_seek = seek

        # res = [i.strip().lower() for i in model.decode(segment, options)[0].text.split(' ')]
        # curr_word = words[0]
        # if res and is_in_end(curr_word, res[-1]):
        #     match = words.pop(0)
        #     prev_seek = seek
        # else:
        #     match = ''
        # timestamps.append(TimestampInfo(curr_time, word_match=match, full_text=res, word_to_match=curr_word))

        timestamps.append(TimestampInfo(curr_time, no_speech_prob=no_speech))

        if not words:
            break

    return timestamps




