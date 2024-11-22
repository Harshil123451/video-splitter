from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from moviepy.editor import VideoFileClip
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure maximum file size (2GB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB in bytes

# Configure upload settings
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
OUTPUT_VIDEO_FOLDER = os.path.join(app.root_path, 'output_videos')
OUTPUT_AUDIO_FOLDER = os.path.join(app.root_path, 'output_audio')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Create necessary folders
for folder in [UPLOAD_FOLDER, OUTPUT_VIDEO_FOLDER, OUTPUT_AUDIO_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        # Get split duration from request
        split_time = request.form.get('splitDuration', type=int)
        if split_time is None:
            return jsonify({'error': 'Split duration not provided'}), 400

        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        new_filename = f"{timestamp}_{filename}_{unique_id}"
        
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        file.save(file_path)
        
        return process_video(new_filename, split_time)
    
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_video(filename, split_time):
    try:
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        video = VideoFileClip(input_path)
        total_duration = video.duration

        # Validate split time
        if split_time <= 0 or split_time >= total_duration:
            video.close()
            os.remove(input_path)
            return jsonify({
                'error': f'Invalid split time. Video duration is {format_duration(int(total_duration))}'
            }), 400

        # Create output filenames
        name_without_ext = os.path.splitext(filename)[0]
        
        # Process first part
        part1_video_path = os.path.join(OUTPUT_VIDEO_FOLDER, f"{name_without_ext}_part1.mp4")
        part1_audio_path = os.path.join(OUTPUT_AUDIO_FOLDER, f"{name_without_ext}_part1.mp3")
        
        # Process second part
        part2_video_path = os.path.join(OUTPUT_VIDEO_FOLDER, f"{name_without_ext}_part2.mp4")
        part2_audio_path = os.path.join(OUTPUT_AUDIO_FOLDER, f"{name_without_ext}_part2.mp3")
        
        # Split video at specified time
        first_half = video.subclip(0, split_time)
        second_half = video.subclip(split_time, total_duration)
        
        # Write first part
        first_half.write_videofile(part1_video_path)
        first_half.audio.write_audiofile(part1_audio_path)
        
        # Write second part
        second_half.write_videofile(part2_video_path)
        second_half.audio.write_audiofile(part2_audio_path)
        
        # Clean up
        video.close()
        first_half.close()
        second_half.close()
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'duration': total_duration,
            'split_time': split_time,
            'parts': {
                'part1': {
                    'video': os.path.basename(part1_video_path),
                    'audio': os.path.basename(part1_audio_path),
                    'duration': split_time
                },
                'part2': {
                    'video': os.path.basename(part2_video_path),
                    'audio': os.path.basename(part2_audio_path),
                    'duration': total_duration - split_time
                }
            }
        })
        
    except Exception as e:
        app.logger.error(f"Processing error: {str(e)}")
        # Clean up on error
        if os.path.exists(input_path):
            os.remove(input_path)
        raise

@app.route('/download/<type>/<filename>')
def download_file(type, filename):
    try:
        if type == 'video':
            directory = OUTPUT_VIDEO_FOLDER
        elif type == 'audio':
            directory = OUTPUT_AUDIO_FOLDER
        else:
            return 'Invalid file type', 400
            
        file_path = os.path.join(directory, secure_filename(filename))
        
        if not os.path.exists(file_path):
            return 'File not found', 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)