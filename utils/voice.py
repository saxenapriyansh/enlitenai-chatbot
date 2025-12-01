"""
Voice utilities for speech-to-text and text-to-speech
"""
from openai import OpenAI
import os
from typing import Optional
import tempfile
from pathlib import Path


class VoiceManager:
    """Manages voice input/output using OpenAI Whisper and TTS"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def transcribe_audio(self, audio_bytes: bytes, audio_format: str = "webm") -> str:
        """
        Transcribe audio to text using OpenAI Whisper
        
        Args:
            audio_bytes: Audio data as bytes
            audio_format: Audio format (webm, mp3, wav, etc.)
        
        Returns:
            Transcribed text
        """
        try:
            # Create a temporary file to store audio
            with tempfile.NamedTemporaryFile(suffix=f".{audio_format}", delete=False) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name
            
            # Transcribe using Whisper
            with open(temp_audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            
            # Clean up temp file
            os.unlink(temp_audio_path)
            
            return transcript.text
            
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
    
    def text_to_speech(self, text: str, voice: str = "alloy") -> bytes:
        """
        Convert text to speech using OpenAI TTS
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        
        Returns:
            Audio data as bytes
        """
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            return response.content
            
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")
    
    def save_audio(self, audio_bytes: bytes, output_path: str):
        """Save audio bytes to file"""
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

