import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import os
import pygame

# Setup
# Get the directory where this script is located
script_dir = os.path.dirname(__file__)

# File Paths

main_gif_path = os.path.join(script_dir, "joke.gif")
jokes_file_path = os.path.join(script_dir, "randomJokes.txt")
bg_music_path = os.path.join(script_dir, "background.mp3")
punchline_sound_path = os.path.join(script_dir, "punchline.mp3")  # <-- NEW

# Initialize Pygame Audio
pygame.mixer.init()

# Load and play background Audio
pygame.mixer.music.load(bg_music_path)
pygame.mixer.music.play(-1)

# Load punchline sound effect
if os.path.exists(punchline_sound_path):
    punch_sound = pygame.mixer.Sound(punchline_sound_path)
else:
    punch_sound = None
    print("Warning: punchline.mp3 not found!")

# Load Jokes
def load_jokes():
    with open(jokes_file_path, "r", encoding="utf-8") as file:
        jokes_list = file.readlines()
    return [j.strip() for j in jokes_list if j.strip()]

jokes = load_jokes()
remaining_jokes = jokes.copy()
random.shuffle(remaining_jokes)

# Main Window
root = tk.Tk()
root.title("Alexa Joke Assistant")
root.geometry("600x400")
root.resizable(False, False)

# GIF Background
main_gif = Image.open(main_gif_path)

# Converting each GIF frame to ImageTk.PhotoImage and resize to fit window
main_frames = [ImageTk.PhotoImage(frame.copy().resize((600, 400))) for frame in ImageSequence.Iterator(main_gif)]
main_index = 0

# Label to display GIF frames
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

def update_main_gif():
    global main_index
    if main_index < len(main_frames):
        bg_label.config(image=main_frames[main_index])
        main_index += 1
        root.after(50, update_main_gif)
    else:
        # Keep last frame after GIF ends
        bg_label.config(image=main_frames[-1])

update_main_gif()

# Fonts
cartoon_font_setup = ("Comic Sans MS", 18, "bold")
cartoon_font_punch = ("Comic Sans MS", 16, "bold")

# Labels

setup_label = tk.Label(root, text="Click the button to hear a joke!", font=cartoon_font_setup,
                       fg="#FF69B4", bg="#FFFACD", wraplength=500, justify="center",
                       bd=5, relief="ridge")
setup_label.place(relx=0.5, rely=0.2, anchor="center")

punchline_label = tk.Label(root, text="", font=cartoon_font_punch,
                           fg="#8A2BE2", bg="#E0FFFF", wraplength=500, justify="center",
                           bd=5, relief="ridge")
punchline_label.place(relx=0.5, rely=0.4, anchor="center")

# Joke Logic
def get_random_joke():
    global current_setup, current_punchline, remaining_jokes
    
     # Refill remaining jokes if all have been shown
    if not remaining_jokes:
        remaining_jokes[:] = jokes.copy()
        random.shuffle(remaining_jokes)

    joke = remaining_jokes.pop()
    
    # Split joke into setup and punchline
    if "?" in joke:
        parts = joke.split("?", 1)
        current_setup = parts[0] + "?"
        current_punchline = parts[1].strip()
    elif "." in joke:
        parts = joke.split(".", 1)
        current_setup = parts[0] + "."
        current_punchline = parts[1].strip()
    else:
        current_setup = joke
        current_punchline = "No punchline found."

    setup_label.config(text=current_setup)
    punchline_label.config(text="")

    btn_joke.config(bg=random.choice(["#FFB6C1", "#FFD700", "#7CFC00", "#87CEEB", "#FF69B4"]))
    btn_punchline.config(bg=random.choice(["#FFA07A", "#ADFF2F", "#00CED1", "#EE82EE", "#FFC0CB"]))

def show_punchline():
    punchline_label.config(text=current_punchline)

    # Play funny punchline sound
    if punch_sound:
        punch_sound.play()

    btn_joke.config(bg=random.choice(["#FFB6C1", "#FFD700", "#7CFC00", "#87CEEB", "#FF69B4"]))
    btn_punchline.config(bg=random.choice(["#FFA07A", "#ADFF2F", "#00CED1", "#EE82EE", "#FFC0CB"]))

# Buttons
btn_joke = tk.Button(root, text="Alexa tell me a Joke", command=get_random_joke, width=25, bg="#FFB6C1")
btn_joke.place(relx=0.5, rely=0.65, anchor="center")

btn_punchline = tk.Button(root, text="Show Punchline", command=show_punchline, width=25, bg="#FFA07A")
btn_punchline.place(relx=0.5, rely=0.75, anchor="center")

btn_quit = tk.Button(root, text="Quit", command=root.quit, width=25, bg="#D3D3D3")
btn_quit.place(relx=0.5, rely=0.85, anchor="center")

# Start
root.mainloop()
