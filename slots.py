import random

def slots():

    row1 = []
    row2 = []
    row3 = []
    grid = [row1, row2, row3]

    for row in grid:
        for x in range(3):
            row.append(random.randint(1, 3))

    for row in grid:
        for y in range(len(row)):
            if row[y] == 1:
                row[y] = "X"
            if row[y] == 2:
                row[y] = "O"
            if row[y] == 3:
                row[y] = "+"

    money = 0

    if row1[0] == row2[0] and row2[0] == row3[0]:
        money += 50
    if row1[1] == row2[1] and row2[1] == row3[1]:
        money += 50
    if row1[2] == row2[2] and row2[2] == row3[2]:
        money += 50
    
    if row1[0] == row1[1] and row1[1] == row1[2]:
        money += 50
    if row2[0] == row2[1] and row2[1] == row2[2]:
        money += 50
    if row3[0] == row3[1] and row3[1] == row3[2]:
        money += 50
    
    if row1[0] == row2[1] and row2[1] == row3[2]:
        money += 50
    if row3[0] == row2[1] and row2[1] == row1[2]:
        money += 50

    for row in grid:
        print(row)

    print(f"{money} won!")
