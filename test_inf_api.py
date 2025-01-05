import tkinter as tk
from tkinter import messagebox
import requests
import random

def get_trivia_questions(amount=10):
    url = f"https://the-trivia-api.com/v2/questions?limit={amount}"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        print("Failed to fetch trivia questions.")
        return None
    
    questions = []
    for question_data in data:
        question = question_data['question']['text']
        correct_answer = question_data['correctAnswer']
        incorrect_answers = question_data['incorrectAnswers']
        category = question_data['category']
        difficulty = question_data['difficulty']
        
        hint = f"Category: {category}, Difficulty: {difficulty}"
        explanation = f"No explanation available"
        
        questions.append({
            'question': question,
            'correct_answer': correct_answer,
            'incorrect_answers': incorrect_answers,
            'category': category,
            'difficulty': difficulty,
            'hint': hint,
            'explanation': explanation
        })
    
    return questions

def display_question():
    global current_question
    current_question = random.choice(trivia_questions)
    question_label.config(text=current_question['question'])
    hint_button.config(state=tk.NORMAL)
    answer_entry.delete(0, tk.END)
    explanation_label.config(text="")

def show_hint():
    hint = current_question.get('hint', 'No hint available')
    messagebox.showinfo("Hint", hint)

def check_answer():
    user_answer = answer_entry.get().strip()
    correct_answer = current_question['correct_answer']
    explanation = current_question.get('explanation', 'No explanation available')
    
    if user_answer.lower() == correct_answer.lower():
        result = "Correct!"
    else:
        result = f"Incorrect! The correct answer is: {correct_answer}"
    
    explanation_label.config(text=f"{result}\nExplanation: {explanation}")

trivia_questions = get_trivia_questions(10)

root = tk.Tk()
root.title("Trivia Quiz")

question_label = tk.Label(root, text="", wraplength=400, justify="left")
question_label.pack(pady=10)

answer_entry = tk.Entry(root, width=50)
answer_entry.pack(pady=5)

answer_button = tk.Button(root, text="Submit Answer", command=check_answer)
answer_button.pack(pady=5)

hint_button = tk.Button(root, text="Show Hint", command=show_hint)
hint_button.pack(pady=5)

explanation_label = tk.Label(root, text="", wraplength=400, justify="left")
explanation_label.pack(pady=10)

next_question_button = tk.Button(root, text="Next Question", command=display_question)
next_question_button.pack(pady=5)

display_question()

root.mainloop()