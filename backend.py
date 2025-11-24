from datetime import datetime

'''
not sure which function to implement search/sort algo in
'''

class Flashcard:
    def __init__(self, front: str, back: str, id=None):
        self.front = front
        self.back = back
        self.rating = 0

        self.last_review = None
        self.next_review = datetime.now()

        self.date_created = datetime.now()

    def rate(self, rating: int):
        self.rating = rating

class Deck:
    def __init__(self, name: str, speed):
        self.name = name
        self.speed = speed
        self.date_created = datetime.now()
        self.date_reviewed = None

        self.cards = []
        self.due_cards = []

        self.cards_today = 0
        self.score = 0

    def add_card(self, front: str, back: str):
        card = Flashcard(front, back)
        self.cards.append(card)

    def schedule_card(self, card: Flashcard):
        # TODO

        match card.rating:
            case "0":
                pass
            case "1":
                pass
            case "2":
                pass
            case _:
                pass
        pass

    def get_next_card(self):
        # TODO
        pass
