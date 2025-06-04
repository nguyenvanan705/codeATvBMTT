import os
import hashlib
import unicodedata
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

# Cấu hình quan trọng cho Windows
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Đảm bảo thư mục upload tồn tại
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Cấu hình SocketIO với async_mode và engineio_logger
socketio = SocketIO(app, 
                   async_mode='eventlet',
                   cors_allowed_origins="*",
                   engineio_logger=True,
                   logger=True)

available_files = {}

def safe_filename(filename):
    """Chuẩn hóa tên file an toàn"""
    filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    return secure_filename(filename)

def calculate_sha256(file_path):
    """Tính toán hash SHA-256"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Xử lý upload file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        filename = safe_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        file_hash = calculate_sha256(file_path)
        is_text = filename.lower().endswith('.txt')
        
        available_files[filename] = {
            'path': file_path,
            'hash': file_hash,
            'size': os.path.getsize(file_path),
            'is_text': is_text
        }
        
        socketio.emit('file_added', {
            'filename': filename,
            'hash': file_hash,
            'size': available_files[filename]['size'],
            'is_text': is_text
        }, namespace='/')
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'hash': file_hash,
            'is_text': is_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Xử lý download file"""
    if filename not in available_files:
        return jsonify({'error': 'File not found'}), 404
    
    file_info = available_files[filename]
    mimetype = 'text/plain' if file_info['is_text'] else 'application/octet-stream'
    
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=not file_info['is_text'],
            mimetype=mimetype
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view/<filename>', methods=['GET'])
def view_text_file(filename):
    """Xem nội dung file text"""
    if filename not in available_files or not available_files[filename]['is_text']:
        return jsonify({'error': 'File not found or not a text file'}), 404
    
    try:
        with open(available_files[filename]['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({
            'filename': filename,
            'content': content,
            'hash': available_files[filename]['hash']
        })
    except UnicodeDecodeError:
        try:
            with open(available_files[filename]['path'], 'r', encoding='latin-1') as f:
                content = f.read()
            return jsonify({
                'filename': filename,
                'content': content,
                'hash': available_files[filename]['hash']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify_file():
    """Kiểm tra tính toàn vẹn file"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        filename = data.get('filename')
        received_hash = data.get('hash')
        
        if not filename or not received_hash:
            return jsonify({'error': 'Missing filename or hash'}), 400
        
        if filename not in available_files:
            return jsonify({'error': 'File not found'}), 404
        
        file_info = available_files[filename]
        return jsonify({'verified': file_info['hash'] == received_hash})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect', namespace='/')
def handle_connect():
    """Xử lý kết nối socket"""
    try:
        emit('file_list', [
            {
                'filename': name,
                'hash': info['hash'],
                'size': info['size'],
                'is_text': info['is_text']
            } for name, info in available_files.items()
        ])
    except Exception as e:
        print(f"Socket error: {str(e)}")

@socketio.on('get_file_list', namespace='/')
def handle_get_file_list():
    """Gửi danh sách file khi client yêu cầu"""
    try:
        emit('file_list', [
            {
                'filename': name,
                'hash': info['hash'],
                'size': info['size'],
                'is_text': info['is_text']
            } for name, info in available_files.items()
        ])
    except Exception as e:
        print(f"Socket error: {str(e)}")

def cleanup_sockets():
    """Dọn dẹp socket khi tắt ứng dụng"""
    try:
        socketio.stop()
    except:
        pass

if __name__ == '__main__':
    try:
        print("Starting server...")
        socketio.run(app,
                   host='0.0.0.0',
                   port=8000,
                   debug=True,
                   use_reloader=False,
                   allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        cleanup_sockets()
        print("Server stopped")