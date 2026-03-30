def romain_vers_entier(s):
    valeurs = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    total = 0

    for i in range(len(s)):
        if i < len(s) - 1 and valeurs[s[i]] < valeurs[s[i + 1]]:
            total -= valeurs[s[i]]
        else:
            total += valeurs[s[i]]

    return total


# Tests
print(romain_vers_entier("III"))       
print(romain_vers_entier("MCMXCIV"))  