# contains class for flashcards with question and answers

class Card:
    def __init__(self, question: str, answer: str):
        self.question, self.answer = question, answer
