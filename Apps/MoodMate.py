import tkinter as tk
from tkinter import messagebox
import requests

# Functions to fetch API data
def get_evil_insult():
    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['insult']
    except Exception as e:
        return f"Error: {e}"

def get_affirmation():
    url = "https://www.affirmations.dev/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['affirmation']
    except Exception as e:
        return f"Error: {e}"

def get_advice():
    url = "https://api.adviceslip.com/advice"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['slip']['advice']
    except Exception as e:
        return f"Error: {e}"

# GUI Functionality
def fetch_data(api_choice):
    if api_choice == "Evil Insult":
        result = get_evil_insult()
    elif api_choice == "Affirmation":
        result = get_affirmation()
    elif api_choice == "Advice":
        result = get_advice()
    else:
        result = "Invalid API choice."
    
    # Display result in a messagebox
    messagebox.showinfo(api_choice, result)

# Main GUI Application
def main():
    # Initialize window
    window = tk.Tk()
    window.title("Multi-API Fetcher")
    window.geometry("400x300")
    window.resizable(False, False)

    # Heading
    heading = tk.Label(window, text="Choose an API to Fetch Data", font=("Arial", 14))
    heading.pack(pady=20)

    # Buttons for APIs
    evil_insult_btn = tk.Button(window, text="Evil Insult Generator", font=("Arial", 12), command=lambda: fetch_data("Evil Insult"))
    evil_insult_btn.pack(pady=5)

    affirmation_btn = tk.Button(window, text="Affirmation Generator", font=("Arial", 12), command=lambda: fetch_data("Affirmation"))
    affirmation_btn.pack(pady=5)

    advice_btn = tk.Button(window, text="Advice Slip Generator", font=("Arial", 12), command=lambda: fetch_data("Advice"))
    advice_btn.pack(pady=5)

    # Exit Button
    exit_btn = tk.Button(window, text="Exit", font=("Arial", 12), fg="red", command=window.quit)
    exit_btn.pack(pady=20)

    # Run the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
