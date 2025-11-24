import json
import uuid
import os

class Flashcard:
    """
    Represents a single flashcard.
    Stores:
      - front/back text
      - SM-2 values (interval, ease_factor, repetitions)
    """

    def __init__(self, front, back, card_id=None, created_at=None):
        self.id = card_id or str(uuid.uuid4()) 
        self.front = front
        self.back = back
        self.repetitions = 0      
        self.interval = 1         
        self.ease_factor = 2.5    
        self.created_at = created_at or uuid.uuid4().int
        self.last_score = 0

    def apply_rating(self, rating):
        self.last_score = rating

        match rating:
            case "0":
                self.repetitions = 0
                self.interval = 1
                self.ease_factor = max(1.3, self.ease_factor - 0.2)
            case "1":
                self.repetitions += 1
                self.interval = max(1, int(self.interval * 1.2))
                self.ease_factor = max(1.3, self.ease_factor - 0.05)
            case "2":
                self.repetitions += 1
                match self.repetitions:
                    case "1":
                        self.interval = 1
                    case "2":
                        self.interval = 3
                    case _:
                        self.interval = int(self.interval * self.ease_factor)
                self.ease_factor = min(2.5, self.ease_factor + 0.1)

class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.score = 0

    def add_card(self, card: Flashcard):
        self.cards.append(card)

    def remove_card(self, card_id):
        card = self.get_card(card_id)
        if card:
            self.cards.remove(card)
            return True
        return False

    def get_card(self, card_id):
        # Binary search 
        low = 0
        high = len(self.cards) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_id = self.cards[mid].id

            if mid_id == card_id:
                return self.cards[mid]
            elif mid_id < card_id:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def sort_by_id(self):
        self.cards = self._quicksort(self.cards, key=lambda c: c.id)

    def sort_by_score(self):
        self.cards.sort(key=lambda c: (c.last_score, c.created_at))

    @staticmethod
    def _quicksort(cards, key):
        if len(cards) <= 1:
            return cards
        pivot = key(cards[len(cards) // 2])
        left = [c for c in cards if key(c) < pivot]
        mid = [c for c in cards if key(c) == pivot]
        right = [c for c in cards if key(c) > pivot]
        return Deck._quicksort(left, key) + mid + Deck._quicksort(right, key)

    def rate_card(self, card: Flashcard, rating):
        card.apply_rating(rating)

        self.score += rating
        self.sort_by_score()

    def max_score(self):
        """
        Returns the highest possible score for this deck,
        assuming all cards were rated 'Easy' (2 points each).
        """
        return len(self.cards) * 2

    # --------------------------------------------------
    # SAVE DECK TO JSON
    # --------------------------------------------------
    def save_to_file(self, filename):
        data = {
            "name": self.name,
            "score": self.score,
            "cards": [self._card_to_dict(c) for c in self.cards]
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # --------------------------------------------------
    # LOAD DECK FROM JSON
    # --------------------------------------------------
    @classmethod
    def load_from_file(cls, filename):
        if not os.path.exists(filename):
            return None
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            deck = cls(data["name"])
            deck.score = data.get("score", 0)
            for card_data in data["cards"]:
                card = Flashcard(
                    front=card_data["front"],
                    back=card_data["back"],
                    card_id=card_data["id"]
                )
                card.repetitions = card_data["repetitions"]
                card.interval = card_data["interval"]
                card.ease_factor = card_data["ease_factor"]
                card.last_score = card_data.get("last_score", 0)
                deck.cards.append(card)
            return deck

    @staticmethod
    def _card_to_dict(card: Flashcard):
        return {
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "repetitions": card.repetitions,
            "interval": card.interval,
            "ease_factor": card.ease_factor,
            "last_score": getattr(card, "last_score", 0)
        }


def create_card(front, back):
    return Flashcard(front, back)