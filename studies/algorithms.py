def bubbleSort(liste):
    b = 0
    for i in range(len(liste)-1,0,-1):
         for a in range(i):
             print(liste)
             b += 1
             print(b)
             if liste[a] > liste[a + 1]:
                liste[a], liste[a + 1] = liste[a + 1], liste[a]



liste = [10,9,8,7,6,5,4,3,2,1]

bubbleSort(liste)
print(liste)