import random
from domain.entities.tile import Tile
from domain.entities.position import Position

class Room:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = (x + w // 2, y + h // 2)

class MapGenerator:
    TILE_SIZE = 20
    WIDTH, HEIGHT = 100, 100  # 2000x2000 pixels

    @staticmethod
    def generate_map():
        # Initialize all tiles as walls
        tiles = [Tile(Position(x * MapGenerator.TILE_SIZE, y * MapGenerator.TILE_SIZE), "wall", False) 
                 for y in range(MapGenerator.HEIGHT) for x in range(MapGenerator.WIDTH)]
        
        # Generate rooms
        rooms = []
        for _ in range(20):
            while True:
                w = random.randint(5, 10)
                h = random.randint(5, 10)
                x = random.randint(0, MapGenerator.WIDTH - w)
                y = random.randint(0, MapGenerator.HEIGHT - h)
                new_room = Room(x, y, w, h)
                if all(not (new_room.x < existing.x + existing.w and new_room.x + new_room.w > existing.x and
                            new_room.y < existing.y + existing.h and new_room.y + new_room.h > existing.y) 
                       for existing in rooms):
                    rooms.append(new_room)
                    break
        
        # Carve out rooms as path tiles
        for room in rooms:
            for dx in range(room.w):
                for dy in range(room.h):
                    tx = room.x + dx
                    ty = room.y + dy
                    idx = ty * MapGenerator.WIDTH + tx
                    tiles[idx].type = "path"
                    tiles[idx].passable = True
        
        # Connect rooms with wider corridors
        rooms.sort(key=lambda r: r.center[0])
        for i in range(len(rooms) - 1):
            MapGenerator.connect_rooms(tiles, rooms[i], rooms[i + 1])
        
        for _ in range(5):
            r1, r2 = random.sample(rooms, 2)
            MapGenerator.connect_rooms(tiles, r1, r2)
        
        # Place cages
        cage_rooms = random.sample(rooms, 3)
        for room in cage_rooms:
            cx, cy = room.center
            idx = cy * MapGenerator.WIDTH + cx
            tiles[idx].type = "cage"
        
        # Place escape points
        escape_rooms = random.sample([r for r in rooms if r not in cage_rooms], 2)
        for room in escape_rooms:
            cx, cy = room.center
            idx = cy * MapGenerator.WIDTH + cx
            tiles[idx].type = "escape"
        
        # Add bushes
        for _ in range(50):
            while True:
                x = random.randint(0, MapGenerator.WIDTH - 1)
                y = random.randint(0, MapGenerator.HEIGHT - 1)
                idx = y * MapGenerator.WIDTH + x
                if tiles[idx].type == "path":
                    tiles[idx].type = "bush"
                    break
        
        # Calculate key positions
        cage_positions = [Position(room.center[0] * MapGenerator.TILE_SIZE, room.center[1] * MapGenerator.TILE_SIZE) 
                          for room in cage_rooms]
        escape_positions = [Position(room.center[0] * MapGenerator.TILE_SIZE, room.center[1] * MapGenerator.TILE_SIZE) 
                            for room in escape_rooms]
        
        # Select spawn room
        available_rooms = [r for r in rooms if r not in cage_rooms and r not in escape_rooms]
        spawn_room = random.choice(available_rooms)
        spawn_pos = Position(spawn_room.center[0] * MapGenerator.TILE_SIZE, 
                             spawn_room.center[1] * MapGenerator.TILE_SIZE)
        
        # Place guards
        guard_rooms = random.sample(available_rooms, 2)
        guard_positions = []
        for r in guard_rooms:
            gx = random.randint(r.x, r.x + r.w - 1)
            gy = random.randint(r.y, r.y + r.h - 1)
            guard_pos = Position(gx * MapGenerator.TILE_SIZE, gy * MapGenerator.TILE_SIZE)
            guard_positions.append(guard_pos)
        
        return {
            'tiles': tiles,
            'spawn_pos': spawn_pos,
            'cage_positions': cage_positions,
            'escape_positions': escape_positions,
            'guard_positions': guard_positions
        }

    @staticmethod
    def connect_rooms(tiles, r1, r2):
        cx1, cy1 = r1.center
        cx2, cy2 = r2.center
        if random.choice([True, False]):
            # Horizontal then vertical (3 tiles wide)
            for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                for dy in [-1, 0, 1]:
                    y = cy1 + dy
                    if 0 <= y < MapGenerator.HEIGHT:
                        idx = y * MapGenerator.WIDTH + x
                        tiles[idx].type = "path"
                        tiles[idx].passable = True
            for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                for dx in [-1, 0, 1]:
                    x = cx2 + dx
                    if 0 <= x < MapGenerator.WIDTH:
                        idx = y * MapGenerator.WIDTH + x
                        tiles[idx].type = "path"
                        tiles[idx].passable = True
        else:
            # Vertical then horizontal (3 tiles wide)
            for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                for dx in [-1, 0, 1]:
                    x = cx1 + dx
                    if 0 <= x < MapGenerator.WIDTH:
                        idx = y * MapGenerator.WIDTH + x
                        tiles[idx].type = "path"
                        tiles[idx].passable = True
            for x in range(min(cx1, cx2), max(cx2, cx1) + 1):
                for dy in [-1, 0, 1]:
                    y = cy2 + dy
                    if 0 <= y < MapGenerator.HEIGHT:
                        idx = y * MapGenerator.WIDTH + x
                        tiles[idx].type = "path"
                        tiles[idx].passable = True