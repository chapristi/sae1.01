from entity.player import * 
from sqlite3 import Connection
from entity.winningInformations import WinningInformations
from helpers.colors import *
from dataServices.sqlCommands import *
from helpers.helperPlayer import getOtherPlayer

def pointsDistribution( winningInformations : WinningInformations,currentPlayers : CurrentPlayers,
    currentPlayer : Player ,conn : Connection)->None:

    otherPlayer : Player

    otherPlayer = getOtherPlayer(currentPlayers,currentPlayer)
    if  not winningInformations.isDraw:
        print(setColorGreen("🙂 Bravo c'est " + "(" + currentPlayer.name +")"+ " qui l'emporte vous gagnez +" + str(winningInformations.pointWin) + " points"))
        addPoint(currentPlayer.id,winningInformations.pointWin,conn,winningInformations.colName)
        print(setColorGreen("🙃 Merci " + "(" + otherPlayer.name +")"+ "d'avoir paricipé vous gagnez +" + str(winningInformations.pointLoose) + " points"))
        addPoint(otherPlayer.id,winningInformations.pointLoose,conn,winningInformations.colName)
    else:
        print(setColorGreen("🙃 Bravo une egalité parfaite "+ currentPlayers.player1.name + " et "+ currentPlayers.player2.name + "vous remportez " + str(winningInformations.pointDraw) + " points"))
        addPoint(currentPlayers.player1.id,winningInformations.pointDraw,conn,winningInformations.colName)
        addPoint(currentPlayers.player2.id,winningInformations.pointDraw,conn,winningInformations.colName)
