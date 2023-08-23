import time
import re
import clipboard

url_pattern = re.compile(r'https?://.*jable')
previous_clipboard_text = None

while True:
    clipboard_text = clipboard.paste()
    
    if clipboard_text != previous_clipboard_text:
        if url_pattern.search(clipboard_text):
            with open('url.txt', 'a') as f:
                f.write(clipboard_text + '\n')
            print(f'"{clipboard_text}" 已成功保存到 url.txt')
        
        previous_clipboard_text = clipboard_text
    
    time.sleep(5)
