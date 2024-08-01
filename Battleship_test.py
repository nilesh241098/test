class Battleship:
    def __init__(self, team_name, sector_x, sector_y):
        self.team_name = team_name
        self.sector_x = sector_x
        self.sector_y = sector_y

def print_battleship_map(battleships):
    # Determine the size of the grid
    max_x = max(battleship.sector_x for battleship in battleships)
    max_y = max(battleship.sector_y for battleship in battleships)
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
    for battleship in battleships:
        grid[max_y - battleship.sector_y][battleship.sector_x - 1] = battleship.team_name
    for i in range(max_y):
        for j in range(max_x):
            current_team = grid[i][j]
            if current_team != ' ':
                if ((i > 0 and grid[i - 1][j] != ' ' and grid[i - 1][j] != current_team) or
                    (i < max_y - 1 and grid[i + 1][j] != ' ' and grid[i + 1][j] != current_team) or
                    (j > 0 and grid[i][j - 1] != ' ' and grid[i][j - 1] != current_team) or
                    (j < max_x - 1 and grid[i][j + 1] != ' ' and grid[i][j + 1] != current_team)):
                    grid[i][j] = current_team.lower()

    for i in range(max_y):
        print(' '.join(grid[i]), max_y - i)
    
    print(' '.join(map(str, range(1, max_x + 1))))

battleships = [
    Battleship("A", 3, 5),
    Battleship("Z", 7, 1),
    Battleship("Z", 4, 4),
    Battleship("A", 2, 6),
    Battleship("A", 4, 2)
]

print_battleship_map(battleships)