import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import pygame

# Initialize pygame mixer for sounds and music _____________________________________________________________________________________________________________________
pygame.mixer.init()

# Global variables for sound settings ______________________________________________________________________________________________________________________________
sound_effect_volume = 50
music_volume = 50
selected_style = "Classic"
player_score = 0
computer_score = 0

# Load sound effects and music _____________________________________________________________________________________________________________________________________
button_click_sound = pygame.mixer.Sound("button_click.wav")
button_click_sound.set_volume(sound_effect_volume / 100)
background_music = "background_music.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(music_volume / 100)
pygame.mixer.music.play(-1)  # Loop music indefinitely

# Load images _______________________________________________________________________________________________________________________________________________________
background_main = "background_main.png"
background_settings = "background_settings.png"
background_styles = "background_styles.png"
background_game = "background_game.png"

card_images = {
    "Classic": {
        "rock": "classic_rock.png",
        "paper": "classic_paper.png",
        "scissors": "classic_scissors.png"
    },
    "Modern": {
        "rock": "modern_rock.png",
        "paper": "modern_paper.png",
        "scissors": "modern_scissors.png"
    },
    "Fantasy": {
        "rock": "fantasy_rock.png",
        "paper": "fantasy_paper.png",
        "scissors": "fantasy_scissors.png"
    }
}

# Function to resize an image _______________________________________________________________________________________________________________________________________
def resize_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize(size, Image.Resampling.LANCZOS) 
    return ImageTk.PhotoImage(image)

# Function to play a sound effect ____________________________________________________________________________________________________________________________________
def play_sound_effect():
    button_click_sound.play()

# Function to open the settings window _______________________________________________________________________________________________________________________________
def open_settings():
    play_sound_effect()

    def update_sound_effect(value):
        global sound_effect_volume
        sound_effect_volume = float(value)
        button_click_sound.set_volume(sound_effect_volume / 100)

    def update_music(value):
        global music_volume
        music_volume = float(value)
        pygame.mixer.music.set_volume(music_volume / 100)

    def close_settings():
        play_sound_effect()
        settings_window.destroy()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x400")
    settings_window.resizable(False, False)

    bg_image = resize_image(background_settings, (500, 400))
    bg_label = tk.Label(settings_window, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)

    # Sound effect volume slider __________________________________________________________________________________________
    tk.Label(settings_window, text="Sound Effects Volume:", bg="#f0f0f0", font=("Arial", 16)).pack(pady=10)
    sound_effect_slider = ttk.Scale(settings_window, from_=0, to=100, orient="horizontal", command=update_sound_effect)
    sound_effect_slider.set(sound_effect_volume)
    sound_effect_slider.pack(pady=5)

    # Music volume slider __________________________________________________________________________________________________
    tk.Label(settings_window, text="Music Volume:", bg="#f0f0f0", font=("Arial", 16)).pack(pady=10)
    music_slider = ttk.Scale(settings_window, from_=0, to=100, orient="horizontal", command=update_music)
    music_slider.set(music_volume)
    music_slider.pack(pady=5)

    # Back button __________________________________________________________________________________________________________
    back_button = tk.Button(settings_window, text="Back to Menu", command=close_settings, font=("Arial", 16))
    back_button.pack(pady=20)

# Function to open the card style selection window _____________________________________________________________________________________________________________________________________
def open_card_style():
    play_sound_effect()

    def select_style(style):
        global selected_style
        selected_style = style
        play_sound_effect()
        messagebox.showinfo("Style Selected", f"You selected the {style} style!")
        card_style_window.destroy()

    def go_back_to_menu():
        play_sound_effect()
        card_style_window.destroy()

    card_style_window = tk.Toplevel(root)
    card_style_window.title("Select Card Style")
    card_style_window.geometry("600x500")
    card_style_window.resizable(False, False)

    bg_image = resize_image(background_styles, (600, 500))
    bg_label = tk.Label(card_style_window, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)

    tk.Label(card_style_window, text="Choose Your Card Style:", font=("Arial", 18), bg="#f0f0f0").pack(pady=20)

    styles = ["Classic", "Modern", "Fantasy"]
    for style in styles:
        style_button = tk.Button(card_style_window, text=style, command=lambda s=style: select_style(s), font=("Arial", 16))
        style_button.pack(pady=10)

    back_button = tk.Button(card_style_window, text="Back to Menu", command=go_back_to_menu, font=("Arial", 16))
    back_button.pack(pady=20)

# Function to start the game _____________________________________________________________________________________________________________________________________
def start_game():
    play_sound_effect()

    def play_round(player_choice):
        global player_score, computer_score
        rps = ["rock", "paper", "scissors"]
        computer_choice = random.choice(rps)

        fixed_size = (150, 200)

        player_img = resize_image(card_images[selected_style][player_choice], fixed_size)
        computer_img = resize_image(card_images[selected_style][computer_choice], fixed_size)

        player_card.config(image=player_img)
        computer_card.config(image=computer_img)
        player_card.image = player_img
        computer_card.image = computer_img

        result = determine_winner(player_choice, computer_choice)
        result_label.config(text=result)

        if "Win" in result:
            player_score += 1
        elif "Lose" in result:
            computer_score += 1

        if player_score == 3 or computer_score == 3:
            show_winner()

    def determine_winner(player, computer):
        if player == computer:
            return "It's a Tie!"
        results = {
            ("rock", "scissors"): "You Win!",
            ("rock", "paper"): "You Lose!",
            ("paper", "rock"): "You Win!",
            ("paper", "scissors"): "You Lose!",
            ("scissors", "paper"): "You Win!",
            ("scissors", "rock"): "You Lose!"
        }
        return results.get((player, computer), "Invalid Result")

    def show_winner():
        winner = "You" if player_score > computer_score else "Computer"
        winner_window = tk.Toplevel(root)
        winner_window.title("Game Over")
        winner_window.geometry("400x300")
        winner_window.resizable(False, False)
        tk.Label(winner_window, text=f"{winner} won the game!", font=("Arial", 16)).pack(pady=20)

    game_window = tk.Toplevel(root)
    game_window.title("Rock Paper Scissors Game")
    game_window.geometry("800x600")
    game_window.resizable(False, False)

    bg_image = resize_image(background_game, (800, 600))
    bg_label = tk.Label(game_window, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relwidth=1, relheight=1)

    # Cards and labels _____________________________________________________________________________________________________________________________________
    tk.Label(game_window, text="Rock Paper Scissors", font=("Arial", 20), bg="#f0f0f0").pack(pady=10)

    cards_frame = tk.Frame(game_window, bg="#f0f0f0")
    cards_frame.pack(pady=20)

    player_card = tk.Label(cards_frame, bg="#f0f0f0")
    player_card.grid(row=0, column=0, padx=20)

    computer_card = tk.Label(cards_frame, bg="#f0f0f0")
    computer_card.grid(row=0, column=2, padx=20)

    tk.Button(cards_frame, text="Rock", command=lambda: play_round("rock"), font=("Arial", 16)).grid(row=1, column=0)
    tk.Button(cards_frame, text="Paper", command=lambda: play_round("paper"), font=("Arial", 16)).grid(row=1, column=1)
    tk.Button(cards_frame, text="Scissors", command=lambda: play_round("scissors"), font=("Arial", 16)).grid(row=1, column=2)

    result_label = tk.Label(game_window, text="", font=("Arial", 16), bg="#f0f0f0")
    result_label.pack(pady=20)

# Main window setup _____________________________________________________________________________________________________________________________________
root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("800x600")
root.resizable(False, False)

bg_image = resize_image(background_main, (800, 600))
bg_label = tk.Label(root, image=bg_image)
bg_label.image = bg_image
bg_label.place(relwidth=1, relheight=1)

tk.Label(root, text="Rock Paper Scissors", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

tk.Button(root, text="Start Game", command=start_game, width=20, font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Select Card Style", command=open_card_style, width=20, font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Settings", command=open_settings, width=20, font=("Arial", 16)).pack(pady=10)

root.mainloop()

