def isDigit(input : str) -> bool:
    """
        Vérifie si la chaîne de caractères donnée ne contient que des chiffres.

        Args:
            input_str (str): La chaîne de caractères à vérifier.

        Returns:
            bool: True si la chaîne ne contient que des chiffres, False sinon.
    """
    numbers : str
    isDigit : bool
    i : int

    if input == "":
        return False
    numbers = "0123456789"
    isDigit = True
    i  = 0 
    while i < len(input) and isDigit:
        if input[i] not in numbers: isDigit = False
        i = i+1
    return isDigit



