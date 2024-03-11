class card:
    def __init__(self,suit, value):
        self.suit = suit
        self.value = value
    
    def __repr__(self):
        return  " of ".join(self.value,self.suit)