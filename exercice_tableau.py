def produit_sans_soi(nums):
    n = len(nums)
    
    gauche = [1] * n
    droite = [1] * n
    resultat = [1] * n

    
    for i in range(1, n):
        gauche[i] = gauche[i-1] * nums[i-1]

    
    for i in range(n-2, -1, -1):
        droite[i] = droite[i+1] * nums[i+1]

    
    for i in range(n):
        resultat[i] = gauche[i] * droite[i]

    return resultat
print(produit_sans_soi([1,2,3,4,5]))


print(produit_sans_soi([3,2,1]))


def test():
    assert produit_sans_soi([1,2,3,4,5]) == [120,60,40,30,24]
    assert produit_sans_soi([3,2,1]) == [2,3,6]
    assert produit_sans_soi([1,1,1]) == [1,1,1]
    print("Tous les tests sont OK ")

if __name__ == "__main__":
    test()