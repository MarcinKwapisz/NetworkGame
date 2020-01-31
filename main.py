cards = [["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],["Guard",1],
         ["Priest",2],["Priest",2],["Priest",2],["Baron",3],["Baron",3],["Baron",3],["Baron",3],["Baron",3],["Handmaiden",4],
         ["Handmaiden",4],["Prince",5],["Prince",5],["King",6],["Countess",7],["Princess",8]]

import random
print(len(cards))
l = random.choice(cards)
print(l)
cards.remove(l)
print(len(cards))
