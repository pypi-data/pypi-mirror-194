from typing import Tuple, Union
from .pawn import Pawn
from ..utilities.location import Point, bresenham, distance_between


class Square:
    def __init__(self, position: Point, symbol: str = '⬜', impassable: bool = False, is_water: bool = False,
                 is_burning: bool = False, is_lava: bool = False, damage: int = 0, occupant: Union[Pawn, None] = None) -> None:
        self.position = position
        self._base_symbol = symbol
        self._symbol = symbol
        self._temp_symbol = ''
        self._impassable = impassable
        self.is_water = is_water
        self.is_burning = is_burning
        self.is_lava = is_lava
        self.damage = damage
        self.occupant = occupant

    @property
    def name(self) -> str:
        return f"Tile at {self.position}"

    @property
    def impassable(self) -> bool:
        return self._impassable or self.occupied

    @property
    def symbol(self):
        if self.occupied:
            return self.occupant.symbol  # type: ignore
        if self._temp_symbol:
            return self._temp_symbol
        return self._symbol

    def toggle_burning(self, damage: int = 3) -> None:
        if self.is_burning:
            self.is_burning = False
            self._symbol = self._base_symbol
            self.damage = 0
        else:
            self.is_burning = True
            self._symbol = '🟨'
            self.damage = damage

    def toggle_lava(self) -> None:
        if self.is_lava:
            self.is_lava = False
            self._symbol = self._base_symbol
            self.damage = 0
        else:
            self.is_lava = True
            self._symbol = '🟥'
            self.damage = 10000

    def set_temp_symbol(self, symbol: str) -> None:
        self._symbol = symbol

    def clear_temp_symbol(self) -> None:
        self._symbol = ''

    @property
    def occupied(self) -> bool:
        return self.occupant is not None

    def trigger_effect(self) -> None:
        if self.occupied and (self.is_burning or self.is_lava):
            self.occupant._take_damage(self, self.damage, "fire")  # type: ignore

    def place(self, new_occupant: Pawn) -> str:
        '''Place a pawn in the square; returns True if successful.'''
        if self.occupied:
            return "the square is occupied!"
        if self.impassable:
            return "the square is impassable!"
        self.occupant = new_occupant
        return 'success'

    def __repr__(self):
        return self.symbol if not self.occupied else self.occupant.symbol  # type: ignore

    def __str__(self):
        return self.symbol if not self.occupied else self.occupant.symbol  # type: ignore


class Board:
    # assume all levels are square
    def __init__(self, grid: list[list[Square]] | None = None, grid_size: int = 20):
        if grid:
            self.grid_size = len(grid)
            self.grid = grid
        else:
            self.grid_size = grid_size
            self.grid = []

            for y in range(grid_size):
                self.grid.append([])
                for x in range(grid_size):
                    self.grid[y].append(Square(Point(x, y)))

    def _tick(self):
        for row in self.grid:
            for square in row:
                if square.occupied and square.position != square.occupant.position: # type: ignore
                    square.occupant = None
                square.trigger_effect()
    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)
        
    def at(self, position: Union[Point, Tuple[int, int]]) -> Square | None:
        "get square at position (x, y)"

        if isinstance(position, tuple):
            position = Point(position[0], position[1])

        if (0 > position.x >= len(self.grid[0])) or (0 > position.y >= len(self.grid)):
            return None
        return self.grid[position.y][position.x]

    def place(self, pawn: Pawn, position: Point) -> str:
        '''Place a pawn in the square; returns True if successful.'''
        if self.at(position) is None:
            return "the square is out of bounds!"
        return self.at(position).place(pawn) # type: ignore

    
    #################################################################
    # ~~ Getters, Distance Calculations, and Convenience Methods ~~ #
    #################################################################

    @property
    def dangerous_points(self) -> list[Point]:
        "get a list of points that are dangerous"
        return [square.position for row in self.grid for square in row if square.is_burning or square.is_lava]

    @property
    def dangerous_positions(self) -> list[Tuple[int, int]]:
        "get a list of positions that are dangerous"
        return [square.position.to_tuple() for row in self.grid for square in row if square.is_burning or square.is_lava]

    @property
    def impassable_points(self) -> list[Point]:
        "get a list of points that are impassable"
        return [square.position for row in self.grid for square in row if square.impassable]

    @property
    def impassable_positions(self) -> list[Tuple[int, int]]:
        "get a list of positions that are impassable"
        return [square.position.to_tuple() for row in self.grid for square in row if square.impassable]

    def get_squares_at_points(self, *points: Union[Point,tuple[int,int]]) -> list[Square]:
        "get a list of squares at the provided points"
        return list(filter(None, [self.at(point) for point in points]))

    def get_players_in_positions(self, *positions: Union[Point, Tuple[int, int]]) -> list[Pawn]:
        "get a list of players in the provided positions"
        return [self.at(pos).occupant # type: ignore
                for pos in positions
                if self.at(pos) is not None and self.at(pos).occupied] # type: ignore

    def get_players_in_squares(self, *squares: Square) -> list[Pawn]:
        "get a list of players in the provided squares"
        return list(filter(None, [square.occupant for square in squares if square.occupied]))

    def get_players_in_range(self, origin: Union[Point, tuple[int,int]], radius: int) -> list[Pawn]:
        "get a list of players in the provided radius"
        return list(filter(None,
                          [square.occupant
                          for square in self.get_squares_in_radius(origin, radius)]))

    def get_squares_in_radius(self, origin: Union[Point, tuple[int,int]], radius: int) -> list[Square]:
        "get a list of squares in the provided radius"
        if isinstance(origin, tuple):
            origin = Point(*origin)
        return list(filter(None,
                           [self.at(Point(origin.x + x, origin.y + y))
                           for x in range(-radius, radius + 1)
                           for y in range(-radius, radius + 1)
                           if (x ** 2 + y ** 2) <= radius ** 2]))

    def get_adjacent_squares(self, position: Union[Point,tuple[int,int]]) -> list[Square]:
        "get a list of adjacent squares"
        if isinstance(position, tuple):
            position = Point(*position)
        return list(filter(None,
                           [self.at(Point(position.x + x, position.y + y))
                           for x in [-1, 0, 1]
                           for y in [-1, 0, 1]
                           if not (x == y == 0)]))

    def get_adjacent_entities(self, origin: Pawn) -> list[Pawn]:
        "get a list of all entities in melee range of the origin pawn"
        return self.get_players_in_squares(*self.get_adjacent_squares(origin.position))
    
    def get_melee_range_entities(self, origin: Pawn) -> list[Pawn]:
        "get a list of all entities in melee range of the origin pawn"
        return self.get_adjacent_entities(origin)

    def get_nearest_player_to(self, origin: Pawn) -> Pawn:
        "get the nearest player to the origin pawn"
        player = None
        radius = 1
        while player is None:
            players = self.get_players_in_range(origin.position, radius)
            if players:
                player = min(players, key=lambda p: distance_between(origin, p)) # type: ignore
            radius += 1
        return player

    def distance_between(self, origin: Union[Pawn, Point], destination: Union[Pawn, Point]) -> float:
        "get the distance between two points"
        if isinstance(origin, Pawn):
            origin = origin.position
        if isinstance(destination, Pawn):
            destination = destination.position
        return distance_between(origin, destination)

    def get_squares_in_line(self, origin: Point, destination: Point) -> list[Square]|None:
        if self.at(origin) is not None and self.at(destination) is not None and origin != destination:
            return self.get_squares_at_points(*list(bresenham(origin, destination)))

    def __repr__(self):
        return f"Board({len(self.grid)} * {len(self.grid[0])} grid)"

    def __str__(self):
        s = ""
        for y in range(len(self.grid)-1, -1, -1):
            for x in range(len(self.grid[0])):
                s += str(self.grid[y][x].symbol)
            s += "\n"

        return s

    def __getitem__(self, position: Union[Point,tuple[int,int]]) -> Square | None:
        return self.at(position)

