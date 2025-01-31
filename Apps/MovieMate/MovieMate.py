import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import requests
from io import BytesIO
# other python file imports
import recommendations
from api_key import API_KEY 

# Constants
API_KEY = API_KEY
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"

class ShowTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Mate")
        self.root.geometry("800x600")

        # Database connection
        self.conn = sqlite3.connect("movie_mate.db")
        self.create_tables()

        # Initialize notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.main_page = tk.Frame(self.notebook)
        self.profile_page = tk.Frame(self.notebook)
        self.notebook.add(self.main_page, text="Main Page")
        self.notebook.add(self.profile_page, text="Profile")

        # Create pages
        self.sort_option = tk.StringVar(value="None")
        self.create_main_page()
        self.create_profile_page()
        self.update_profile_tabs()

    def create_tables(self):
        """Creates necessary tables in the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                score INTEGER,
                poster_path TEXT,
                type TEXT
            )
        """)
        self.conn.commit()

    def create_main_page(self):
        """Creates the main page layout and ensures the search bar remains visible."""
        if not hasattr(self, "main_frame"):  # Ensure we don't re-create elements
            self.main_frame = tk.Frame(self.main_page)
            self.main_frame.pack(fill=tk.BOTH, expand=True)

            title_label = tk.Label(self.main_frame, text="Show Tracker", font=("Arial", 24))
            title_label.pack(pady=10)

            # Search Bar Frame
            self.search_frame = tk.Frame(self.main_frame)
            self.search_frame.pack(pady=10)

            search_label = tk.Label(self.search_frame, text="Search:")
            search_label.pack(side=tk.LEFT, padx=5)

            self.search_entry = tk.Entry(self.search_frame, width=40)
            self.search_entry.pack(side=tk.LEFT, padx=5)

            # Search Button
            search_button = tk.Button(self.search_frame, text="Search", command=self.search_show)
            search_button.pack(side=tk.LEFT, padx=5)

            # Clear Button
            clear_button = tk.Button(self.search_frame, text="Clear", command=self.clear_search)
            clear_button.pack(side=tk.LEFT, padx=5)

            # Scrollable Frame Setup
            self.results_canvas = tk.Canvas(self.main_frame)
            self.results_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.results_canvas.yview)
            self.results_frame = tk.Frame(self.results_canvas)

            self.results_frame.bind("<Configure>", lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))
            self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
            self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)

            self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.display_recommendations()

    def create_profile_page(self):
        """Creates the profile page layout."""
        title_label = tk.Label(self.profile_page, text="Profile Page", font=("Arial", 24))
        title_label.pack(pady=10)

        # Added the next 6 lines for sorting
        sort_frame = tk.Frame(self.profile_page)
        sort_frame.pack(pady=5)
        tk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)

        self.sort_dropdown = ttk.Combobox(sort_frame, textvariable=self.sort_option, values=["None", "Score (High to Low)", "Movies Only", "TV Shows Only"], state="readonly")
        self.sort_dropdown.pack(side=tk.LEFT, padx=5)
        self.sort_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_profile_tabs())

        self.profile_notebook = ttk.Notebook(self.profile_page)
        self.profile_notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs with scrolling
        self.completed_tab = self.create_scrollable_tab(self.profile_notebook, "Completed")
        self.plan_to_watch_tab = self.create_scrollable_tab(self.profile_notebook, "Plan to Watch")
        self.dropped_tab = self.create_scrollable_tab(self.profile_notebook, "Dropped")

    def create_scrollable_tab(self, notebook, label):
        """Creates a scrollable tab."""
        frame = tk.Frame(notebook)
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        notebook.add(frame, text=label)
        return scrollable_frame
    
    def update_profile_tabs(self):
        tabs = {"Completed": self.completed_tab, "Plan to Watch": self.plan_to_watch_tab, "Dropped": self.dropped_tab}
        sort_option = self.sort_option.get()
        for category, tab in tabs.items():
            for widget in tab.winfo_children():
                widget.destroy()

            query = "SELECT id, title, score, poster_path, type FROM shows WHERE category=?"
            params = (category,)

            if sort_option == "Score (High to Low)":
                query += " ORDER BY score DESC"
            elif sort_option == "Movies Only":
                query += " AND type='movie'"
            elif sort_option == "TV Shows Only":
                query += " AND type='tv'"
            
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            shows = cursor.fetchall()

            for show_id, title, score, poster, show_type in shows:
                frame = tk.Frame(tab, relief=tk.RIDGE, borderwidth=2, padx=5, pady=5)
                frame.pack(fill=tk.X, pady=5)

                tk.Label(frame, text=f"{title} (Score: {score if score else 'N/A'})", font=("Arial", 14)).pack(side=tk.LEFT)
                edit_button = tk.Button(frame, text="Edit", command=lambda s_id=show_id: self.edit_show(s_id))
                edit_button.pack(side=tk.RIGHT)
    # def update_profile_tabs(self):
    #     """Updates the profile page with the latest data."""
    #     tabs = {"Completed": self.completed_tab, "Plan to Watch": self.plan_to_watch_tab, "Dropped": self.dropped_tab}
    #     for category, tab in tabs.items():
    #         for widget in tab.winfo_children():
    #             widget.destroy()

    #         cursor = self.conn.cursor()
    #         cursor.execute("SELECT id, title, score, poster_path FROM shows WHERE category=?", (category,))
    #         shows = cursor.fetchall()

    #         for show_id, title, score, poster in shows:
    #             frame = tk.Frame(tab, relief=tk.RIDGE, borderwidth=2, padx=5, pady=5)
    #             frame.pack(fill=tk.X, pady=5)

    #             tk.Label(frame, text=f"{title} (Score: {score if score else 'N/A'})", font=("Arial", 14)).pack(side=tk.LEFT)
    #             edit_button = tk.Button(frame, text="Edit", command=lambda s_id=show_id: self.edit_show(s_id))
    #             edit_button.pack(side=tk.RIGHT)
    
    def search_show(self):
        """Handles search without removing the search bar."""
        query = self.search_entry.get()

        if not query:
            self.clear_search()
            return

        # Clear previous results but keep the search bar
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Fetch and display results
        url = f"{BASE_URL}/search/multi?api_key={API_KEY}&query={query}"
        response = requests.get(url)

        if response.status_code == 200:
            results = response.json().get('results', [])
            self.display_results(results)
        else:
            messagebox.showerror("API Error", "Failed to fetch results.")                           

    def create_search_bar(self):
        """Creates the search bar UI with a Clear button."""
        self.search_frame = tk.Frame(self.main_page)
        self.search_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.search_entry = tk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(self.search_frame, text="Search", command=self.search_show)
        search_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(self.search_frame, text="Clear", command=self.create_main_page)
        clear_button.pack(side=tk.LEFT, padx=5)

    def clear_search(self):
        """Clears search results and restores recommendations."""
        self.search_entry.delete(0, tk.END)
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.display_recommendations()

    def display_results(self, results):
        """Displays the search results."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not results:
            tk.Label(self.results_frame, text="No results found.").pack(pady=10)
            return

        for result in results:
            title = result.get("title") or result.get("name", "Unknown")
            release_date = result.get("release_date") or result.get("first_air_date", "N/A")
            poster_path = result.get("poster_path", "")

            # Determine the type (movie or TV show)
            if "media_type" in result:
                show_type = "Movie" if result["media_type"] == "movie" else "TV Show"
            else:
                show_type = "Movie" if "title" in result else "TV Show"  # Heuristic check

            result_frame = tk.Frame(self.results_frame, relief=tk.RIDGE, borderwidth=2, padx=5, pady=5)
            result_frame.pack(fill=tk.X, pady=5)

            # Load poster image
            if poster_path:
                image_url = f"{IMAGE_BASE_URL}{poster_path}"
                image_response = requests.get(image_url)
                image_data = Image.open(BytesIO(image_response.content))
                image_data.thumbnail((100, 150))
                poster_image = ImageTk.PhotoImage(image_data)

                poster_label = tk.Label(result_frame, image=poster_image)
                poster_label.image = poster_image  # Keep a reference to prevent garbage collection
                poster_label.pack(side=tk.LEFT, padx=10)

            info_frame = tk.Frame(result_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            tk.Label(info_frame, text=f"Title: {title}", font=("Arial", 14)).pack(anchor=tk.W)
            tk.Label(info_frame, text=f"Release Date: {release_date}").pack(anchor=tk.W)

            button_frame = tk.Frame(info_frame)
            button_frame.pack(anchor=tk.E)

            tk.Button(button_frame, text="Add to Completed", command=lambda t=title, p=poster_path, st=show_type: self.add_to_db(t, "Completed", p, st)).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Add to Plan to Watch", command=lambda t=title, p=poster_path, st=show_type: self.add_to_db(t, "Plan to Watch", p, st)).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Add to Dropped", command=lambda t=title, p=poster_path, st=show_type: self.add_to_db(t, "Dropped", p, st)).pack(side=tk.LEFT, padx=5)

    def display_recommendations(self):
        """Displays recommended shows when there is no search query."""
        self.recommendations_frame = recommendations.display_recommended_shows(self.results_frame, self.add_to_db)

    def add_to_db(self, title, category, poster_path, show_type):
        """Adds a title to the database."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO shows (title, category, poster_path, type) VALUES (?, ?, ?, ?)", (title, category, poster_path, show_type))
        self.conn.commit()
        messagebox.showinfo("Success", f"Added '{title}' to {category}.")
        self.update_profile_tabs()

    def edit_show(self, show_id):
        """Opens an edit dialog for a show."""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Show")

        # Fetch show details
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, category, score FROM shows WHERE id=?", (show_id,))
        show = cursor.fetchone()
        if not show:
            messagebox.showerror("Error", "Show not found!")
            edit_window.destroy()
            return

        title, category, score = show

        tk.Label(edit_window, text=f"Editing: {title}", font=("Arial", 14)).pack(pady=10)

        # Score editing
        tk.Label(edit_window, text="Score:").pack(pady=5)
        score_var = tk.StringVar(value=score if score is not None else "")
        score_entry = tk.Entry(edit_window, textvariable=score_var)
        score_entry.pack(pady=5)

        # Category dropdown
        tk.Label(edit_window, text="Category:").pack(pady=5)
        category_var = tk.StringVar(value=category)
        category_dropdown = ttk.Combobox(
            edit_window, textvariable=category_var, values=["Completed", "Plan to Watch", "Dropped"]
        )
        category_dropdown.pack(pady=5)

        # Delete Button
        delete_button = tk.Button(edit_window, text="Delete Show", fg="red",
                                command=lambda: self.delete_show(show_id, edit_window))
        delete_button.pack(pady=10)

        # Save Changes Button
        def save_changes():
            new_score = score_var.get()
            new_category = category_var.get()

            # Update database
            cursor.execute("""
                UPDATE shows
                SET score = ?, category = ?
                WHERE id = ?
            """, (new_score, new_category, show_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Show updated successfully!")
            self.update_profile_tabs()
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)

    def delete_show(self, show_id, edit_window):
        """Deletes a show from the database."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM shows WHERE id=?", (show_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Show deleted successfully!")
        self.update_profile_tabs()
        edit_window.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ShowTrackerApp(root)
    root.mainloop()
