import os
import ffmpeg
import mimetypes
import time
from pathlib import Path
from gemini_client import client

supported_formats = {
    '.mp4': 'video/mp4',
    '.m4v': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.mpg': 'video/mpg',
    '.mov': 'video/mov',
    '.avi': 'video/avi',
    '.flv': 'video/x-flv',
    '.webm': 'video/webm',
    '.wmv': 'video/wmv',
    '.3gp': 'video/3gpp',
    '.3gpp': 'video/3gpp'
}

def video_compressor(input_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in supported_formats:
        print(f"Unsupported format '{ext}', skipping compression.")
        return input_path

    # Probe video to get resolution
    probe = ffmpeg.probe(input_path)
    video_streams = [s for s in probe['streams'] if s['codec_type'] == 'video']
    if not video_streams:
        raise ValueError("No video stream found in file")
    
    height = int(video_streams[0]['height'])
    
    if height > 480:
        # Generate output filename
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_compressed{ext}"

        # Compress to 480p while preserving aspect ratio
        ffmpeg.input(input_path).output(
            output_path,
            vf='scale=-2:480',
            preset='fast',
            crf=23
        ).overwrite_output().run()

        print(f"Video compressed to 480p: {output_path}")
        return output_path
    else:
        print("Video is 480p or lower, skipping compression.")
        return input_path
    
def get_mime_type(file_path):
    file_extension = Path(file_path).suffix.lower()
    if file_extension in supported_formats:
        return supported_formats[file_extension]
    
    # Fallback to mimetypes guess
    guessed_type, _ = mimetypes.guess_type(file_path)
    if guessed_type and guessed_type.startswith('video/'):
        return guessed_type
    
    # Default to mp4 if can't determine
    return 'video/mp4'
    
def upload_video_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")
    
    file_path = Path(file_path)
    mime_type = get_mime_type(str(file_path))
    
    print(f"Uploading {file_path.name} ({mime_type})...")
    
    try:
        with open(file_path, 'rb') as f:
            file_obj = client.files.upload(
                file=f,
                config={
                    "display_name": file_path.name,
                    "mime_type": mime_type,
                }
            )
        
        print("File uploaded. Waiting for processing...")
        
        # Wait for file processing
        max_wait_time = 300
        wait_time = 0
        
        while file_obj.state.name == "PROCESSING" and wait_time < max_wait_time:
            time.sleep(5)
            wait_time += 5
            file_obj = client.files.get(name=file_obj.name)
            print(f"Processing... ({wait_time}s)")
        
        if file_obj.state.name == "FAILED":
            raise Exception("File processing failed")
        elif file_obj.state.name == "PROCESSING":
            raise Exception("File processing timed out")
        
        print("File processed successfully!")
        return file_obj
        
    except Exception as e:
        raise Exception(f"Error uploading file: {str(e)}")