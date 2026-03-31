n = int(input("Entrez un entier : "))

binaire = bin(n)[2:]
nb_bits_1 = binaire.count('1')

print("Binaire :", binaire)
print("Nombre de bits à 1 :", nb_bits_1)