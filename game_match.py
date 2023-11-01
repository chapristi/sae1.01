class GameMatch:
    colName : str
    pointWin : int
    pointLoose : int
    numberOfMatches : int
    isOver : bool

def gameMatchInit(gameMatch : GameMatch)->None:
   """
        Cette procedure permet d'initailiser l'objet de type GameMatch

        Args : 
            gameMatch (GameMatch): variable de type GameMatch.
        Returns:
            Rien
   """
   gameMatch.colName = "scoreMatches"
   gameMatch.numberOfMatches = 20
   gameMatch.pointWin = 15
   gameMatch.pointLoose = 2
   gameMatch.isOver = False