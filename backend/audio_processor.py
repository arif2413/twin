"""
Audio processing utilities for handling audio chunks.
"""

import struct
from typing import List, Tuple


def parse_audio_chunk(audio_bytes: bytes, sample_rate: int = 16000, channels: int = 1) -> List[float]:
    """
    Parse binary audio chunk (PCM 16-bit) to float array.
    
    Args:
        audio_bytes: Binary audio data (PCM 16-bit format)
        sample_rate: Sample rate in Hz (default: 16000)
        channels: Number of audio channels (default: 1 for mono)
    
    Returns:
        List of float values normalized to [-1.0, 1.0]
    """
    # Convert bytes to 16-bit integers
    int16_samples = struct.unpack(f'<{len(audio_bytes) // 2}h', audio_bytes)
    
    # Normalize to float range [-1.0, 1.0]
    float_samples = [sample / 32768.0 for sample in int16_samples]
    
    return float_samples


def get_audio_info(audio_bytes: bytes, sample_rate: int = 16000, channels: int = 1) -> dict:
    """
    Get information about an audio chunk.
    
    Args:
        audio_bytes: Binary audio data
        sample_rate: Sample rate in Hz
        channels: Number of audio channels
    
    Returns:
        Dictionary with audio information
    """
    num_samples = len(audio_bytes) // 2  # 16-bit = 2 bytes per sample
    duration_seconds = num_samples / sample_rate
    
    return {
        "size_bytes": len(audio_bytes),
        "num_samples": num_samples,
        "sample_rate": sample_rate,
        "channels": channels,
        "duration_seconds": duration_seconds,
        "format": "PCM 16-bit",
    }

