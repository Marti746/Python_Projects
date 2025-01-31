import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from api_key import API_KEY 

# Constants
MY_KEY = API_KEY
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"

def fetch_recommended_shows():
    """Fetch trending shows from TMDb API."""
    url = f"{BASE_URL}/trending/all/week?api_key={MY_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("results", [])[:10]  # Get top 10 results
    return []

def display_recommended_shows(parent, add_to_db):
    """Display recommended shows in the main page."""
    recommended_shows = fetch_recommended_shows()

    # Create Frame for Recommendations
    recommendations_frame = tk.Frame(parent)
    recommendations_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(recommendations_frame, text="Recommended Shows", font=("Arial", 14, "bold")).pack(pady=5)

    for show in recommended_shows:
        title = show.get("title") or show.get("name", "Unknown")
        poster_path = show.get("poster_path")
        full_poster_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None

        # Determine the type (movie or TV show)
        if "media_type" in show:
            show_type = "Movie" if show["media_type"] == "movie" else "TV Show"
        else:
            show_type = "Movie" if "title" in show else "TV Show"  # Heuristic check    

        frame = tk.Frame(recommendations_frame, pady=5)
        frame.pack(fill="x", padx=10)

        # Load Poster Image
        if full_poster_url:
            try:
                response = requests.get(full_poster_url)
                img = Image.open(BytesIO(response.content))
                img = img.resize((50, 75), Image.ANTIALIAS)
                poster_image = ImageTk.PhotoImage(img)

                img_label = tk.Label(frame, image=poster_image)
                img_label.image = poster_image  # Keep a reference
                img_label.pack(side="left", padx=5)
            except Exception:
                pass  # Fallback in case image fails

        # Show Title
        title_label = tk.Label(frame, text=title, font=("Arial", 12), anchor="w")
        title_label.pack(side="left", padx=10)

        # Add to Profile Button
        add_button = tk.Button(frame, text="Add", command=lambda t=title, p=poster_path: add_to_db(t, "Plan to Watch", p))
        add_button.pack(side="right", padx=5)

    return recommendations_frame
