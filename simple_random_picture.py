import os
import random
import threading
import sqlite3
from flask import Flask, send_file

app = Flask(__name__)

ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
IMAGE_DIR = './'

REFRESH_INTERVAL_SECONDS = 5  # 默认刷新间隔时间，单位：秒

# 创建一个线程锁
db_lock = threading.Lock()

def get_db_connection():
    if 'db_connection' not in threading.current_thread().__dict__:
        threading.current_thread().db_connection = sqlite3.connect('image_paths.db')
    return threading.current_thread().db_connection

def get_db_cursor():
    return get_db_connection().cursor()

def load_image_paths():
    image_paths = []
    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                image_paths.append(os.path.join(root, file))
    return image_paths

def save_image_paths(image_paths):
    conn = get_db_connection()
    try:
        with conn:
            db_cursor = conn.cursor()
            # 创建表，如果不存在
            db_cursor.execute('CREATE TABLE IF NOT EXISTS image_paths (path TEXT)')
            db_cursor.execute('DELETE FROM image_paths')
            for path in image_paths:
                db_cursor.execute('INSERT INTO image_paths (path) VALUES (?)', (path,))
                print(f"插入数据：{path}")
            print("数据库已更新")
    except sqlite3.Error as e:
        print("Error while saving image paths:", e)


def get_random_image_path():
    db_cursor = get_db_cursor()
    db_cursor.execute('SELECT path FROM image_paths ORDER BY RANDOM() LIMIT 1')
    result = db_cursor.fetchone()
    if result:
        return result[0]
    else:
        return ""

@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_file(filename)

@app.route('/')
def random_image():
    random_image_path = get_random_image_path()
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>随机图片</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        main {{
            height: 80vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        img {{
            max-width: 100vw;
            max-height: 100vh;
            object-fit: contain;
        }}
    </style>
    <script>
        const REFRESH_INTERVAL_SECONDS = {REFRESH_INTERVAL_SECONDS};

        function refreshPage() {{
            location.reload();
        }}

        setTimeout(refreshPage, REFRESH_INTERVAL_SECONDS * 1000);
    </script>
</head>
<body>
    <main>
        <img src="/img/{random_image_path}" alt="随机图片">
    </main>
</body>
</html>
    '''

def ask_for_database_update():
    response = input("是否需要更新数据库内的数据？(y/n): ")
    return response.lower() == 'y'

if __name__ == '__main__':
    if ask_for_database_update():
        print("开始更新数据库...")
        with app.app_context():
            image_paths = load_image_paths()
            save_image_paths(image_paths)
        print("数据库更新完成")
    
    app.run()
