import pygame
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
import os

# Initialize pygame mixer
pygame.mixer.init()

# Tkinter window
root = tk.Tk()
root.title("Python Music Player 🎶")
root.geometry("500x400")

# Playlist
playlist = []
current_song_index = 0
paused = False

# --- Functions ---
def add_song():
    file = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file:
        playlist.append(file)
        listbox.insert(tk.END, os.path.basename(file))

def play_song():
    global current_song_index, paused
    if playlist:
        if listbox.curselection():
            current_song_index = listbox.curselection()[0]
        song = playlist[current_song_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        paused = False
        update_song_info()
        update_progress_bar()

def pause_song():
    global paused
    pygame.mixer.music.pause()
    paused = True

def resume_song():
    global paused
    pygame.mixer.music.unpause()
    paused = False
    update_progress_bar()

def stop_song():
    pygame.mixer.music.stop()
    progress_var.set(0)

def next_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index + 1) % len(playlist)
        play_song()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(current_song_index)

def previous_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index - 1) % len(playlist)
        play_song()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(current_song_index)

def set_volume(val):
    volume = int(val) / 100
    pygame.mixer.music.set_volume(volume)

def update_song_info():
    if playlist:
        song = playlist[current_song_index]
        audio = MP3(song)
        song_label.config(text=f"Playing: {os.path.basename(song)} | Length: {int(audio.info.length)} sec")

def update_progress_bar():
    if playlist:
        song = playlist[current_song_index]
        audio = MP3(song)
        length = audio.info.length
        pos = pygame.mixer.music.get_pos() / 1000  # milliseconds to seconds
        if not paused:
            progress_var.set(pos)
        if pos >= length - 1:  # song finished
            next_song()
        root.after(1000, update_progress_bar)

# --- UI ---
listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=10)

# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Add Song", command=add_song).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Play", command=play_song).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Pause", command=pause_song).grid(row=0, column=2, padx=5)
tk.Button(frame, text="Resume", command=resume_song).grid(row=0, column=3, padx=5)
tk.Button(frame, text="Stop", command=stop_song).grid(row=0, column=4, padx=5)
tk.Button(frame, text="Previous", command=previous_song).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Next", command=next_song).grid(row=1, column=2, padx=5, pady=5)

# Volume slider
volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=5)

# Song info
song_label = tk.Label(root, text="No song playing", wraplength=400)
song_label.pack(pady=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = tk.Scale(root, variable=progress_var, from_=0, to=100, orient=tk.HORIZONTAL, length=400, label="Progress (sec)")
progress_bar.pack(pady=5)

# Start Tkinter event loop
root.mainloop()
