import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import pygame
import os

# ----------------------------
# SETUP PATHS (works inside folder)
# ----------------------------
script_dir = os.path.dirname(__file__)  # folder where this script is
bg_music_path = os.path.join(script_dir, "background.mp3")
correct_sound_path = os.path.join(script_dir, "correct.mp3")
wrong_sound_path = os.path.join(script_dir, "wrong.mp3")
gif_path = os.path.join(script_dir, "menu.gif")

# ----------------------------
# INITIALIZE PYGAME
# ----------------------------
pygame.mixer.init()

def safe_load_sound(file_path):
    if os.path.exists(file_path):
        return pygame.mixer.Sound(file_path)
    else:
        print(f"Warning: {file_path} not found!")
        return None

# Background music
if os.path.exists(bg_music_path):
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
else:
    print("Warning: background.mp3 not found!")

# Correct/Wrong sounds
correct_sound = safe_load_sound(correct_sound_path)
wrong_sound = safe_load_sound(wrong_sound_path)

# ----------------------------
# GLOBAL VARIABLES
# ----------------------------
score = 0
current_question = 0
attempts = 0
difficulty = 1
num1, num2 = 0, 0
operation = "+"

# ----------------------------
# GIF BACKGROUND FUNCTION
# ----------------------------
def load_gif_background_once(frame, gif_path, width, height):
    if not os.path.exists(gif_path):
        print(f"Warning: {gif_path} not found!")
        return
    gif = Image.open(gif_path)
    frames = [ImageTk.PhotoImage(f.copy().resize((width, height))) for f in ImageSequence.Iterator(gif)]
    frame.frames = frames  # keep reference
    label = tk.Label(frame)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    def animate(ind=0):
        label.config(image=frame.frames[ind])
        ind += 1
        if ind < len(frame.frames):
            frame.after(100, animate, ind)
    animate()
    return label

# ----------------------------
# MODAL POPUP FUNCTION
# ----------------------------
def show_modal(message, color, sound=None):
    if sound:
        try:
            sound.play()
        except:
            pass
    modal = tk.Toplevel(root)
    modal.overrideredirect(True)
    modal.geometry(f"400x100+{root.winfo_x()+100}+{root.winfo_y()+175}")
    modal.config(bg="#1d4031")
    tk.Label(modal, text=message, font=("Comic Sans MS", 18, "bold"),
             fg=color, bg="#1d4031").pack(expand=True)
    modal.after(1200, modal.destroy)

# ----------------------------
# QUIZ FUNCTIONS
# ----------------------------
def display_menu():
    menu_frame.pack(fill="both", expand=True)
    quiz_frame.pack_forget()
    result_frame.pack_forget()

def random_numbers(level):
    if level == 1:
        return random.randint(0,9), random.randint(0,9)
    elif level == 2:
        return random.randint(10,99), random.randint(10,99)
    else:
        return random.randint(1000,9999), random.randint(1000,9999)

def choose_operation():
    return random.choice(["+", "-"])

def show_problem():
    global num1, num2, operation, attempts, current_question
    if current_question >= 10:
        show_results()
        return
    num1, num2 = random_numbers(difficulty)
    operation = choose_operation()
    attempts = 0
    problem_label.config(text=f"{num1} {operation} {num2} = ?")
    question_label.config(text=f"Question: {current_question+1}/10")
    score_label.config(text=f"Score: {score}")
    answer_entry.delete(0, tk.END)

def check_answer():
    global score, attempts, current_question
    try:
        user = int(answer_entry.get())
    except:
        show_modal("Enter a valid number!", "#fa9876")
        return

    correct = num1 + num2 if operation == "+" else num1 - num2

    if user == correct:
        score += 10 if attempts == 0 else 5
        show_modal("✅ Correct!", "#00ff00", correct_sound)
        current_question += 1
        show_problem()
    else:
        attempts += 1
        if attempts < 2:
            show_modal("❌ Wrong! Try again.", "#ff4500", wrong_sound)
        else:
            show_modal(f"❌ Wrong! Correct: {correct}", "#ff4500", wrong_sound)
            current_question += 1
            show_problem()

    score_label.config(text=f"Score: {score}")
    question_label.config(text=f"Question: {current_question+1}/10")

def show_results():
    quiz_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)
    if score>=90: grade="A+ 🎉"
    elif score>=75: grade="A 👍"
    elif score>=50: grade="B 🙂"
    else: grade="C 😐"
    result_label.config(text=f"Score: {score}/100\nGrade: {grade}")

def start_quiz(level):
    global difficulty, score, current_question
    difficulty = level
    score=0
    current_question=0
    menu_frame.pack_forget()
    result_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)
    show_problem()

def play_again():
    display_menu()

# ----------------------------
# MAIN WINDOW
# ----------------------------
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("600x450")
root.resizable(False, False)

# ----------------------------
# FRAMES
# ----------------------------
menu_frame = tk.Frame(root, width=600, height=450)
quiz_frame = tk.Frame(root, width=600, height=450)
result_frame = tk.Frame(root, width=600, height=450)

# ----------------------------
# LOAD GIF BACKGROUND
# ----------------------------
load_gif_background_once(menu_frame, gif_path, 600, 450)
load_gif_background_once(quiz_frame, gif_path, 600, 450)
load_gif_background_once(result_frame, gif_path, 600, 450)

# ----------------------------
# MENU FRAME
# ----------------------------
tk.Label(menu_frame, text="Select Difficulty", font=("Comic Sans MS",24,"bold"),
         fg="#fa9876", bg="#1d4031").pack(pady=80)

button_frame = tk.Frame(menu_frame, bg="#1d4031")
button_frame.pack(pady=10)
tk.Button(button_frame,text="Easy", width=15,bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=lambda: start_quiz(1)).grid(row=0,column=0,padx=5)
tk.Button(button_frame,text="Moderate", width=15,bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=lambda: start_quiz(2)).grid(row=0,column=1,padx=5)
tk.Button(button_frame,text="Advanced", width=15,bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=lambda: start_quiz(3)).grid(row=0,column=2,padx=5)

# ----------------------------
# QUIZ FRAME
# ----------------------------
question_label = tk.Label(quiz_frame,text="Question: 1/10",font=("Comic Sans MS",16,"bold"),
                          fg="#fa9876", bg="#1d4031")
question_label.pack(pady=(60,5))
score_label = tk.Label(quiz_frame,text="Score: 0",font=("Comic Sans MS",16,"bold"),
                       fg="#fa9876", bg="#1d4031")
score_label.pack(pady=5)

problem_label = tk.Label(quiz_frame,text="",font=("Comic Sans MS",20,"bold"),
                         fg="#fa9876", bg="#1d4031")
problem_label.pack(pady=20)

answer_entry = tk.Entry(quiz_frame,font=("Comic Sans MS",16,"bold"), bg="#1d4031", fg="#fa9876",
                        insertbackground="#fa9876")
answer_entry.pack(pady=10)

tk.Button(quiz_frame,text="Submit",bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=check_answer).pack(pady=10)

# ----------------------------
# RESULT FRAME
# ----------------------------
result_label = tk.Label(result_frame,text="",font=("Comic Sans MS",24,"bold"),
                        fg="#fa9876", bg="#1d4031")
result_label.pack(pady=150)
tk.Button(result_frame,text="Play Again",bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=play_again).pack(pady=10)
tk.Button(result_frame,text="Exit",bg="#1d4031",fg="#fa9876",
          font=("Comic Sans MS",14,"bold"), command=root.quit).pack(pady=10)

# Start with menu
display_menu()
root.mainloop()
