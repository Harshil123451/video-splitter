import os
from werkzeug.utils import secure_filename
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           os.path.splitext(filename)[1].lower() in allowed_extensions

def generate_unique_filename(filename):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    secure_name = secure_filename(filename)
    return timestamp + secure_name