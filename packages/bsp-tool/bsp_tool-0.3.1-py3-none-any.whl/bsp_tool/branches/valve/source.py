import collections
import enum
import struct
from typing import List

from .. import base
from .. import shared
from .. import vector
from ..id_software import quake


BSP_VERSION = 19  # & 20

GAMES = ["Counter-Strike: Source",  # counter-strike source/cstrike
         "Half-Life 1: Source - Deathmatch",  # Half-Life 1 Source Deathmatch/hl1mp
         "Half-Life 2",  # Half-Life 2/hl2
         "Half-Life 2: Episode 1"]  # Half-Life 2/episodic
GAME_VERSIONS = {game: BSP_VERSION for game in GAMES}


class LUMP(enum.Enum):
    ENTITIES = 0
    PLANES = 1
    TEXTURE_DATA = 2
    VERTICES = 3
    VISIBILITY = 4
    NODES = 5
    TEXTURE_INFO = 6
    FACES = 7  # version 1
    LIGHTING = 8  # version 1
    OCCLUSION = 9  # version 2
    LEAVES = 10  # version 1
    FACE_IDS = 11
    EDGES = 12
    SURFEDGES = 13
    MODELS = 14
    WORLD_LIGHTS = 15
    LEAF_FACES = 16
    LEAF_BRUSHES = 17
    BRUSHES = 18
    BRUSH_SIDES = 19
    AREAS = 20
    AREA_PORTALS = 21
    PORTALS = 22
    CLUSTERS = 23
    PORTAL_VERTICES = 24
    CLUSTER_PORTALS = 25
    DISPLACEMENT_INFO = 26
    ORIGINAL_FACES = 27
    PHYSICS_DISPLACEMENT = 28
    PHYSICS_COLLIDE = 29
    VERTEX_NORMALS = 30
    VERTEX_NORMAL_INDICES = 31
    DISPLACEMENT_LIGHTMAP_ALPHAS = 32  # deprecated / X360 ?
    DISPLACEMENT_VERTICES = 33
    DISPLACEMENT_LIGHTMAP_SAMPLE_POSITIONS = 34
    GAME_LUMP = 35
    LEAF_WATER_DATA = 36
    PRIMITIVES = 37
    PRIMITIVE_VERTICES = 38  # deprecated / X360 ?
    PRIMITIVE_INDICES = 39
    PAKFILE = 40
    CLIP_PORTAL_VERTICES = 41
    CUBEMAPS = 42
    TEXTURE_DATA_STRING_DATA = 43
    TEXTURE_DATA_STRING_TABLE = 44
    OVERLAYS = 45
    LEAF_MIN_DIST_TO_WATER = 46
    FACE_MACRO_TEXTURE_INFO = 47
    DISPLACEMENT_TRIS = 48
    PHYSICS_COLLIDE_SURFACE = 49  # deprecated / X360 ?
    WATER_OVERLAYS = 50  # deprecated / X360 ?
    LIGHTMAP_PAGES = 51
    LIGHTMAP_PAGE_INFOS = 52
    LIGHTING_HDR = 53  # version 1
    WORLD_LIGHTS_HDR = 54
    LEAF_AMBIENT_LIGHTING_HDR = 55  # version 1
    LEAF_AMBIENT_LIGHTING = 56  # version 1
    XZIP_PAKFILE = 57  # deprecated / X360 ?
    FACES_HDR = 58  # version 1
    MAP_FLAGS = 59
    OVERLAY_FADES = 60
    UNUSED_61 = 61
    UNUSED_62 = 62
    UNUSED_63 = 63


lump_header_address = {LUMP_ID: (8 + i * 16) for i, LUMP_ID in enumerate(LUMP)}
SourceLumpHeader = collections.namedtuple("SourceLumpHeader", ["offset", "length", "version", "fourCC"])


def read_lump_header(file, LUMP: enum.Enum) -> SourceLumpHeader:
    file.seek(lump_header_address[LUMP])
    offset, length, version, fourCC = struct.unpack("4I", file.read(16))
    header = SourceLumpHeader(offset, length, version, fourCC)
    return header

# TODO: changes from GoldSrc -> Source
# MipTexture.flags -> TextureInfo.flags (Surface enum)

# a rough map of the relationships between lumps:
#
#                     /-> SurfEdge -> Edge -> Vertex
# Leaf -> Node -> Face -> Plane
#                     \-> DisplacementInfo -> DisplacementVertex
#
# ClipPortalVertices are AreaPortal geometry [citation neeeded]


# engine limits: (2013 SDK bspfile.h)
class MIN(enum.Enum):
    DISPLACEMENT_POWER = 2


class MAX(enum.Enum):
    # misc:
    CUBEMAP_SAMPLES = 1024
    DISPLACEMENT_POWER = 4
    DISPLACEMENT_CORNER_NEIGHBORS = 4
    ENTITY_KEY, ENTITY_VALUE = 32, 1024  # key value pair sizes
    LIGHTMAPS = 4  # ? left over from Quake / GoldSrc lightmap format ?
    LIGHTMAP_DIMENSION_WITH_BORDER_BRUSH = 35  # "vbsp cut limit" +1 (to account for rounding errors)
    LIGHTMAP_DIMENSION_WITHOUT_BORDER_BRUSH = 32
    LIGHTMAP_DIMENSION_WITH_BORDER_DISPLACEMENT = 128
    LIGHTMAP_DIMENSION_WITHOUT_BORDER_DISPLACEMENT = 125
    # absolute maximum, based on previous values
    LIGHTMAP_DIMENSION_WITH_BORDER = LIGHTMAP_DIMENSION_WITH_BORDER_DISPLACEMENT
    LIGHTMAP_DIMENSION_WITHOUT_BORDER = LIGHTMAP_DIMENSION_WITHOUT_BORDER_DISPLACEMENT
    LIGHTING_STYLES = 64
    PORTAL_VERTICES = 128000
    # lumps:
    ENTITIES = 8192
    PLANES = 65536
    TEXTURE_DATA = 2048
    VERTICES = 65536
    VISIBILITY_CLUSTERS = 65536
    VISIBILITY_SIZE = 0x1000000  # "increased in BSPVERSION 7"
    NODES = 65536
    TEXTURE_INFO = 12288
    FACES = 65536
    LIGHTING_SIZE = 0x1000000
    LEAVES = 65536
    EDGES = 256000
    SURFEDGES = 512000
    MODELS = 1024
    WORLD_LIGHTS = 8192
    LEAF_FACES = 65536
    LEAF_BRUSHES = 65536
    BRUSHES = 8192
    BRUSH_SIDES = 65536
    AREAS = 256
    AREA_BYTES = AREAS // 8
    AREA_PORTALS = 1024
    # UNUSED_24 [PORTALVERTS] = 128000
    DISPLACEMENT_INFO = 2048
    ORIGINAL_FACES = FACES
    VERTEX_NORMALS = 256000
    VERTEX_NORMAL_INDICES = 256000
    DISPLACEMENT_VERTICES_FOR_ONE = (2 ** DISPLACEMENT_POWER + 1) ** 2
    DISPLACEMENT_VERTICES = DISPLACEMENT_INFO * DISPLACEMENT_VERTICES_FOR_ONE
    LEAF_WATER_DATA = 32768
    PRIMITIVES = 32768
    PRIMITIVE_VERTICES = 65536
    PRIMITIVE_INDICES = 65536
    TEXDATA_STRING_DATA = 256000
    TEXDATA_STRING_TABLE = 65536
    OVERLAYS = 512
    DISPLACEMENT_TRIANGLES_FOR_ONE = 2 ** DISPLACEMENT_POWER * 3
    DISPLACEMENT_TRIANGLES = DISPLACEMENT_INFO * DISPLACEMENT_TRIANGLES_FOR_ONE
    WATER_OVERLAYS = 16384
    LIGHTING_HDR_SIZE = LIGHTING_SIZE
    WORLD_LIGHTS_HDR = WORLD_LIGHTS
    FACES_HDR = FACES


class MAX_X360(enum.Enum):  # "force static arrays to be very small"
    """#if !defined( BSP_USE_LESS_MEMORY )"""
    ENTITIES = 2
    PLANES = 2
    TEXTURE_DATA = 2
    VERTICES = 2
    VISIBILITY_CLUSTERS = 2
    NODES = 2
    TEXTURE_INFO = 2
    FACES = 2
    LIGHTING_SIZE = 2
    LEAVES = 2
    EDGES = 2
    SURFEDGES = 2
    MODELS = 2
    WORLD_LIGHTS = 2
    LEAF_FACES = 2
    LEAF_BRUSHES = 2
    BRUSHES = 2
    BRUSH_SIDES = 2
    AREAS = 2
    AREA_BYTES = 2
    AREA_PORTALS = 2
    # UNUSED_24 [PORTALVERTS] = 2
    DISPLACEMENT_INFO = 2
    ORIGINAL_FACES = FACES
    VERTEX_NORMALS = 2
    VERTEX_NORMAL_INDICES = 2
    DISPLACEMENT_VERTICES_FOR_ONE = (2 ** MAX.DISPLACEMENT_POWER.value + 1) ** 2
    DISPLACEMENT_VERTICES = DISPLACEMENT_INFO * DISPLACEMENT_VERTICES_FOR_ONE
    LEAF_WATER_DATA = 2
    PRIMITIVES = 2
    PRIMITIVE_VERTICES = 2
    PRIMITIVE_INDICES = 2
    TEXDATA_STRING_DATA = 2
    TEXDATA_STRING_TABLE = 2
    OVERLAYS = 2
    DISPLACEMENT_TRIANGLES_FOR_ONE = 2 ** MAX.DISPLACEMENT_POWER.value * 3
    DISPLACEMENT_TRIANGLES = DISPLACEMENT_INFO * DISPLACEMENT_TRIANGLES_FOR_ONE
    WATER_OVERLAYS = 2
    LIGHTING_HDR_SIZE = LIGHTING_SIZE
    WORLD_LIGHTS_HDR = WORLD_LIGHTS
    FACES_HDR = FACES


# flag enums
class Contents(enum.IntFlag):  # src/public/bspflags.h
    """Brush flags"""  # NOTE: vbsp sets these in src/utils/vbsp/textures.cpp
    # visible
    EMPTY = 0x00
    SOLID = 0x01
    WINDOW = 0x02
    AUX = 0x04  # unused?
    GRATE = 0x08  # allows bullets & vis
    SLIME = 0x10
    WATER = 0x20
    MIST = 0x40  # BLOCK_LOS, blocks AI line of sight
    OPAQUE = 0x80  # blocks NPC line of sight, may be non-solid
    TEST_FOG_VOLUME = 0x100  # cannot be seen through, but may be non-solid
    UNUSED_1 = 0x200
    UNUSED_2 = 0x400  # titanfall vertex lump flags?
    TEAM1 = 0x0800
    TEAM2 = 0x1000
    IGNORE_NO_DRAW_OPAQUE = 0x2000  # ignore opaque if Surface.NO_DRAW
    MOVEABLE = 0x4000  # pushables
    # not visible
    AREAPORTAL = 0x8000
    PLAYER_CLIP = 0x10000
    MONSTER_CLIP = 0x20000
    # CURRENT_ flags are for moving water
    CURRENT_0 = 0x40000
    CURRENT_90 = 0x80000
    CURRENT_180 = 0x100000
    CURRENT_270 = 0x200000
    CURRENT_UP = 0x400000
    CURRENT_DOWN = 0x800000
    ORIGIN = 0x1000000  # "removed before bsping an entity"
    MONSTER = 0x2000000  # in-game only, shouldn't be in a .bsp
    DEBRIS = 0x4000000
    DETAIL = 0x8000000  # func_detail; for VVIS (visleaf assembly from Brushes)
    TRANSLUCENT = 0x10000000
    LADDER = 0x20000000
    HITBOX = 0x40000000  # requests hit tracing use hitboxes


class DisplacementFlags(enum.IntFlag):
    """DisplacementInfo collision flags"""
    UNUSED = 1
    NO_PHYS = 2
    NO_HULL = 4
    NO_RAY = 8


class DispTris(enum.IntFlag):
    """DisplacementTriangle flags"""
    SURFACE = 0x01
    WALKABLE = 0x02
    BUILDABLE = 0x04
    SURFPROP1 = 0x08  # ?
    SURFPROP2 = 0x10  # ?


class Surface(enum.IntFlag):  # src/public/bspflags.h
    """TextureInfo flags"""  # NOTE: vbsp sets these in src/utils/vbsp/textures.cpp
    LIGHT = 0x0001  # "value will hold the light strength"
    SKY_2D = 0x0002  # don't draw, indicates we should skylight + draw 2d sky but not draw the 3D skybox
    SKY = 0x0004  # don't draw, but add to skybox
    WARP = 0x0008  # turbulent water warp
    TRANSLUCENT = 0x0010
    NO_PORTAL = 0x0020  # the surface can not have a portal placed on it
    TRIGGER = 0x0040  # xbox hack to work around elimination of trigger surfaces, which breaks occluders
    NO_DRAW = 0x0080
    HINT = 0x0100  # make a bsp split on this face
    SKIP = 0x0200  # don't split on this face, allows for non-closed brushes
    NO_LIGHT = 0x0400  # don't calculate light
    BUMPLIGHT = 0x0800  # calculate three lightmaps for the surface for bumpmapping (ssbump?)
    NO_SHADOWS = 0x1000
    NO_DECALS = 0x2000
    NO_CHOP = 0x4000	 # don't subdivide patches on this surface
    HITBOX = 0x8000  # surface is part of a hitbox


# classes for each lump, in alphabetical order:
class Area(base.MappedArray):  # LUMP 20
    num_area_portals: int   # number of AreaPortals after first_area_portal in this Area
    first_area_portal: int  # index of first AreaPortal
    _mapping = ["num_area_portals", "first_area_portal"]
    _format = "2i"


class AreaPortal(base.MappedArray):  # LUMP 21
    # public/bspfile.h dareaportal_t &  utils/vbsp/portals.cpp EmitAreaPortals
    portal_key: int                # for tying to entities
    first_clip_portal_vert: int    # index into the ClipPortalVertex lump
    num_clip_portal_vertices: int  # number of ClipPortalVertices after first_clip_portal_vertex in this AreaPortal
    plane: int                     # index of into the Plane lump
    _mapping = ["portal_key", "other_area", "first_clip_portal_vertex",
                "num_clip_portal_vertices", "plane"]
    _format = "4Hi"


class Brush(base.Struct):  # LUMP 18
    """Assumed to carry over from .vmf"""
    first_side: int  # index into BrushSide lump
    num_sides: int   # number of BrushSides after first_side in this Brush
    contents: int    # contents bitflags
    __slots__ = ["first_side", "num_sides", "contents"]
    _format = "3i"


class BrushSide(base.Struct):  # LUMP 19
    plane: int      # index into Plane lump
    texture_info: int   # index into TextureInfo lump
    displacement_info: int  # index into DisplacementInfo lump
    bevel: int      # smoothing group?
    __slots__ = ["plane", "texture_info", "displacement_info", "bevel"]
    _format = "H3h"


class Cubemap(base.Struct):  # LUMP 42
    """Location (origin) & resolution (size)"""
    origin: List[float]  # origin.xyz
    size: int  # texture dimension (each face of a cubemap is square)
    __slots__ = ["origin", "size"]
    _format = "4i"
    _arrays = {"origin": [*"xyz"]}


class DisplacementInfo(base.Struct):  # LUMP 26
    """Holds the information defining a displacement"""
    start_position: List[float]  # rough XYZ of the vertex to orient around
    displacement_vert_start: int  # index of first DisplacementVertex
    displacement_tri_start: int   # index of first DisplacementTriangle
    # ^ length of sequence for each varies depending on power
    power: int  # level of subdivision
    flags: int  # see DisplacementFlags
    min_tesselation: int  # for tesselation shaders / triangle assembley?
    smoothing_angle: float  # ?
    contents: int  # contents bitflags
    map_face: int  # index of Face?
    __slots__ = ["start_position", "displacement_vert_start", "displacement_tri_start",
                 "power", "flags", "min_tesselation", "smoothing_angle", "contents",
                 "map_face", "lightmap_alpha_start", "lightmap_sample_position_start",
                 "edge_neighbours", "corner_neighbours", "allowed_vertices"]
    _format = "3f3iHhfiH2i88c10i"
    _arrays = {"start_position": [*"xyz"], "edge_neighbours": 44,
               "corner_neighbours": 44, "allowed_vertices": 10}
    # TODO: map neighbours with base.Struct subclasses, rather than MappedArrays
    # both the __init__ & flat methods may need some changes to accommodate this

    # def __init__(self, _tuple):
    #     super(base.Struct, self).__init__(_tuple)
    #     self.edge_neighbours = ...
    #     self.corner_neighbours = ...


class DisplacementVertex(base.Struct):  # LUMP 33
    """The positional deformation & blend value of a point in a displacement"""
    vector: List[float]  # direction of vertex offset from barymetric base
    distance: float      # length to scale deformation vector by
    alpha: float         # [0-1] material blend factor
    __slots__ = ["vector", "distance", "alpha"]
    _format = "5f"
    _arrays = {"vector": [*"xyz"]}


class Face(base.Struct):  # LUMP 7
    """makes up Models (including worldspawn), also referenced by LeafFaces"""
    plane: int       # index into Plane lump
    side: int        # "faces opposite to the node's plane direction"
    on_node: bool    # if False, face is in a leaf
    first_edge: int  # index into the SurfEdge lump
    num_edges: int   # number of SurfEdges after first_edge in this Face
    texture_info: int    # index into the TextureInfo lump
    displacement_info: int   # index into the DisplacementInfo lump (None if -1)
    surface_fog_volume_id: int  # t-junctions? QuakeIII vertex-lit fog?
    styles: int      # 4 different lighting states? "switchable lighting info"
    light_offset: int  # index of first pixel in LIGHTING / LIGHTING_HDR
    area: float  # surface area of this face
    lightmap: List[float]
    # lightmap.mins  # dimensions of lightmap segment
    # lightmap.size  # scalars for lightmap segment
    original_face: int  # ORIGINAL_FACES index, -1 if this is an original face
    num_primitives: int  # non-zero if t-juncts are present? number of Primitives
    first_primitive_id: int  # index of Primitive
    smoothing_groups: int    # lightmap smoothing group
    __slots__ = ["plane", "side", "on_node", "first_edge", "num_edges",
                 "texture_info", "displacement_info", "surface_fog_volume_id", "styles",
                 "light_offset", "area", "lightmap", "original_face",
                 "num_primitives", "first_primitive_id", "smoothing_groups"]
    _format = "Hb?i4h4bif5i2HI"
    _arrays = {"styles": 4, "lightmap": {"mins": [*"xy"], "size": ["width", "height"]}}


class LeafWaterData(base.Struct):
    surface_z: float  # global Z height of the water's surface
    min_z: float  # bottom of the water volume?
    texture_data: int  # index to this LeafWaterData's TextureData
    _format = "2fI"
    _mapping = ["surface_z", "min_z", "texture_data"]


class Model(base.Struct):  # LUMP 14
    """Brush based entities; Index 0 is worldspawn"""
    mins: List[float]  # bounding box minimums along XYZ axes
    maxs: List[float]  # bounding box maximums along XYZ axes
    origin: List[float]  # center of model, worldspawn is always at 0 0 0
    head_node: int   # index into Node lump
    first_face: int  # index into Face lump
    num_faces: int   # number of Faces after first_face in this Model
    __slots__ = ["mins", "maxs", "origin", "head_node", "first_face", "num_faces"]
    _format = "9f3i"
    _arrays = {"mins": [*"xyz"], "maxs": [*"xyz"], "origin": [*"xyz"]}


class Node(base.Struct):  # LUMP 5
    plane: int            # index into Plane lump
    children: List[int]   # 2 indices; Node if positive, Leaf if negative
    mins: List[float]     # bounding box minimums along XYZ axes
    maxs: List[float]     # bounding box maximums along XYZ axes
    first_face: int       # index into Face lump
    num_faces: int        # number of Faces after first_face in this Node
    area: int             # index into Area lump, if all children are in the same area, else -1
    padding: int          # should be empty
    __slots__ = ["plane", "children", "mins", "maxs", "first_face", "num_faces",
                 "area", "padding"]
    # area is appears to always be 0
    # however leaves correctly connect to all areas
    _format = "3i6h2H2h"
    _arrays = {"children": 2, "mins": [*"xyz"], "maxs": [*"xyz"]}


class OverlayFade(base.MappedArray):  # LUMP 60
    """Holds fade distances for the overlay of the same index"""
    _mapping = ["min", "max"]
    _format = "2f"


class TextureData(base.Struct):  # LUMP 2
    """Data on this view of a texture (.vmt), indexed by TextureInfo"""
    reflectivity: List[float]
    name_index: int  # index of texture name in TEXTURE_DATA_STRING_TABLE / TABLE
    size: List[int]  # dimensions of full texture
    view: List[int]  # dimensions of visible section of texture
    __slots__ = ["reflectivity", "name_index", "size", "view"]
    _format = "3f5i"
    _arrays = {"reflectivity": [*"rgb"], "size": ["width", "height"], "view": ["width", "height"]}


class TextureInfo(base.Struct):  # LUMP 6
    """Texture projection info & index into TEXTURE_DATA"""
    texture: List[List[float]]  # 2 texture projection vectors
    lightmap: List[List[float]]  # 2 lightmap projection vectors
    flags: int  # Surface flags
    texture_data: int  # index of TextureData
    __slots__ = ["texture", "lightmap", "flags", "texture_data"]
    _format = "16f2i"
    _arrays = {"texture": {"s": [*"xyz", "offset"], "t": [*"xyz", "offset"]},
               "lightmap": {"s": [*"xyz", "offset"], "t": [*"xyz", "offset"]}}
    # ^ nested MappedArrays; texture.s.x, texture.t.x


class WorldLight(base.Struct):  # LUMP 15
    """A static light"""
    origin: List[float]  # origin point of this light source
    intensity: float     # light strength scalar
    normal: List[float]  # light direction
    cluster: int  # ?
    type: int  # some enum?
    style: int  # related to face styles?
    # see base.fgd:
    stop_dot: float  # ?
    stop_dot2: float  # ?
    exponent: float  # falloff?
    radius: float
    # attenuations:
    constant: float
    linear: float
    quadratic: float
    # ^ these factor into some equation...
    flags: int  # bitflags?
    texture_info: int  # index of TextureInfo
    owner: int  # parent entity ID?
    __slots__ = ["origin", "intensity", "normal", "cluster", "type", "style",
                 "stop_dot", "stop_dot2", "exponent", "radius",
                 "constant", "linear", "quadratic",  # attenuation
                 "flags", "texture_info", "owner"]
    _format = "9f3i7f3i"
    _arrays = {"origin": [*"xyz"], "intensity": [*"xyz"], "normal": [*"xyz"]}


# classes for special lumps, in alphabetical order:
class StaticPropv4(base.Struct):  # sprp GAME LUMP (LUMP 35)
    """https://github.com/ValveSoftware/source-sdk-2013/blob/master/sp/src/public/gamebspfile.h#L151"""
    origin: List[float]  # origin.xyz
    angles: List[float]  # origin.yzx  QAngle; Z0 = East
    name_index: int  # index into AME_LUMP.sprp.model_names
    first_leaf: int  # index into Leaf lump
    num_leafs: int  # number of Leafs after first_leaf this StaticPropv10 is in
    solid_mode: int  # collision flags enum
    flags: int  # other flags
    skin: int  # index of this StaticProp's skin in the .mdl
    fade_distance: List[float]  # min & max distances to fade out
    lighting_origin: List[float]  # xyz position to sample lighting from
    __slots__ = ["origin", "angles", "name_index", "first_leaf", "num_leafs",
                 "solid_mode", "flags", "skin", "fade_distance", "lighting_origin"]
    _format = "6f3H2Bi5f"
    _arrays = {"origin": [*"xyz"], "angles": [*"yzx"], "fade_distance": ["min", "max"],
               "lighting_origin": [*"xyz"]}


class StaticPropv5(base.Struct):  # sprp GAME LUMP (LUMP 35)
    """https://github.com/ValveSoftware/source-sdk-2013/blob/master/sp/src/public/gamebspfile.h#L168"""
    origin: List[float]  # origin.xyz
    angles: List[float]  # origin.yzx  QAngle; Z0 = East
    name_index: int  # index into AME_LUMP.sprp.model_names
    first_leaf: int  # index into Leaf lump
    num_leafs: int  # number of Leafs after first_leaf this StaticPropv10 is in
    solid_mode: int  # collision flags enum
    flags: int  # other flags
    skin: int  # index of this StaticProp's skin in the .mdl
    fade_distance: List[float]  # min & max distances to fade out
    lighting_origin: List[float]  # xyz position to sample lighting from
    forced_fade_scale: float  # relative to pixels used to render on-screen?
    __slots__ = ["origin", "angles", "name_index", "first_leaf", "num_leafs",
                 "solid_mode", "skin", "fade_distance", "lighting_origin",
                 "forced_fade_scale"]
    _format = "6f3HBi6f2Hi2H"
    _arrays = {"origin": [*"xyz"], "angles": [*"yzx"], "fade_distance": ["min", "max"],
               "lighting_origin": [*"xyz"]}


class StaticPropv6(base.Struct):  # sprp GAME LUMP (LUMP 35)
    origin: List[float]  # origin.xyz
    angles: List[float]  # origin.yzx  QAngle; Z0 = East
    name_index: int  # index into AME_LUMP.sprp.model_names
    first_leaf: int  # index into Leaf lump
    num_leafs: int  # number of Leafs after first_leaf this StaticPropv10 is in
    solid_mode: int  # collision flags enum
    skin: int  # index of this StaticProp's skin in the .mdl
    fade_distance: List[float]  # min & max distances to fade out
    lighting_origin: List[float]  # xyz position to sample lighting from
    forced_fade_scale: float  # relative to pixels used to render on-screen?
    dx_level: List[int]  # supported directX level, will not render depending on settings
    __slots__ = ["origin", "angles", "name_index", "first_leaf", "num_leafs",
                 "solid_mode", "skin", "fade_distance", "lighting_origin",
                 "forced_fade_scale", "dx_level"]
    _format = "6f3HBi6f2Hi2H"
    _arrays = {"origin": [*"xyz"], "angles": [*"yzx"], "fade_distance": ["min", "max"],
               "lighting_origin": [*"xyz"], "dx_level": ["min", "max"]}


# {"LUMP_NAME": {version: LumpClass}}
BASIC_LUMP_CLASSES = {"DISPLACEMENT_TRIS":         {0: shared.UnsignedShorts},
                      "LEAF_FACES":                {0: shared.UnsignedShorts},
                      "SURFEDGES":                 {0: shared.Ints},
                      "TEXTURE_DATA_STRING_TABLE": {0: shared.UnsignedShorts}}

LUMP_CLASSES = {"AREAS":                 {0: Area},
                "AREA_PORTALS":          {0: AreaPortal},
                "BRUSHES":               {0: Brush},
                "BRUSH_SIDES":           {0: BrushSide},
                "CUBEMAPS":              {0: Cubemap},
                "DISPLACEMENT_INFO":     {0: DisplacementInfo},
                "DISPLACEMENT_VERTICES": {0: DisplacementVertex},
                "EDGES":                 {0: quake.Edge},
                "FACES":                 {1: Face},
                "LEAF_WATER_DATA":       {0: LeafWaterData},
                "MODELS":                {0: Model},
                "NODES":                 {0: Node},
                "OVERLAY_FADES":         {0: OverlayFade},
                "ORIGINAL_FACES":        {0: Face},
                "PLANES":                {0: quake.Plane},
                "TEXTURE_DATA":          {0: TextureData},
                "TEXTURE_INFO":          {0: TextureInfo},
                "VERTICES":              {0: quake.Vertex},
                "VERTEX_NORMALS":        {0: quake.Vertex},
                "WORLD_LIGHTS":          {0: WorldLight},
                "WORLD_LIGHTS_HDR":      {0: WorldLight}}

SPECIAL_LUMP_CLASSES = {"ENTITIES":                 {0: shared.Entities},
                        "TEXTURE_DATA_STRING_DATA": {0: shared.TextureDataStringData},
                        "PAKFILE":                  {0: shared.PakFile},
                        "PHYSICS_COLLIDE":          {0: shared.PhysicsCollide}
                        }

# {"lump": {version: SpecialLumpClass}}
GAME_LUMP_CLASSES = {"sprp": {4: lambda raw_lump: shared.GameLump_SPRP(raw_lump, StaticPropv4),
                              5: lambda raw_lump: shared.GameLump_SPRP(raw_lump, StaticPropv5),
                              6: lambda raw_lump: shared.GameLump_SPRP(raw_lump, StaticPropv6)}}
# NOTE: having some errors with CS:S


# branch exclusive methods, in alphabetical order:
def vertices_of_face(bsp, face_index: int) -> List[float]:
    """Format: [Position, Normal, TexCoord, LightCoord, Colour]"""
    face = bsp.FACES[face_index]
    uvs, uv2s = [], []
    first_edge = face.first_edge
    edges = []
    positions = []
    for surfedge in bsp.SURFEDGES[first_edge:(first_edge + face.num_edges)]:
        if surfedge >= 0:  # index is positive
            edge = bsp.EDGES[surfedge]
            positions.append(bsp.VERTICES[bsp.EDGES[surfedge][0]])
            # ^ utils/vrad/trace.cpp:637
        else:  # index is negatice
            edge = bsp.EDGES[-surfedge][::-1]  # reverse
            positions.append(bsp.VERTICES[bsp.EDGES[-surfedge][1]])
            # ^ utils/vrad/trace.cpp:635
        edges.append(edge)
    positions = t_junction_fixer(bsp, face, positions, edges)
    texture_info = bsp.TEXTURE_INFO[face.texture_info]
    texture_data = bsp.TEXTURE_DATA[texture_info.texture_data]
    texture = texture_info.texture
    lightmap = texture_info.lightmap

    def vector_of(P):
        """returns the normal of plane (P)"""
        return (P.x, P.y, P.z)

    # texture vector -> uv calculation discovered in:
    # github.com/VSES/SourceEngine2007/blob/master/src_main/engine/matsys_interface.cpp
    # SurfComputeTextureCoordinate & SurfComputeLightmapCoordinate
    for P in positions:
        # texture UV
        uv = [vector.dot(P, vector_of(texture.s)) + texture.s.offset,
              vector.dot(P, vector_of(texture.t)) + texture.t.offset]
        uv[0] /= texture_data.view.width if texture_data.view.width != 0 else 1
        uv[1] /= texture_data.view.height if texture_data.view.height != 0 else 1
        uvs.append(vector.vec2(*uv))
        # lightmap UV
        uv2 = [vector.dot(P, vector_of(lightmap.s)) + lightmap.s.offset,
               vector.dot(P, vector_of(lightmap.t)) + lightmap.t.offset]
        if any([(face.lightmap.mins.x == 0), (face.lightmap.mins.y == 0)]):
            uv2 = [0, 0]  # invalid / no lighting
        else:
            uv2[0] -= face.lightmap.mins.x
            uv2[1] -= face.lightmap.mins.y
            uv2[0] /= face.lightmap.size.x
            uv2[1] /= face.lightmap.size.y
        uv2s.append(uv2)
    normal = [bsp.PLANES[face.plane].normal] * len(positions)  # X Y Z
    colour = [texture_data.reflectivity] * len(positions)  # R G B
    return list(zip(positions, normal, uvs, uv2s, colour))


def t_junction_fixer(bsp, face: int, positions: List[List[float]], edges: List[List[float]]) -> List[List[float]]:
    # TODO: look at primitives system
    # https://github.com/magcius/noclip.website/blob/master/src/SourceEngine/BSPFile.ts#L1052
    # https://github.com/magcius/noclip.website/blob/master/src/SourceEngine/BSPFile.ts#L1537
    # report to bsp.log rather than printing
    # bsp may need a method wrapper to give a warning to check the logs
    # face_index = bsp.FACES.index(face)
    # first_edge = face.first_edge
    if {positions.count(P) for P in positions} != {1}:
        # print(f"Face #{face_index} has interesting edges (t-junction?):")
        # print("\tAREA:", f"{face.area:.3f}")
        # center = sum(map(vector.vec3, positions), start=vector.vec3()) / len(positions)
        # print("\tCENTER:", f"({center:.3f})")
        # print("\tSURFEDGES:", bsp.SURFEDGES[first_edge:first_edge + face.num_edges])
        # print("\tEDGES:", edges)
        # loops = [(e[0] == edges[i-1][1]) for i, e in enumerate(edges)]
        # if not all(loops):
        #     print("\tWARINNG! EDGES do not loop!")
        #     print("\tLOOPS:", loops)
        # print("\tPOSITIONS:", [bsp.VERTICES.index(P) for P in positions])

        # PATCH
        # -- if you see 1 index between 2 indentical indicies:
        # -- compress the 3 indices down to just the first
        repeats = [i for i, P in enumerate(positions) if positions.count(P) != 1]
        # if len(repeats) > 0:
        #     print("\tREPEATS:", repeats)
        #     print([bsp.VERTICES.index(P) for P in positions], "-->")
        if len(repeats) == 2:
            index_a, index_b = repeats
            if index_b - index_a == 2:
                # edge goes out to one point and doubles back; delete it
                positions.pop(index_a + 1)
                positions.pop(index_a + 1)
            # what about Ts around the ends?
            print([bsp.VERTICES.index(P) for P in positions])
        else:
            if repeats[1] == repeats[0] + 1 and repeats[1] == repeats[2] - 1:
                positions.pop(repeats[1])
                positions.pop(repeats[1])
            print([bsp.VERTICES.index(P) for P in positions])
    return positions


def displacement_indices(power: int) -> List[List[int]]:  # not directly a method
    """returns an array of indices ((2 ** power) + 1) ** 2 long"""
    power2 = 2 ** power
    power2A = power2 + 1
    power2B = power2 + 2
    power2C = power2 + 3
    tris = []
    for line in range(power2):
        line_offset = power2A * line
        for block in range(2 ** (power - 1)):
            offset = line_offset + 2 * block
            if line % 2 == 0:  # |\|/|
                tris.extend([offset + 0, offset + power2A, offset + 1])
                tris.extend([offset + power2A, offset + power2B, offset + 1])
                tris.extend([offset + power2B, offset + power2C, offset + 1])
                tris.extend([offset + power2C, offset + 2, offset + 1])
            else:  # |/|\|
                tris.extend([offset + 0, offset + power2A, offset + power2B])
                tris.extend([offset + 1, offset + 0, offset + power2B])
                tris.extend([offset + 2, offset + 1, offset + power2B])
                tris.extend([offset + power2C, offset + 2, offset + power2B])
    return tris


def vertices_of_displacement(bsp, face_index: int) -> List[List[float]]:
    """Format: [Position, Normal, TexCoord, LightCoord, Colour]"""
    face = bsp.FACES[face_index]
    if face.displacement_info == -1:
        raise RuntimeError(f"Face #{face_index} is not a displacement!")
    base_vertices = bsp.vertices_of_face(face_index)
    if len(base_vertices) != 4:
        raise RuntimeError(f"Face #{face_index} does not have 4 corners (probably t-junctions)")
    disp_info = bsp.DISPLACEMENT_INFO[face.displacement_info]
    start = vector.vec3(*disp_info.start_position)
    base_quad = [vector.vec3(*P) for P, N, uv, uv2, rgb in base_vertices]
    # rotate so the point closest to start on the quad is index 0
    if start not in base_quad:
        start = sorted(base_quad, key=lambda P: (start - P).magnitude())[0]
    starting_index = base_quad.index(start)

    def rotated(q):
        return q[starting_index:] + q[:starting_index]

    A, B, C, D = rotated(base_quad)
    AD = D - A
    BC = C - B
    quad = rotated(base_vertices)
    uvA, uvB, uvC, uvD = [vector.vec2(*uv) for P, N, uv, uv2, rgb in quad]
    uvAD = uvD - uvA
    uvBC = uvC - uvB
    uv2A, uv2B, uv2C, uv2D = [vector.vec2(*uv2) for P, N, uv, uv2, rgb in quad]
    uv2AD = uv2D - uv2A
    uv2BC = uv2C - uv2B
    power2 = 2 ** disp_info.power
    disp_verts = bsp.DISPLACEMENT_VERTICES[disp_info.displacement_vert_start:]
    disp_verts = disp_verts[:(power2 + 1) ** 2]
    vertices = []
    for index, disp_vertex in enumerate(disp_verts):
        t1 = index % (power2 + 1) / power2
        t2 = index // (power2 + 1) / power2
        bary_vert = vector.lerp(A + (AD * t1), B + (BC * t1), t2)
        # ^ interpolates across the base_quad to find the barymetric point
        displacement_vert = [x * disp_vertex.distance for x in disp_vertex.vector]
        true_vertex = [a + b for a, b in zip(bary_vert, displacement_vert)]
        texture_uv = vector.lerp(uvA + (uvAD * t1), uvB + (uvBC * t1), t2)
        lightmap_uv = vector.lerp(uv2A + (uv2AD * t1), uv2B + (uv2BC * t1), t2)
        normal = base_vertices[0][1]
        colour = base_vertices[0][4]
        vertices.append((true_vertex, normal, texture_uv, lightmap_uv, colour))
    return vertices


# TODO: vertices_of_model: walk the node tree
# TODO: vertices_of_node

methods = [vertices_of_face, vertices_of_displacement, shared.worldspawn_volume]
