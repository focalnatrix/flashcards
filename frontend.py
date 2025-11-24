import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import backend

class FlashcardApp:
    def __init__(self):
        self.decks = []
        self.current_deck = None
        self.deck_rows_frame = None

        self.main_window = tk.Tk()
        self.main_window.withdraw()
        self.main_window.title("Flashcards")
        self.center_window(self.main_window, 700, 500)
        self.main_window.deiconify()
    
        self.main_menu()
        self.main_window.mainloop()

    def main_menu(self):
        self.main_frame = ttk.Frame(self.main_window, padding="50")
        self.main_frame.pack(fill="both", expand=True)

        # Text here should be some welcoming text or whatever
        ttk.Label(self.main_frame, text="Welcome to our app!!!!!", 
                  font=("Arial", 16, "bold")).pack(padx=10, pady=10)

        self.decks_container = ttk.Frame(self.main_frame)
        self.decks_container.pack(fill="both", expand=True)

        self.show_decks(self.decks_container)

        ttk.Button(self.main_frame, text="Create New Deck", 
                   command=self.create_deck_menu).pack(pady=2)
        ttk.Button(self.main_frame, text="Add New Card", 
                   command=self.create_card_menu).pack(pady=2)

    def create_deck_menu(self):
        self.create_deck_window = tk.Toplevel(self.main_window)
        self.create_deck_window.withdraw()
        self.create_deck_window.title("Create Deck")
        self.center_window(self.create_deck_window, 600, 400)
        self.create_deck_window.deiconify()
        
        main_frame = ttk.Frame(self.create_deck_window, padding="50")
        main_frame.pack(anchor="center", expand=True)

        main_frame.columnconfigure(0, weight=1)

        '''
        Allows user to input deck name
        '''
        ttk.Label(main_frame, text="Deck Name", font=("Arial", 14, "bold")).grid(
            row=0, column=0, sticky=tk.W ,padx=(0,5), pady=(0,5))

        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=0, sticky=tk.W, pady=(0,15))
        self.name_entry.focus_set()

        '''
        Allows user to choose review speed
        '''
        ttk.Label(main_frame, text="Review Speed", font=("Arial", 14, "bold")).grid(
            row=2, column=0, padx=(0,20), pady=(0,5), sticky=(tk.W))
        
        review_speed_frame = ttk.Frame(main_frame)
        review_speed_frame.grid(row=3, column=0, sticky=tk.W, pady=(0,20))

        self.speed_entry = tk.StringVar(value="Slow")

        ttk.Radiobutton(review_speed_frame, text="Slow", variable=self.speed_entry, value="Slow").grid(
            row=2, column=0, sticky=tk.W, padx=(0,20))
        ttk.Label(review_speed_frame, text="Review cards less frequently").grid(
            row=2, column=1, sticky=tk.W)
        
        ttk.Radiobutton(review_speed_frame, text="Fast", variable=self.speed_entry, value="Fast").grid(
            row=3, column=0, sticky=tk.W)
        ttk.Label(review_speed_frame, text="Review cards more frequently").grid(
            row=3, column=1, sticky=tk.W)

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
                ttk.Label(self.deck_rows_frame, text="Deck Name", font=("Arial", 13, "bold")).grid(
                    row=0, column=0, padx=5, pady=3, sticky="w")
                ttk.Label(self.deck_rows_frame, text="Speed", font=("Arial", 13, "bold")).grid(
                    row=0, column=1, padx=5, pady=3)
                ttk.Label(self.deck_rows_frame, text="Actions", font=("Arial", 13, "bold")).grid(
                    row=0, column=2, padx=5, pady=3)
            
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
        ttk.Button(button_frame, text="Delete", command=lambda d=deck: self.delete_deck(d)).pack(
            side="left", padx=2)

    
    def create_card_menu(self):
        if not self.decks:
            messagebox.showerror("Error", "You need to create a deck before adding cards!")
            return
        
        '''
        General window setup
        '''
        self.create_card_window = tk.Toplevel(self.main_window)
        self.create_card_window.withdraw()
        self.create_card_window.title("Create Card")
        self.center_window(self.create_card_window, 600, 400)
        self.create_card_window.deiconify()

        main_frame = ttk.Frame(self.create_card_window, padding="20")
        main_frame.pack(anchor="center", expand=True)

        '''
        Allows user to pick a deck to add the card to
        '''
        option_frame = ttk.Frame(main_frame)
        option_frame.grid(row=0, column=0, sticky="w", pady=(0,15))

        options = [deck.name for deck in self.decks]
        self.deck_entry = tk.StringVar()
        self.deck_entry.set(options[0])

        ttk.Label(option_frame, text="Select Deck", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=(0,10), sticky="w")
        deck_menu = ttk.OptionMenu(option_frame, self.deck_entry, options[0], *options)
        deck_menu.grid(row=0, column=1, padx=(0,10))

        '''
        Allows user to customize front and back parts of card
        '''
        ttk.Label(main_frame, text="Front", font=("Arial", 14, "bold")).grid(
            row=1, column=0, sticky="w", padx=(0,5), pady=(0,5))

        self.front_entry = tk.Text(main_frame, height=5, width=50)
        self.front_entry.grid(row=2, column=0, pady=(0,15))
        self.front_entry.focus_set()

        ttk.Label(main_frame, text="Back", font=("Arial", 14, "bold")).grid(
            row=3, column=0, sticky="w", padx=(0,5), pady=(0,5))

        self.back_entry = tk.Text(main_frame, height=5, width=50)
        self.back_entry.grid(row=4, column=0, pady=(0,15))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0)

        ttk.Button(button_frame, text="Create Card", command=self.create_card).grid(row=0, column=0)


    def create_card(self):
        '''
        i have class ill finish this later
        '''
        front = self.front_entry.get()
        back = self.back_entry.get()
        selected_deck = self.deck_entry.get()

        if not front or back:
            messagebox.showerror("Error", "Both front and back parts must be filled!")
            return
        
        this_deck = next((d for d in self.decks if d.name == selected_deck), None)
        
        try:
            new_card = backend.Flashcard(front, back)
            selected_deck.add_card(new_card)

            self.create_card_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create card: {str(e)}")

    def study_deck(self, deck):
        # TODO
        pass

    def edit_deck(self, deck):
        # TODO
        '''
        Two sections
        1. Edit deck details (name, speed)
        2. View/Add/Edit/Delete cards in the deck
        '''
        pass

    def delete_deck(self, deck):
        # TODO
        pass  

    def center_window(self, window, width=None, height=None):
        window.update_idletasks()
        w = width if width else window.winfo_width()
        h = height if height else window.winfo_height()
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        window.geometry(f'{w}x{h}+{x}+{y}')

FlashcardApp()