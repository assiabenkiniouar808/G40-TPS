def entier_vers_romain(num):
    valeurs = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'),
        (1, 'I')
    ]

    resultat = ""

    for val, symbole in valeurs:
        while num >= val:
            resultat += symbole
            num -= val

    return resultat


# Test
print(entier_vers_romain(1994))  