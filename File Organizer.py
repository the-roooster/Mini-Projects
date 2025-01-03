import tkinter as tk
from tkinter import filedialog
import os
import shutil
import tempfile

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        original_folder_contents = get_folder_contents(folder_path)
        try:
            sort_files(folder_path)
        except Exception as e:
            show_error_message(f"An error occurred: {e}")
            revert_changes(folder_path, original_folder_contents)
        else:
            show_success_message("Files sorted successfully!")
def sort_files(folder_path):
    file_types = {
        'documents': ['.doc', '.docx', '.pdf', '.txt'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'videos': ['.mp4', '.avi', '.mov', '.mkv'],
        'audio': ['.mp3', '.wav', '.flac']
    }
    for file_type, extensions in file_types.items():
        subfolder_path = os.path.join(folder_path, file_type)
        os.makedirs(subfolder_path, exist_ok=True)
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in extensions:
                    shutil.move(filepath, os.path.join(subfolder_path, filename))
def get_folder_contents(folder_path):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            temp_file.write(f"{filepath}\n")
    return temp_file.name
def revert_changes(folder_path, temp_file_path):
    with open(temp_file_path, 'r') as temp_file:
        for line in temp_file:
            filepath = line.strip()
            if os.path.isfile(filepath):
                os.remove(filepath)
    with open(temp_file_path, 'r') as temp_file:
        for line in temp_file:
            filepath = line.strip()
            try:
                shutil.copy(filepath, folder_path)
            except FileNotFoundError:
                pass
    os.remove(temp_file_path)
def show_success_message(message):
    success_window = tk.Toplevel()
    success_window.title("Success")
    success_label = tk.Label(success_window, text=message)
    success_label.pack(pady=20)
    success_window.after(2000, success_window.destroy)  # Close window after 2 seconds
def show_error_message(message):
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_label = tk.Label(error_window, text=message)
    error_label.pack(pady=20)
    error_window.after(2000, error_window.destroy)  # Close window after 2 seconds
def main():
    root = tk.Tk()
    root.title("File Sorter")
    button = tk.Button(root, text="Select Folder", command=select_folder)
    button.pack(pady=20)
    root.mainloop()
if __name__ == "__main__":
    main()