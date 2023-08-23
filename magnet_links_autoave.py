import re
import clipboard
import shutil
import os
import time

def extract_magnet_links(text):
    magnet_links = re.findall(r'magnet:\?[^"\']+', text)
    return magnet_links

def save_links_to_file(links):
    with open('links.txt', 'a') as f:
        for link in links:
            f.write(link + '\n')

def display_saved_links(links):
    print("Saved Magnet Links:")
    for link in links:
        print(link)

def create_backup():
    if os.path.exists('links.txt'):
        shutil.copy2('links.txt', 'links_backup.txt')

def remove_backup():
    if os.path.exists('links_backup.txt'):
        os.remove('links_backup.txt')

def remove_duplicates_and_save():
    unique_links = set()

    with open('links.txt', 'r') as f:
        for line in f:
            unique_links.add(line.strip())

    with open('links.txt', 'w') as f:
        for link in unique_links:
            f.write(link + '\n')

def main():
    prev_clipboard_text = ""
    while True:
        clipboard_text = clipboard.paste()

        if clipboard_text != prev_clipboard_text:
            magnet_links = extract_magnet_links(clipboard_text)

            if magnet_links:
                save_links_to_file(magnet_links)
                display_saved_links(magnet_links)
                print("Magnet links saved to links.txt")
                
            prev_clipboard_text = clipboard_text

        time.sleep(1)  # Wait for 1 second before checking again

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        create_backup()
        remove_duplicates_and_save()
        remove_backup()
        print("Duplicates removed from links.txt, backup created and removed")
