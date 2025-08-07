import os
import json
from operator import truediv
import whisper
from pathlib import Path
# Manually set FFmpeg path
FFMPEG_PATH = r"C:\ffmpeg-2025-02-02-git-957eb2323a-full_build\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH
# Supported media formats
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv"}
def find_media_files(directory):
    media_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in AUDIO_EXTENSIONS or ext in VIDEO_EXTENSIONS:
                    media_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error while scanning the directory: {e}")
    return media_files
def transcribe_media(file_path, model):
    try:
        print(f"Processing: {file_path}")
        result = model.transcribe(file_path, fp16=False)  # Ensure compatibility
        transcription_text = result.get("text", "")
        print("Transcription Output:\n", transcription_text)  # Print transcription
        print("Transcription completed successfully.")
        return transcription_text
    except Exception as e:
        print(f"Error during transcription of {file_path}: {e}")
        return ""
def save_transcription(file_path, transcription, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, Path(file_path).stem + ".json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"file": file_path, "transcription": transcription}, f, indent=4)
        print(f"Saved transcription to: {output_path}")
    except Exception as e:
        print(f"Error saving transcription: {e}")
def save_transcription_as_text(file_path, transcription, output_dir):
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, Path(file_path).stem + ".txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        print(f"Saved transcription as text to: {output_path}")
    except Exception as e:
        print(f"Error saving text transcription: {e}")
def main(input_path, output_dir, save_as_text=True):
    try:
        print("Loading Whisper model...")
        model = whisper.load_model("tiny")
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        return
    if os.path.isfile(input_path):
        print(f"Processing single file: {input_path}")
        transcription = transcribe_media(input_path, model)
        if transcription:
            if save_as_text:
                save_transcription_as_text(input_path, transcription, output_dir)
            else:
                save_transcription(input_path, transcription, output_dir)
    elif os.path.isdir(input_path):
        print(f"Scanning directory: {input_path}")
        media_files = find_media_files(input_path)
        if not media_files:
            print("No media files found.")
            return
        for file_path in media_files:
            transcription = transcribe_media(file_path, model)
            if transcription:
                if save_as_text:
                    save_transcription_as_text(file_path, transcription, output_dir)
                else:
                    save_transcription(file_path, transcription, output_dir)
    else:
        print(f"Invalid input path: {input_path}")
        return

    print("Processing complete!")


if __name__ == "__main__":
    # Define default paths if not dynamically set
    input_path = r"C:\Users\saikiranreddy\PycharmProjects\PythonProject3\.venv\media_file\WhatsApp Audio 2025-02-07 at 23.29.37_e358574f.mp3"  # or a directory path
    output_directory = r"C:\Users\saikiranreddy\OneDrive\Documents\trans"

    main(input_path, output_directory, save_as_text=True)
