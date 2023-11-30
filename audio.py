from pathlib import Path
from openai import OpenAI
import os

client = OpenAI(api_key="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")

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="shimmer",
  input=f"""Test test."""
)

response.stream_to_file(speech_file_path)