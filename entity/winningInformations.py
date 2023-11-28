
class WinningInformations:
    pointWin : int
    pointDraw : int
    pointLoose : int
    isDraw : int
    colName : str
   

def winningInformationsInit(
        winningInformations : WinningInformations,
        colName : str,
        pointDraw: int,
        pointWin : int,
        pointLoose : int,
        isDraw : bool
    )->None:
    """
        Initialise les informations de gain.

        Args:
            winningInformations (WinningInformations): L'objet WinningInformations à initialiser.
            colName (str): Le nom de la colonne associée aux informations de gain.
            pointDraw (int): Le nombre de points attribués en cas d'égalité.
            pointWin (int): Le nombre de points attribués en cas de victoire.
            pointLoose (int): Le nombre de points attribués en cas de défaite.
            isDraw (bool): Indique si le jeu peut se terminer par une égalité.

        Returns:
            None
    """
    winningInformations.pointDraw = pointDraw
    winningInformations.colName = colName
    winningInformations.pointWin = pointWin
    winningInformations.pointLoose = pointLoose
    winningInformations.isDraw = isDraw
  




    
   