import tictacpy

class Board:
    def __init__(self, x, o, b):
        self.A1 = b
        self.A2 = b
        self.A3 = b
        self.B1 = b
        self.B2 = b
        self.B3 = b
        self.C1 = b
        self.C2 = b
        self.C3 = b
    
    def decode(self, square:str):
        if square.lower() not in ("a1", "b1", "c1", "a2", "b2", "c2", "a3", "b3", "c3"):
            raise tictacpy.InvalidSquare(F"Square {square} is not on the board!")
        elif square.lower() == "a1":
            return self.A1
        elif square.lower() == "a2":
            return self.A2
        elif square.lower() == "a3":
            return self.A3
        elif square.lower() == "b1":
            return self.B1
        elif square.lower() == "b2":
            return self.B2
        elif square.lower() == "b3":
            return self.B3
        elif square.lower() == "c1":
            return self.C1
        elif square.lower() == "c2":
            return self.C2
        elif square.lower() == "c3":
            return self.C3
        else:
            return None
        
    def change(self, square, emoji, x, o):
        if emoji not in ("x", "o"):
            raise tictacpy.InvalidPlayer("Your player must be \"x\" or \"o\"")
        if square.lower() not in ("a1", "b1", "c1", "a2", "b2", "c2", "a3", "b3", "c3"):
            raise tictacpy.InvalidSquare(F"Square {square} is not on the board!")
        elif square.lower() == "a1":
            if emoji == "x":
                self.A1 = x
            elif emoji == "o":
                self.A1 = o
            else:
                return False
            return True
        elif square.lower() == "a2":
            if emoji == "x":
                self.A2 = x
            elif emoji == "o":
                self.A2 = o
            else:
                return False
            return True
        elif square.lower() == "a3":
            if emoji == "x":
                self.A3 = x
            elif emoji == "o":
                self.A3 = o
            else:
                return False
            return True
        elif square.lower() == "b1":
            if emoji == "x":
                self.B1 = x
            elif emoji == "o":
                self.B1 = o
            else:
                return False
            return True
        elif square.lower() == "b2":
            if emoji == "x":
                self.B2 = x
            elif emoji == "o":
                self.B2 = o
            else:
                return False
            return True
        elif square.lower() == "b3":
            if emoji == "x":
                self.B3 = x
            elif emoji == "o":
                self.B3 = o
            else:
                return False
            return True
        elif square.lower() == "c1":
            if emoji == "x":
                self.C1 = x
            elif emoji == "o":
                self.C1 = o
            else:
                return False
            return True
        elif square.lower() == "c2":
            if emoji == "x":
                self.C2 = x
            elif emoji == "o":
                self.C2 = o
            else:
                return False
            return True
        elif square.lower() == "c3":
            if emoji == "x":
                self.C3 = x
            elif emoji == "o":
                self.C3 = o
            else:
                return False
            return True
        else:
            return False