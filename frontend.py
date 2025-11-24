import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import backend

class FlashcardApp:
    def __init__(self):
        self.decks = []
        self.current_deck = None
        self.deck_rows_frame = None

        self.main_window = tk.Tk()
        self.main_window.title("Flashcards")
        self.main_window.geometry("600x400")

        self.main_menu()
        self.main_window.mainloop()

    def main_menu(self):
        self.main_frame = ttk.Frame(self.main_window, padding="50")
        self.main_frame.pack(fill="both", expand=True)

        # Text here should be some welcoming text or whatever
        ttk.Label(self.main_frame, text="Welcome to our app!!!!!", font=("Arial", 16, "bold")).pack(padx=10, pady=10)

        self.decks_container = ttk.Frame(self.main_frame)
        self.decks_container.pack(fill="both", expand=True)

        self.show_decks(self.decks_container)

        ttk.Button(self.main_frame, text="Create New Deck", command=self.create_menu).pack(pady=2)

    def create_menu(self):
        self.create_deck_window = tk.Toplevel(self.main_window)
        self.create_deck_window.title("Create Deck")
        
        main_frame = ttk.Frame(self.create_deck_window, padding="50")
        main_frame.pack(fill="both", expand=True)

        main_frame.columnconfigure(0, weight=1)

        '''
        Allows user to input deck name
        '''
        ttk.Label(main_frame, text="Deck Name", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky=tk.W ,padx=(0,5), pady=(0,5))

        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=0, sticky=tk.W, pady=(0,15))
        self.name_entry.focus_set()

        '''
        Allows user to choose review speed
        '''
        
        review_speed_frame = ttk.Frame(main_frame)
        review_speed_frame.grid(row=3, column=0, sticky=tk.W, pady=(0,20))

        ttk.Label(review_speed_frame, text="Review Speed", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=(0,20), pady=(0,5), sticky=(tk.W))

        self.speed_entry = tk.StringVar(value="Slow")
        ttk.Radiobutton(review_speed_frame, text="Slow", variable=self.speed_entry, 
                        value="Slow").grid(row=2, column=1, sticky=tk.W, padx=(0,20))
        ttk.Radiobutton(review_speed_frame, text="Fast", variable=self.speed_entry, 
                        value="Fast").grid(row=2, column=2, sticky=tk.W)

        '''
        Create and cancel buttons
        '''
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2)

        ttk.Button(button_frame, text="Create This Deck", command=self.create_deck).grid(row=0, column=0)     

    def create_deck(self):
        deck_name = self.name_entry.get()
        deck_speed = self.speed_entry.get()

        if not deck_name:
            messagebox.showerror("Error", "A deck needs a name!")
            return
        
        try:
            new_deck = backend.Deck(deck_name, deck_speed)
            self.decks.append(new_deck)

            self.create_deck_window.destroy()

            if self.no_decks_label:
                self.no_decks_label.destroy()
                self.no_decks_label = None

            if len(self.decks) >= 1:
                ttk.Label(self.deck_rows_frame, text="Deck Name", font=("Arial", 11, "bold")).grid(
                    row=0, column=0, padx=5, pady=3, sticky="w")
                ttk.Label(self.deck_rows_frame, text="Speed", font=("Arial", 11, "bold")).grid(
                    row=0, column=1, padx=5, pady=3, sticky="w")
            
            row_index = len(self.decks)
            self._add_deck_to_table(new_deck, row_index)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create deck: {str(e)}") 

    def show_decks(self, parent_frame):

        wrapper = ttk.Frame(parent_frame)
        wrapper.pack(pady=10)
        wrapper.pack(anchor="center")

        self.deck_rows_frame = ttk.Frame(wrapper)
        self.deck_rows_frame.pack(anchor="w")

        self.no_decks_label = None

        if not self.decks:
            self.no_decks_label = ttk.Label(
                self.deck_rows_frame, 
                text="No decks available. Create a new deck to get started!", 
                foreground="gray", anchor="center"
                )
            self.no_decks_label.grid(row=1, column=0, columnspan=3, pady=10)
            return
                
        for i, deck in enumerate(self.decks):
            self._add_deck_to_table(deck, i + 1)

    
    def _add_deck_to_table(self, deck, row_index):
        ttk.Label(self.deck_rows_frame, text=deck.name).grid(
                row=row_index, column=0, padx=5, pady=2, sticky="w")
        
        ttk.Label(self.deck_rows_frame, text=str(deck.speed)).grid(
                row=row_index, column=1, padx=5, pady=2)

        button_frame = ttk.Frame(self.deck_rows_frame)
        button_frame.grid(row=row_index, column=2, padx=10, pady=2)
        
        ttk.Button(button_frame, text="Study", command=lambda d=deck: self.study_deck(d)).pack(
            side="left", padx=2)
        ttk.Button(button_frame, text="Edit", command=lambda d=deck: self.edit_deck(d)).pack(
            side="left", padx=2)
        

    def create_card(self):
        self.create_card_window = tk.Toplevel(self.main_window)

    def edit_deck(self, deck):
        # TODO
        pass

    def study_deck(self, deck):
        # TODO
        pass

FlashcardApp()