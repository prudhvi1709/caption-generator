import os
import ffmpeg
import mimetypes
import time
import base64
from pathlib import Path

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
    
    print(f"Processing {file_path.name} ({mime_type})...")
    
    try:
        # Read the video file and encode it as base64
        with open(file_path, 'rb') as f:
            video_data = f.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        # Create a file object that contains the video data
        file_obj = type('FileObject', (), {
            'name': file_path.name,
            'mime_type': mime_type,
            'uri': f"data:{mime_type};base64,{video_base64}",
            'data': video_data,
            'base64_data': video_base64
        })()
        
        print("Video file processed successfully!")
        return file_obj
        
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")