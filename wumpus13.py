import random

symbols = ['_','W','B','P','*']

def print_lair():
    print ("The lair looked like:")
    for y in range(lair_height-1,-1,-1):
        lair_row = '';
        for x in lair:
            lair_row += symbols[x[y]] + ' '
        print(lair_row[:-1])

def place_items(key, num_items):
    random.seed()
    if num_items > 0:
        placed_items = 0;   
        while placed_items < num_items:
            x = random.randint(0, lair_width - 1)
            y = random.randint(0, lair_height - 1)
            if lair[x][y] == 0:
                lair[x][y] = key
                placed_items += 1
        return x,y # return the position of the last item placed

def sense_nearby():
    wumpus = False
    bats = False
    pit = False
    
    def update_senses(item):
        if item == 1:
            nonlocal wumpus
            wumpus = True
        if item == 2:
            nonlocal bats
            bats = True
        if item == 3:
            nonlocal pit
            pit = True
            
    # North
    if player_y < lair_height - 1:
        item = lair[player_x][player_y + 1]
        update_senses(item)
    # South
    if player_y > 0:
        item = lair[player_x][player_y - 1]
        update_senses(item)
    # East
    if player_x < lair_width - 1:
        item = lair[player_x + 1][player_y]
        update_senses(item)
    # West 
    if player_x > 0:
        item = lair[player_x - 1][player_y]
        update_senses(item)
        
    if wumpus:
        print("You smell a wumpus!")
    if bats:
        print("You hear bats!")
    if pit:
        print("You feel a draft!")
    
def lose():
    print ("You lost!")
    print_lair()
    global game_over
    game_over = True
    
def shoot(direction):
    print ("Shooting arrow...")
    global arrows
    arrows -= 1
    target_x = player_x
    target_y = player_y
    if direction == 'N':
        target_y += 1
    if direction == 'S':
        target_y -= 1
    if direction == 'E':
        target_x += 1
    if direction == 'W':
        target_x -= 1
    if lair[target_x][target_y] == 1:
        print ("You killed a wumpus!")
        lair[target_x][target_y] = 0
        global wumpuses_left
        wumpuses_left -= 1
        print(f'There are {wumpuses_left} wumpuses left.')
    else:
        print ("You missed!")
        lose()

quit = False
first_time = True

while not quit:
    if first_time:
        same_settings = False
    else:
        same_settings = input('Same settings? ')[0].lower() != 'n'
    if not same_settings:
        lair_size = input('How big is the lair?(x,y) ').split(',')
        lair_width = int(lair_size[0])
        lair_height = int(lair_size[1])
        num_wumpuses = int(input('How many wumpuses? '))
        if num_wumpuses < 1:
            print('There must be at least one wumpus')
            continue
        num_bats = int(input('How many bats? '))
        num_pits = int(input('How many pits? '))
        if num_pits + num_bats + num_wumpuses >= lair_width * lair_height:
            print('Too many items to fit in the lair')
            continue
    
    # Make empty lair
    lair = [[0]*lair_height for i in range(lair_width)]
    
    # wumpus key = 1
    place_items(1,num_wumpuses)
    # bats key = 2
    place_items(2,num_bats)
    # pits key = 3
    place_items(3,num_pits)
    # player key = 4
    player_x, player_y = place_items(4,1)
    
    arrows = num_wumpuses
    wumpuses_left = num_wumpuses
    game_over = False
    
    while not game_over:
        if wumpuses_left == 0:
            print ("You won!")
            print_lair()
            game_over = True
        item = lair[player_x][player_y]
        if item == 1:
            print("A wumpus ate you!")
            lose()
        if item == 2:
            print("Bats carry you to a new room!")
            lair[player_x][player_y] = 0
            player_x = random.randint(0, lair_width - 1)
            player_y = random.randint(0, lair_height - 1)
            place_items(2,1)
            continue
        if item == 3:
            print("You fell in a bottomless pit!")
            lose()
        if not game_over:
            # Move player marker
            lair[player_x][player_y] = 4
            arrow_string = 'arrow' if arrows == 1 else 'arrows'
            print (f'You have {arrows} {arrow_string}')
            directions = ''
            if player_y < lair_height - 1:
                directions += "N,"
            if player_y > 0:
                directions += "S,"
            if player_x < lair_width -1:
                directions += "E,"
            if player_x > 0:
                directions += "W,"
            direction = 'none'
            while directions.find(direction) == -1 and direction != 'Shoot' and direction != ':':
                print (f'You are in room {player_x + 1},{player_y + 1}')
                sense_nearby()
                print (f'You can go {directions[:-1]} or Shoot(:)')
                direction = input('Which way? ').upper()
            if direction == 'Shoot' or direction == ':':
                shoot(input(f'Shoot which way?({directions[:-1]}) ').upper())
            else:
                lair[player_x][player_y] = 0
                if direction == 'N':
                    player_y += 1
                if direction == 'S':
                    player_y -= 1
                if direction == 'E':
                    player_x += 1
                if direction == 'W':
                    player_x -= 1
    
    quit = input('Play again? ')[0].lower() == 'n'
    first_time = False    