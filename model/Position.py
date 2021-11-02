from model.types import Directoin
class Position:
    def __init__(self, direction : Directoin , size : int, entry_price : int , leverage: int) :
        self.direction = direction 
        self.size = size 
        self.entry_price = entry_price  
        self.leverage = leverage 
    
    def pnl_calc(self, price : int):
        if Directoin != Directoin.NONE:
            self.pnl = self.size*(price - self.entry_price)*self.leverage*int(self.direction)
        else : 
            self.pnl = 0  
        return self.pnl 

    def __str__(self):
        return f'direction:{self.direction},size:{self.size},entry_price:{self.entry_price},leverage:{self.leverage},pnl:{self.pnl}'

    

        