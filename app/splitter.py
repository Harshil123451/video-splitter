from moviepy.editor import VideoFileClip
import os
import subprocess
import math
import sys
import urllib.request
import zipfile

# Update FFmpeg path handling
FFMPEG_PATH = 'ffmpeg' if os.environ.get('RENDER') else os.path.join('ffmpeg', 'ffmpeg.exe')

class VideoSplitter:
    def __init__(self, input_folder="input_videos", output_folder="output_videos", audio_folder="output_audio"):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.audio_folder = audio_folder
        
        # Create all necessary folders
        os.makedirs(input_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(audio_folder, exist_ok=True)
        
        # Set up FFmpeg
        self.setup_ffmpeg()

    def setup_ffmpeg(self):
        """Download and set up FFmpeg if not present"""
        ffmpeg_dir = "ffmpeg"
        self.ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        
        if not os.path.exists(self.ffmpeg_path):
            print("FFmpeg not found. Downloading...")
            os.makedirs(ffmpeg_dir, exist_ok=True)
            
            # Download FFmpeg
            url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            zip_path = "ffmpeg.zip"
            
            try:
                # Download with progress
                def report_progress(count, block_size, total_size):
                    percent = int(count * block_size * 100 / total_size)
                    print(f"Downloading FFmpeg: {percent}%", end="\r")
                
                urllib.request.urlretrieve(url, zip_path, reporthook=report_progress)
                print("\nExtracting FFmpeg...")
                
                # Extract ffmpeg.exe
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for file in zip_ref.namelist():
                        if file.endswith('ffmpeg.exe'):
                            with zip_ref.open(file) as source:
                                with open(self.ffmpeg_path, 'wb') as target:
                                    target.write(source.read())
                            break
                
                # Clean up
                os.remove(zip_path)
                print("✅ FFmpeg setup completed")
                
            except Exception as e:
                print(f"❌ Error setting up FFmpeg: {str(e)}")
                sys.exit(1)

    def extract_audio(self, input_path):
        """Extract audio from video using FFmpeg"""
        try:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            audio_path = os.path.join(self.audio_folder, f"{base_name}.mp3")
            
            command = [
                self.ffmpeg_path,
                '-i', input_path,
                '-vn',  # No video
                '-acodec', 'libmp3lame',  # MP3 codec
                '-ab', '192k',  # Bitrate
                '-y',  # Overwrite output
                audio_path
            ]
            
            print(f"\nExtracting audio to: {audio_path}")
            
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {process.stderr}")
                
            print("✅ Audio extraction completed")
            return True
            
        except Exception as e:
            print(f"❌ Error extracting audio: {str(e)}")
            return False

    def split_video_ffmpeg(self, input_path, output_path, start_time, duration):
        """Split video using direct FFmpeg command"""
        try:
            command = [
                self.ffmpeg_path,
                '-i', input_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c:v', 'copy',  # Copy video codec
                '-c:a', 'copy',  # Copy audio codec
                '-y',  # Overwrite output
                output_path
            ]
            
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {process.stderr}")
                
            return True
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def extract_audio_segment(self, input_path, output_path, start_time, duration):
        """Extract audio segment using FFmpeg"""
        try:
            command = [
                self.ffmpeg_path,
                '-i', input_path,
                '-ss', str(start_time),  # Start time
                '-t', str(duration),     # Duration
                '-vn',                   # No video
                '-acodec', 'libmp3lame', # MP3 codec
                '-ab', '192k',           # Bitrate
                '-y',                    # Overwrite output
                output_path
            ]
            
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {process.stderr}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error extracting audio segment: {str(e)}")
            return False

    def split_video(self, input_path, segment_length=60):
        try:
            print(f"\nProcessing: {os.path.basename(input_path)}")
            
            # Get video duration using moviepy
            video = VideoFileClip(input_path)
            duration = video.duration
            video.close()
            
            # Calculate number of segments
            num_segments = math.ceil(duration / segment_length)
            
            print(f"Video duration: {duration:.1f} seconds")
            print(f"Creating {num_segments} segments of {segment_length} seconds each")
            
            for i in range(num_segments):
                start_time = i * segment_length
                # For the last segment, use remaining duration
                if i == num_segments - 1:
                    segment_duration = duration - start_time
                else:
                    segment_duration = segment_length
                
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                
                # Paths for video and audio segments
                video_output = os.path.join(
                    self.output_folder, 
                    f"{base_name}_part{i+1}.mp4"
                )
                audio_output = os.path.join(
                    self.audio_folder, 
                    f"{base_name}_part{i+1}.mp3"
                )
                
                print(f"\nProcessing segment {i+1}/{num_segments} ({start_time:.1f}s to {(start_time + segment_duration):.1f}s)")
                
                # Process video segment
                if self.split_video_ffmpeg(input_path, video_output, start_time, segment_duration):
                    print(f"✅ Completed video segment {i+1}/{num_segments}")
                else:
                    print(f"❌ Failed to process video segment {i+1}/{num_segments}")
                
                # Process audio segment
                if self.extract_audio_segment(input_path, audio_output, start_time, segment_duration):
                    print(f"✅ Completed audio segment {i+1}/{num_segments}")
                else:
                    print(f"❌ Failed to process audio segment {i+1}/{num_segments}")
            
            print(f"\n✅ Successfully processed: {os.path.basename(input_path)}")
            
        except Exception as e:
            print(f"\n❌ Error processing {os.path.basename(input_path)}: {str(e)}")

    def process_folder(self, segment_length=60):
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')
        videos = [f for f in os.listdir(self.input_folder) 
                 if f.lower().endswith(video_extensions)]
        
        if not videos:
            print(f"\nNo videos found in {self.input_folder}")
            print(f"Please add videos with these extensions: {', '.join(video_extensions)}")
            return
        
        print(f"\nFound {len(videos)} videos to process")
        
        for video in videos:
            input_path = os.path.join(self.input_folder, video)
            self.split_video(input_path, segment_length)

if __name__ == "__main__":
    splitter = VideoSplitter()
    
    print("\nVideo Splitter")
    print("=============")
    print(f"1. Place your videos in the '{splitter.input_folder}' folder")
    print(f"2. Video segments will be saved to '{splitter.output_folder}' folder")
    print(f"3. Audio files will be saved to '{splitter.audio_folder}' folder")
    print("4. Supported formats: .mp4, .avi, .mov, .mkv, .wmv")
    
    try:
        segment_length = int(input("\nEnter segment length in seconds (default: 60): ") or "60")
    except ValueError:
        print("Invalid input, using default 60 seconds")
        segment_length = 60
    
    splitter.process_folder(segment_length)
    
    input("\nPress Enter to exit...")