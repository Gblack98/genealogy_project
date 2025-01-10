reponse='oui'
while reponse=='oui':
    n=int(input("Combien de nombre voulez vous entrer : "))
    for i in range(n):
        m=int(input('entrez le nombre : '))
        if m%2==0:
            print("Paire")
        else:
            print("Impair")    
    reponse=input("Voulez-vous continuer : ")        