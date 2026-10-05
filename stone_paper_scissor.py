# Wrote this code 2 yrs ago while learning tkinter and pygame it is not that good but okayish hope you like it; cant release the pygame version yet
import tkinter as tk
import random

choices = ["stone", "paper", "scissors"]
user_wins = 0
computer_wins = 0
target_wins = 10

def play(user_choice):
    global user_wins, computer_wins
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = f"Tie! Computer chose {computer_choice}"
    elif (user_choice == "stone" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "stone") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        result = f"You win! Computer chose {computer_choice}"
        user_wins += 1
    else:
        result = f"Computer wins! Computer chose {computer_choice}"
        computer_wins += 1

    label_result.config(text=result)
    label_score.config(text=f"Your Wins: {user_wins} | Computer Wins: {computer_wins}")

    if user_wins == target_wins:
        label_result.config(text="You reached 10 wins! Champion!")
        disable_buttons()
    elif computer_wins == target_wins:
        label_result.config(text="Computer reached 10 wins! Computer is Champion!")
        disable_buttons()

def disable_buttons():
    btn_stone.config(state="disabled")
    btn_paper.config(state="disabled")
    btn_scissors.config(state="disabled")

root = tk.Tk()
root.title("Rock Paper Scissors")

label_title = tk.Label(root, text="Rock Paper Scissors - First to 10 Wins", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

label_result = tk.Label(root, text="Make your choice!", font=("Arial", 14))
label_result.pack(pady=10)

label_score = tk.Label(root, text="Your Wins: 0 | Computer Wins: 0", font=("Arial", 12))
label_score.pack(pady=5)

stone_img = tk.PhotoImage(file="stone.png")
paper_img = tk.PhotoImage(file="paper.png")
scissors_img = tk.PhotoImage(file="scissors.png")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_stone = tk.Button(frame_buttons, image=stone_img, command=lambda: play("stone"))
btn_stone.grid(row=0, column=0, padx=10)

btn_paper = tk.Button(frame_buttons, image=paper_img, command=lambda: play("paper"))
btn_paper.grid(row=0, column=1, padx=10)

btn_scissors = tk.Button(frame_buttons, image=scissors_img, command=lambda: play("scissors"))
btn_scissors.grid(row=0, column=2, padx=10)

btn_quit = tk.Button(root, text="Quit", command=root.quit, width=12, height=2, bg="red", fg="white")
btn_quit.pack(pady=20)

root.mainloop()
