import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
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

def get_kanye():
    url = "https://api.kanye.rest/"
    try:
        # fetches url
        response = requests.get(url)
        # checks to see if url is available
        response.raise_for_status()
        # retrieves data in a json format
        data = response.json()
        return data['quote']
    except Exception as e:
        return f"Error: {e}"

def get_uselessFact():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    try:
        # fetches url
        response = requests.get(url)
        # checks to see if url is available
        response.raise_for_status()
        # retrieves data in a json format
        data = response.json()
        return data['text']
    except Exception as e:
        return f"Error: {e}"

def get_cocktail():
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['drinks']:
            drink = data['drinks'][0]
            name = drink['strDrink']
            instructions = drink['strInstructions']
            # Gather ingredients and measures
            ingredients = []
            for i in range(1, 16):  # The API provides up to 15 ingredients
                ingredient = drink.get(f"strIngredient{i}")
                measure = drink.get(f"strMeasure{i}")
                if ingredient:
                    ingredients.append(f"{measure.strip() if measure else ''} {ingredient.strip()}".strip())
            ingredients_list = "\n".join(ingredients)

            # Format the result
            result = f"Name: {name}\n\nIngredients:\n{ingredients_list}\n\nInstructions:\n{instructions}"
            return result
        else:
            return "No cocktail data found."
    except Exception as e:
        return f"Error: {e}"

# Prompts for an ingredient, e.g., vodka.
# Displays a list of cocktails containing vodka.
def get_cocktail_by_ingredient(ingredient):
    url = f"https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={ingredient}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['drinks']:
            cocktails = [drink['strDrink'] for drink in data['drinks']]
            # Format the cocktail names into a string
            return f"Cocktails with {ingredient}:\n" + "\n".join(cocktails)
        else:
            return f"No cocktails found with the ingredient: {ingredient}"
    except Exception as e:
        return f"Error: {e}"

# Add an input dialog for ingredient selection
def fetch_cocktail_by_ingredient():
    ingredient = tk.simpledialog.askstring("Input", "Enter an ingredient:")
    if ingredient:
        result = get_cocktail_by_ingredient(ingredient)
        messagebox.showinfo("Cocktail by Ingredient", result)


# Updated Cocktail Function
# Displays a random cocktail's name, ingredients, and instructions. If they type random
# A dialog appears asking:
# Type 'random' for a random cocktail or 'ingredient' to search by ingredient.
def cocktail_options():
    # Prompt user for an option: Random or By Ingredient
    choice = simpledialog.askstring(
        "Cocktail Options",
        "Type 'random' for a random cocktail or 'ingredient' to search by ingredient:"
    )
    
    if not choice:
        return  # User canceled or left input blank
    
    choice = choice.lower().strip()
    if choice == "random":
        result = get_cocktail()
    elif choice == "ingredient":
        ingredient = simpledialog.askstring("Ingredient Input", "Enter an ingredient:")
        if ingredient:
            result = get_cocktail_by_ingredient(ingredient)
        else:
            result = "No ingredient provided."
    else:
        result = "Invalid option. Please choose 'random' or 'ingredient'."
    
    # Display the result
    messagebox.showinfo("Cocktail Generator", result)

# GUI Functionality
def fetch_data(api_choice):
    if api_choice == "Evil Insult":
        result = get_evil_insult()
    elif api_choice == "Affirmation":
        result = get_affirmation()
    elif api_choice == "Advice":
        result = get_advice()
    elif api_choice == "Kanye Quote":
        result = get_kanye()
    elif api_choice == "Random Useless Fact":
        result = get_uselessFact()
    elif api_choice == "Cocktail":
        result = get_cocktail()
    else:
        result = "Invalid API choice."
    
    # Display result in a messagebox
    messagebox.showinfo(api_choice, result)

# Main GUI Application
def main():
    # Initialize window
    window = tk.Tk()
    window.title("Mood Mate")
    window.geometry("400x600")
    window.resizable(False, False) # width, height

    # Heading
    heading = tk.Label(window, text="Choose a Mood You Want to Feel", font=("Arial", 14))
    heading.pack(pady=20)

    # Buttons for APIs
    # Evil Insult Btn
    evil_insult_btn = tk.Button(window, text="Evil Insult Generator", font=("Arial", 12), command=lambda: fetch_data("Evil Insult"))
    evil_insult_btn.pack(pady=5)

    # Affirmation Btn
    affirmation_btn = tk.Button(window, text="Affirmation Generator", font=("Arial", 12), command=lambda: fetch_data("Affirmation"))
    affirmation_btn.pack(pady=5)

    # Advicee Btn
    advice_btn = tk.Button(window, text="Advice Slip Generator", font=("Arial", 12), command=lambda: fetch_data("Advice"))
    advice_btn.pack(pady=5)

    # Kanye Quote Btn
    kanye_btn = tk.Button(window, text="Kanye Quote", font=("Arial", 12), command=lambda: fetch_data("Kanye Quote"))
    kanye_btn.pack(pady=5)

    #Random Useless Fact Btn
    uselessFact_btn = tk.Button(window, text="Random Useless Fact", font=("Arial", 12), command=lambda: fetch_data("Random Useless Fact"))
    uselessFact_btn.pack(pady=5)

    # Cocktail Btn
    cocktail_btn = tk.Button(window, text="Cocktail Generator", font=("Arial", 12), command=cocktail_options)
    cocktail_btn.pack(pady=5)

    # Exit Button
    exit_btn = tk.Button(window, text="Exit", font=("Arial", 12), fg="red", command=window.quit)
    exit_btn.pack(pady=20)

    # Run the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
