
class WinningInformations:
    pointWin : int
    pointDraw : int
    pointLoose : int
    isDraw : int
    colName : str
   

def winningInformationsInit(winningInformations : WinningInformations, colName : str, pointDraw: int, pointWin : int, pointLoose : int,isDraw : bool)->None:
    winningInformations.pointDraw = pointDraw
    winningInformations.colName = colName
    winningInformations.pointWin = pointWin
    winningInformations.pointLoose = pointLoose
    winningInformations.isDraw = isDraw
  




    
   