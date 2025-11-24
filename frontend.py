import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import backend

class FlashcardApp:
    def __init__(self):
        self.decks = []
        self.current_deck = None
        self.start_app()

    def start_app(self):
        # TODO
        
        self.main_window = tk.Tk()
        self.main_window.title("Flashcards")

        # Text here should be some welcoming text or whatever
        tk.Label(self.main_window, text="Welcome to our app!!!!!").pack(padx=10, pady=10)

        tk.Button(self.main_window, text="Create Deck", command=self.create_menu).pack(pady=10)
        # Button for create_card
        # Button for view_all_decks
        # Button for study_deck
        
        self.main_window.mainloop()

    def create_menu(self):
        self.create_deck_window = tk.Toplevel(self.main_window)
        self.create_deck_window.title("Create Deck")

        tk.Label(self.create_deck_window, text="Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.create_deck_window)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.create_deck_window, text="Description").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.create_deck_window)
        self.description_entry.grid(row=1, column=1)

        create_deck_button = tk.Button(self.create_deck_window, text="Create This Deck", command=self.check_deck)
        create_deck_button.grid(row=2, column=0)
        
    def create_deck(self):
        deck_name = self.name_entry.get().strip()
        deck_description = self.description_entry.get().strip()

        if not deck_name or not deck_description:
            messagebox.showerror("Error", "A deck requires a name and description!")
            return
        
        '''
        cian this part doesnt work plz help me fix
        it should import from backend but it doesnt work for 
        soem reason plzsplspls
        '''
        backend.Deck(deck_name, deck_description)
        
        messagebox.showinfo("Info", "Deck created successfully!")
        self.create_deck_window.destroy()
        
    def create_card(self):
        # TODO

        if not self.decks:
            messagebox.showerror("Error", "A deck is needed to create cards!")
        
        self.create_card_window = tk.Tk()

    def view_all_decks(self):
        # TODO
        
        if not self.decks:
            messagebox.showerror("Error", "You have no decks! Please create a deck.")
            return
        pass

    def study_deck(self):
        # TODO
        pass

FlashcardApp()