document.addEventListener('DOMContentLoaded', function() {
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const progressContainer = document.getElementById('progressContainer');

    // Drag and drop functionality
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    const MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024; // 2GB in bytes

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    function handleFileSelect(file) {
        if (file.size > MAX_FILE_SIZE) {
            alert(`File is too large. Maximum size is ${formatFileSize(MAX_FILE_SIZE)}`);
            return;
        }

        const fileInfo = document.getElementById('fileInfo');
        fileInfo.innerHTML = `
            <div class="file-details">
                <p><strong>Selected:</strong> ${file.name}</p>
                <p><strong>Size:</strong> ${formatFileSize(file.size)}</p>
            </div>
        `;
        uploadFile(file);
    }

    function getSplitDuration() {
        const hours = parseInt(document.getElementById('splitHours').value) || 0;
        const minutes = parseInt(document.getElementById('splitMinutes').value) || 0;
        const seconds = parseInt(document.getElementById('splitSeconds').value) || 0;
        return hours * 3600 + minutes * 60 + seconds;
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Get split duration in seconds
        const splitDuration = getSplitDuration();
        formData.append('splitDuration', splitDuration);

        progressContainer.style.display = 'block';
        const progressBar = document.getElementById('progressBar');
        const statusText = document.getElementById('statusText');

        try {
            statusText.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
            progressBar.style.width = '0%';

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }

            if (data.success) {
                progressBar.style.width = '100%';
                statusText.innerHTML = '<i class="fas fa-check"></i> Processing complete!';
                updateDownloadLinks(data.parts);
            } else {
                throw new Error(data.error || 'Processing failed');
            }

        } catch (error) {
            console.error('Error:', error);
            statusText.innerHTML = `<i class="fas fa-exclamation-circle"></i> Error: ${error.message}`;
            progressBar.style.backgroundColor = 'var(--error-color)';
        }
    }

    function formatDuration(seconds) {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    function updateDownloadLinks(parts) {
        const downloadContainer = document.getElementById('downloadContainer');
        const downloadsGrid = downloadContainer.querySelector('.downloads-grid');
        downloadsGrid.innerHTML = '';
        
        for (const [part, files] of Object.entries(parts)) {
            const partDiv = document.createElement('div');
            partDiv.className = 'download-part';
            
            const partTitle = document.createElement('h3');
            partTitle.textContent = `Part ${part.slice(-1)}`;
            
            const duration = document.createElement('p');
            duration.className = 'duration-text';
            duration.textContent = `Duration: ${formatDuration(files.duration)}`;
            
            const videoLink = document.createElement('a');
            videoLink.href = `/download/video/${files.video}`;
            videoLink.className = 'download-button';
            videoLink.innerHTML = '<i class="fas fa-video"></i> Download Video';
            
            const audioLink = document.createElement('a');
            audioLink.href = `/download/audio/${files.audio}`;
            audioLink.className = 'download-button';
            audioLink.innerHTML = '<i class="fas fa-music"></i> Download Audio';
            
            partDiv.appendChild(partTitle);
            partDiv.appendChild(duration);
            partDiv.appendChild(videoLink);
            partDiv.appendChild(audioLink);
            downloadsGrid.appendChild(partDiv);
        }
        
        downloadContainer.style.display = 'block';
    }

    document.querySelectorAll('.time-input input').forEach(input => {
        input.addEventListener('input', function() {
            let value = parseInt(this.value);
            const max = parseInt(this.max);
            const min = parseInt(this.min);

            if (value > max) this.value = max;
            if (value < min) this.value = min;
            if (isNaN(value)) this.value = 0;
        });
    });
});