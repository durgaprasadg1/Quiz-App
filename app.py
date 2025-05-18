from tkinter import *
import tkinter as tk
import requests
import html
import random

root = tk.Tk()
root.title("Quiz App")
root.geometry("950x400")
root.resizable(False, False)
root.config(bg="lightblue")

questionS = ''
options = []
qNo = 0
score = 0
correct_option = ''

def get_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    data = response.json()
    if data["response_code"] == 0:
        q = data["results"][0]
        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrect = [html.unescape(ans) for ans in q["incorrect_answers"]]
        options_list = incorrect + [correct]
        random.shuffle(options_list)
        return {
            "question": question,
            "options": options_list,
            "correct": correct
        }
    else:
        return None

selectedOption = IntVar()


text = Label(root, font=("courier", 10, "bold"), bg="#356696", height=5, width=120)
text.grid(row=0, column=0, padx=0, pady=10)

def nextQue():
    global options, correct_option
    q_data = get_question()
    if q_data:
        questionS = q_data["question"]
        text.config(text=questionS) 
        
        
        for widget in options:
            widget.destroy()
        options.clear()

        correct_option = q_data["correct"]
        for idx, opt in enumerate(q_data["options"], 1):
            button = tk.Radiobutton(root, text=opt, variable=selectedOption, value=idx, anchor="w", width=30)
            button.grid(row=idx, column=0, padx=10, pady=5, sticky="w")  # Adjusted row positions
            options.append(button)

def show_selection():
    global score, qNo
    try:
        selection = selectedOption.get()
        selectedOption.set(0)  

        if selection == 0:
            return 

        selected_text = options[selection-1].cget("text")
        if selected_text == correct_option:
            score += 1
        else:
            score -= 1

        qNo += 1
       
        scoreCard.config(text=f"Score: {score}")
        QueCard.config(text=f"Question: {qNo}")
        nextQue()

    except Exception as err:
        print(f"An error occurred: {err}")


nextQue()

def reset_quiz():
    global score, qNo
    score = 0
    qNo = 0
    selectedOption.set(0)
    scoreCard.config(text=f"Score: {score}")
    QueCard.config(text=f"Question: {qNo}")
    nextQue()

btn = tk.Button(root, text="Submit", command=show_selection)
btn.grid(row=5, column=0, pady=10)  

reset_btn = tk.Button(root, text="Reset Quiz", command=reset_quiz)
reset_btn.grid(row=6, column=0, pady=10)

scoreCard = Label(root, text=f"Score: {score}", font=("courier", 12))
scoreCard.grid(row=7, column=0 )
QueCard = Label(root, text=f"Question: {qNo}", font=("courier", 12))
QueCard.grid(row=8, column=0,pady=10)

root.mainloop()