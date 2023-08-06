import tictacpy

class Emojis:
    def __init__(self, x, o, b):
        self.x = x
        self.o = o
        self.b = b

class TTT:
    def __init__(self, xPlayer, oPlayer, x:str = "❌", o:str = "⭕", b:str = "ㅤ"):
        if xPlayer == oPlayer:
            raise tictacpy.CannotBeTheSame("The players for x and o cannot be the same!")
        self.board = tictacpy.Board(x, o, b)
        self.emojis = Emojis(x, o, b)
        self.xPlayer = xPlayer
        self.oPlayer = oPlayer
        self.turnPlayer = xPlayer
    
    def turn(self, space:str, player:str):
        if space.lower() not in ("a1", "b1", "c1", "a2", "b2", "c2", "a3", "b3", "c3"):
            raise tictacpy.InvalidSquare(F"Square {space} is not on the board!")
        else:
            if player.lower() not in ("x", "o"):
                raise tictacpy.InvalidPlayer("The player must be an \"x\" or an \"o\"")
            elif player == "x":
                turnplayer = self.xPlayer
            elif player == "o":
                turnplayer = self.oPlayer
            
            if turnplayer != self.turnPlayer:
                raise tictacpy.NotTheirTurn("It is not that player's turn!")
            
            square = self.board.decode(space)
            if square is None:
                raise tictacpy.UnknownError("An unknown error has occured!")
            else:
                if square != self.emojis.b:
                    return False
                else:
                    if turnplayer == self.xPlayer:
                        self.turnPlayer = self.oPlayer
                    else:
                        self.turnPlayer = self.xPlayer
                    return self.board.change(space, player, self.emojis.x, self.emojis.o)
    
    def is_over(self):
        if self.board.A1 == self.board.A2 and self.board.A2 == self.board.A3 and self.board.A1 == self.emojis.x:
            return "X"
        elif self.board.A1 == self.board.A2 and self.board.A2 == self.board.A3 and self.board.A1 == self.emojis.o:
            return "O"
        elif self.board.B1 == self.board.B2 and self.board.B2 == self.board.B3 and self.board.B1 == self.emojis.x:
            return "X"
        elif self.board.B1 == self.board.B2 and self.board.B2 == self.board.B3 and self.board.B1 == self.emojis.o:
            return "O"
        elif self.board.C1 == self.board.C2 and self.board.C2 == self.board.C3 and self.board.C1 == self.emojis.x:
            return "X"
        elif self.board.C1 == self.board.C2 and self.board.C2 == self.board.C3 and self.board.C1 == self.emojis.o:
            return "O"
        
        elif self.board.A1 == self.board.B1 and self.board.B1 == self.board.C1 and self.board.A1 == self.emojis.x:
            return "X"
        elif self.board.A1 == self.board.B1 and self.board.B1 == self.board.C1 and self.board.A1 == self.emojis.o:
            return "O"
        elif self.board.A2 == self.board.B2 and self.board.B2 == self.board.C2 and self.board.A2 == self.emojis.x:
            return "X"
        elif self.board.A2 == self.board.B2 and self.board.B2 == self.board.C2 and self.board.A2 == self.emojis.o:
            return "O"
        elif self.board.A3 == self.board.B3 and self.board.B3 == self.board.C3 and self.board.A3 == self.emojis.x:
            return "X"
        elif self.board.A3 == self.board.B3 and self.board.B3 == self.board.C3 and self.board.A3 == self.emojis.o:
            return "O"
        
        elif self.board.A1 == self.board.B2 and self.board.B2 == self.board.C3 and self.board.A1 == self.emojis.x:
            return "X"
        elif self.board.A1 == self.board.B2 and self.board.B2 == self.board.C3 and self.board.A1 == self.emojis.o:
            return "O"
        elif self.board.A3 == self.board.B2 and self.board.B2 == self.board.C1 and self.board.A3 == self.emojis.x:
            return "X"
        elif self.board.A3 == self.board.B2 and self.board.B2 == self.board.C1 and self.board.A3 == self.emojis.o:
            return "O"
        
        elif self.board.A1 != self.emojis.b and self.board.A2 != self.emojis.b and self.board.A3 != self.emojis.b and self.board.B1 != self.emojis.b and self.board.B2 != self.emojis.b and self.board.B3 != self.emojis.b and self.board.C1 != self.emojis.b and self.board.C2 != self.emojis.b and self.board.C3 != self.emojis.b:
            return None
        
        else:
            return False
    
    def visualize(self):
        return "\n".join([
            F"{self.board.A1}|{self.board.A2}|{self.board.A3}",
            F"{self.board.B1}|{self.board.B2}|{self.board.B3}",
            F"{self.board.C1}|{self.board.C2}|{self.board.C3}"
        ])