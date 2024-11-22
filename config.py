import os

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload settings
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'input_videos')
    OUTPUT_VIDEO_FOLDER = os.path.join(BASE_DIR, 'output_videos')
    OUTPUT_AUDIO_FOLDER = os.path.join(BASE_DIR, 'output_audio')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}

    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_VIDEO_FOLDER, exist_ok=True)
import os

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload settings
    MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000MB max file size
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'input_videos')
    OUTPUT_VIDEO_FOLDER = os.path.join(BASE_DIR, 'output_videos')
    OUTPUT_AUDIO_FOLDER = os.path.join(BASE_DIR, 'output_audio')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}

    # Create necessary directories
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_VIDEO_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_AUDIO_FOLDER, exist_ok=True)