from enum import Enum
from g_python.hpacket import HPacket

class HGroupMode(Enum):
    OPEN: 0
    ADMINAPPROVAL: 1
    CLOSED: 2

        
class HBubble(Enum):
    NORMAL: 0
    RED: 3
    BLUE: 4
    YELLOW: 5
    GREEN: 6
    BLACK: 7
    ZOMBIE: 9
    SKULL: 10
    PINK: 12
    PURPLE: 13
    ORANGE: 14
    HEART: 16
    ROSE: 17
    PIG: 19
    DOG: 20
    DUCK: 21
    DRAGON: 22
    STAFF: 23
    BATS: 24
    CONSOLE: 25
    STORM: 27
    PIRATE: 29
    AMBASSADOR: 37
        

class HDance(Enum):
    NONE = 0
    NORMAL = 1
    POGOMOGO = 2
    DUCKFUNK = 3
    THEROLLIE = 4
    
    
class HAction(Enum):
    NONE = 0
    MOVE = 1
    SIT = 2
    LAY = 3
    SIGN = 4


class HDirection(Enum):
    NORTH = 0
    NORTHEAST = 1
    EAST = 2
    SOUTHEAST = 3
    SOUTH = 4
    SOUTHWEST = 5
    WEST = 6
    NORTHWEST = 7


class HEntityType(Enum):
    HABBO = 1
    PET = 2
    OLD_BOT = 3
    BOT = 4


class HGender(Enum):
    UNISEX = "U"
    MALE = "M"
    FEMALE = "F"


class HSign(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    HEART = 11
    SKULL = 12
    EXCLAMATION = 13
    SOCCERBALL = 14
    SMILE = 15
    REDCARD = 16
    YELLOWCARD = 17
    INVISIBLE = 18


class HStance(Enum):
    STAND = 0
    SIT = 1
    LAY = 2


class HPoint:
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "x: {}, y: {}, z: {}".format(self.x, self.y, self.z)

    def __repr__(self):
        return "HPoint({},{},{})".format(self.x, self.y, self.z)


class HEntity:
    def __init__(self, packet: HPacket):
        self.id, self.name, self.motto, self.figure_id, self.index, x, y, z, _, entity_type_id = \
            packet.read('isssiiisii')
        self.tile = HPoint(x, y, float(z))
        self.entity_type = HEntityType(entity_type_id)

        self.stuff = []
        if self.entity_type == HEntityType.HABBO:
            self.gender = packet.read_string()
            self.stuff.extend(packet.read('ii'))
            self.favorite_group = packet.read_string()
            self.stuff.extend(packet.read('siB'))
        elif self.entity_type == HEntityType.PET:
            self.stuff.extend(packet.read('iisiBBBBBBis'))
        elif self.entity_type == HEntityType.BOT:
            self.stuff.extend(packet.read('sis'))
            self.stuff.append([packet.read_short() for _ in range(packet.read_int())])

    def __str__(self):
        return '{}: {} - {}'.format(self.index, self.name, self.entity_type.name)

    def try_update(self, update):
        self.tile = update.tile
        self.nextTile = update.nextTile
        self.headFacing = update.headFacing
        self.bodyFacing = update.bodyFacing

    @classmethod
    def parse(cls, packet):
        return [HEntity(packet) for _ in range(packet.read_int())]


class HFriends:
    def __init__(self, packet):
        self.friends = []
        _, _ = packet.read('ii')
        self.total_friends = packet.read_int()
        for _ in range(self.total_friends):
            id_user, name, _, _, _, clothes, _, motto = packet.read('isiBBsis')
            if packet.read_int() == 0:
                _, _ = packet.read('BB')
            _, _ = packet.read('Bs')
            self.friends.append([id_user, name, clothes, motto])


def read_stuff(packet, category):
    stuff = []
    cat2 = category & 0xFF

    if cat2 == 0:  # legacy
        stuff.append(packet.read_string())
    if cat2 == 1:  # map
        stuff.append([packet.read('ss') for _ in range(packet.read_int())])
    if cat2 == 2:  # string array
        stuff.append([packet.read_string() for _ in range(packet.read_int())])
    if cat2 == 3:  # vote results
        stuff.extend(packet.read('si'))
    if cat2 == 5:  # int array
        stuff.append([packet.read_int() for _ in range(packet.read_int())])
    if cat2 == 6:  # highscores
        stuff.extend(packet.read('sii'))
        stuff.append([(packet.read_int(), [packet.read_string() for _ in range(packet.read_int())]) for _ in
                      range(packet.read_int())])
    if cat2 == 7:  # crackables
        stuff.extend(packet.read('sii'))

    if (category & 0xFF00 & 0x100) > 0:
        stuff.extend(packet.read('ii'))

    return stuff


class HUserUpdate:
    def __init__(self, packet: HPacket):
        self.index, x, y, z, head, body, self.action = packet.read('iiisiis')
        self.tile = get_tile_from_coords(x, y, z)
        self.headFacing = HDirection(head)
        self.bodyFacing = HDirection(body)
        self.nextTile = self.predict_next_tile()

    def __str__(self):
        return '<HUserUpdate> [{}] - X: {} - Y: {} - Z: {} - head {} - body {} - next tile {}'\
            .format(self.index, self.tile.x, self.tile.y, self.tile.z, self.headFacing.name, self.bodyFacing.name, self.nextTile)

    def predict_next_tile(self):
        actions = self.action.split('/mv ')
        if len(actions) > 1:
            (x, y, z) = actions[1].replace('/', '').split(',')
            return get_tile_from_coords(int(x), int(y), z)
        else:
            return HPoint(-1, -1, 0.0)

    @classmethod
    def parse(cls, packet):
        return [HUserUpdate(packet) for _ in range(packet.read_int())]

def get_tile_from_coords(x, y, z) -> HPoint:
    try:
        z = float(z)
    except ValueError:
        z = 0.0

    return HPoint(x, y, z)

class HFloorItem:
    def __init__(self, packet):
        self.id, self.type_id, x, y, facing_id, z = packet.read('iiiiis')
        self.tile = HPoint(x, y, float(z))
        self.facing = HDirection(facing_id)

        h, _, self.category = packet.read('sii')
        self.height = float(h)
        self.stuff = read_stuff(packet, self.category)

        self.seconds_to_expiration, self.usage_policy, self.owner_id = packet.read('iii')
        self.owner = None  # expected to be filled in by parse class method

        if self.type_id < 0:
            packet.read_string()

    @classmethod
    def parse(cls, packet):
        owners = {}
        for _ in range(packet.read_int()):
            id = packet.read_int()
            owners[id] = packet.read_string()

        furnis = [HFloorItem(packet) for _ in range(packet.read_int())]
        for furni in furnis:
            furni.owner = owners[furni.owner_id]

        return furnis


class HGroup:
    def __init__(self, packet):
        self.id, self.name, self.badge_code, self.primary_color, self.secondary_color, \
        self.is_favorite, self.owner_id, self.has_forum = packet.read('issssBiB')


class HUserProfile:
    def __init__(self, packet):
        self.id, self.username, self.figure, self.motto, self.creation_date, self.achievement_score, \
        self.friend_count, self.is_friend, self.is_requested_friend, self.is_online = packet.read('issssiiBBB')

        self.groups = [HGroup(packet) for _ in range(packet.read_int())]
        self.last_access_since, self.open_profile = packet.read('iB')

        self.idk1, self.level, self.idk2, self.gems, self.idk3, self.idk4 = packet.read('BiiiBB')

    def __str__(self):
        return "id: {}, username: {}, score: {}, friends: {}, online: {}, groups: {}, level: {}, gems: {}".format(
            self.id, self.username, self.achievement_score,
            self.friend_count, self.is_online, len(self.groups), self.level, self.gems)


class HWallItem:
    def __init__(self, packet):
        self.id, self.type_id, self.location, self.state, self.seconds_to_expiration, self.usage_policy, \
        self.owner_id = packet.read('sissiii')

    @classmethod
    def parse(cls, packet):
        owners = {}
        for _ in range(packet.read_int()):
            id = packet.read_int()
            owners[id] = packet.read_string()

        furnis = [HWallItem(packet) for _ in range(packet.read_int())]
        for furni in furnis:
            furni.owner = owners[furni.owner_id]

        return furnis


class HWallUpdate:
    '''
        def update(p):
            wall = HWallUpdate(p.packet)
            print(wall.widthX, wall.widthY, wall.lengthX, wall.lengthY)
            # id / cord / rotation / widthX / widthY / lengthX / lengthY

        ext.intercept(Direction.TO_SERVER, update, 'MoveWallItem')
    '''
    def __init__(self, packet):
        self.id, self.cord = packet.read('is')

        self.cord = self.cord.split()
        self.rotation = self.cord[2]
        self.widthX, self.widthY = self.cord[0].split(',')
        self.widthX = self.widthX.split('=')[1]
        self.lengthX, self.lengthY = self.cord[1].split(',')
        self.lengthX = self.lengthX.split('=')[1]


class HInventoryItem:
    def __init__(self, packet):
        _, test = packet.read('is')
        self.is_floor_furni = (test == 'S')

        self.id, self.type_id, _, self.category = packet.read('iiii')
        self.stuff = read_stuff(packet, self.category)

        self.is_groupable, self.is_tradeable, _, self.market_place_allowed, self.seconds_to_expiration, \
        self.has_rent_period_started, self.room_Id = packet.read('BBBBiBi')

        if self.is_floor_furni:
            self.slot_id = packet.read_string()
            packet.read_int()

    @classmethod
    def parse(cls, packet):
        total, current = packet.read('ii')
        return [HInventoryItem(packet) for _ in range(packet.read_int())]
