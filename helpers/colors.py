def setColorRed(text : str) -> str:
    """
        Applique la couleur rouge à un texte donné en utilisant des codes ANSI.

        Args:
            text (str): Le texte auquel appliquer la couleur rouge.

        Returns:
            str: Le texte avec la couleur rouge appliquée, prêt à être affiché dans un terminal.

    """
    return "\u001b[31m" + text + "\u001b[0m"

def setColorBlue(text: str) -> str:
    """
    Applique la couleur bleue à un texte donné en utilisant des codes ANSI.

    Args:
        text (str): Le texte auquel appliquer la couleur bleue.

    Returns:
        str: Le texte avec la couleur bleue appliquée, prêt à être affiché dans un terminal.
    """
    return "\u001b[34m" + text + "\u001b[0m"

def setColorGreen(text : str) -> str:
    """
        Applique la couleur verte à un texte donné en utilisant des codes ANSI.

        Args:
            text (str): Le texte auquel appliquer la couleur verte.

        Returns:
            str: Le texte avec la couleur verte appliquée, prêt à être affiché dans un terminal.

    """
    return "\u001b[32m" + text + "\u001b[0m"

def setColorYellow(text : str)->str:
    """
        Applique la couleur jaune à un texte donné en utilisant des codes ANSI.

        Args:
            text (str): Le texte auquel appliquer la couleur jaune.

        Returns:
            str: Le texte avec la couleur jaune appliquée, prêt à être affiché dans un terminal.
    """
    return "\u001b[33m" + text + "\u001b[0m"


