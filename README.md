# Video Splitter Pro 🎥

A modern web application that allows users to split videos at custom timestamps and extract audio from each part. Perfect for content creators, editors, and anyone needing to split long videos.

![Video Splitter Pro Screenshot](screenshot.png)

## ✨ Features

- **Custom Split Points**: Split videos at any timestamp
- **Audio Extraction**: Automatically extracts audio from each video part
- **Multiple Formats**: Supports MP4, AVI, MOV, and MKV
- **Large File Support**: Handle videos up to 2GB
- **Drag & Drop**: Easy file upload interface
- **Progress Tracking**: Real-time processing status
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Harshil123451/video-splitter.git
   cd video-splitter
   ```

2. **Install FFmpeg**
   - Windows:
     - Download from [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
     - Create a folder named `ffmpeg` in the project root
     - Place ffmpeg.exe inside the folder
   - Mac:
     ```bash
     brew install ffmpeg
     ```
   - Linux:
     ```bash
     sudo apt-get install ffmpeg
     ```

3. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python web_app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:5000`

## 💡 Usage

1. **Set Split Duration**
   - Enter hours, minutes, and seconds for the split point
   - The video will be split at this timestamp

2. **Upload Video**
   - Drag and drop your video file
   - Or click "Choose File" to select
   - Supported formats: MP4, AVI, MOV, MKV
   - Maximum file size: 2GB

3. **Processing**
   - Wait for the upload and processing to complete
   - Progress bar shows current status

4. **Download**
   - Download both video parts separately
   - Download extracted audio for each part
   - Files are automatically cleaned up after download

## 📁 Project Structure
```
video-splitter/
├── static/
│ ├── css/
│ │ └── style.css # Styling
│ └── js/
│ └── main.js # Frontend logic
├── templates/
│ └── index.html # Main page
├── uploads/ # Temporary upload storage
├── output_videos/ # Processed videos
├── output_audio/ # Extracted audio
├── web_app.py # Main application
└── requirements.txt # Dependencies
```

## ⚙️ Technical Details

### Backend
- **Flask**: Web framework
- **MoviePy**: Video processing
- **FFmpeg**: Media handling
- **Werkzeug**: File operations

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with modern features
- **JavaScript**: Dynamic interactions
- **Font Awesome**: Icons

## 🔒 Security

- File type validation
- Secure filename handling
- Automatic file cleanup
- Size limit enforcement

## 💻 Development

### Setting up development environment

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run in debug mode**
   ```bash
   python web_app.py --debug
   ```

### Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

For support, email harshilpatel123451@gmail.com or open an issue on GitHub.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [FFmpeg](https://ffmpeg.org/)
- [Font Awesome](https://fontawesome.com/)

## 📸 Screenshots

### Main Interface
![Main Interface](main-interface.png)

### Processing View
![Processing](processing.png)

### Download Screen
![Download](download.png)

---

Made with ❤️ by [Harshil Chheda](https://github.com/Harshil123451)