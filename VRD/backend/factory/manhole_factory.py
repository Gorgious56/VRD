import bpy
from math import pi, cos, sin
from . import object_factory as obj_fac
from . import primitive_factory as prim_fac
from . import modifier_factory as mod_fac


def create_manhole_bottom_pipes(lod: int, radius: float, settings) -> bpy.types.Object:
    outlet_radius = int(settings.outlet_diameter) / 2000

    vertices = [(-2 * radius, 0, 0), (-radius, 0, 0), (0, 0, 0)]
    skin_radii = [(outlet_radius, outlet_radius), (outlet_radius, outlet_radius), (outlet_radius, outlet_radius)]
    edges = [(0, 1), (1, 2)]

    for i in range(settings.inlets):
        angle = getattr(settings, f"inlet_{i+1}_angle")
        skin_radius = int(getattr(settings, f"inlet_{i+1}_diameter")) / 2000
        vertices.extend((
            (radius * cos(angle) * 1.01, radius * sin(angle) * 1.01, 0),
            (2 * radius * cos(angle), 2 * radius * sin(angle), 0),
        ))
        skin_radii.extend(((skin_radius, skin_radius), (skin_radius, skin_radius)))
        edges.extend(((2, i * 2 + 3), (i * 2 + 3, i * 2 + 4)))

    pipes = obj_fac.ccreate_mesh_objectreate_object(
        name="Manhole_Bottom_Bool_Pipes",
        auto_smooth=True,
        vertices=vertices,
        edges=edges,
        used_as_boolean=True,
    )
    mod_fac.add_modifier(pipes, mod_fac.ModSettings('WELD', "VRD_WELD"))
    mod_fac.add_modifier(pipes, mod_fac.ModSettings('SKIN', "VRD_PIPE_DIAMETER", {"use_smooth_shade": True, "branch_smoothing": 1}))
    for i, v in enumerate(pipes.data.skin_vertices[0].data):
            v.radius = skin_radii[i]

    mod_fac.add_modifier(pipes, mod_fac.ModSettings('SUBSURF', "VRD_SUBSURF", {"levels": settings.lod // 4, "render_levels": settings.lod // 4}))

    return pipes


def create_manhole_bottom(settings) -> bpy.types.Object:
    radius = settings.radius
    lod = settings.lod
    bot_height = 0.61
    bot_thickness = 0.1
    bot_bot_thickness = 0.25

    bot_obj_bool_main = prim_fac.create_cylinder(
        radius=radius - bot_thickness,
        height=bot_height,
        lod=lod,
        name="Manhole_Bottom_Bool_Main",
        location=(0, 0, bot_bot_thickness),
        used_as_boolean=True)
    

    bot_obj_bool_top = prim_fac.create_cylinder(
        radius=radius - bot_thickness / 2,
        height=bot_height,
        lod=lod,
        name="Manhole_Bottom_Bool_Top",
        location=(0, 0, bot_height - bot_thickness / 2),
        used_as_boolean=True)

    pipes = create_manhole_bottom_pipes(lod, radius, settings)    
    pipes.location[2] += bot_bot_thickness
    pipes.rotation_euler = (0.01, 0, 0)

    bot_obj = prim_fac.create_cylinder(
        radius=settings.radius,
        height=bot_height,
        lod=settings.lod,
        name="Manhole_Bottom")

    for boolean in (bot_obj_bool_top, bot_obj_bool_main):
        boolean.parent = bot_obj
        mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('BOOLEAN', 'VRD_BOOL_MAIN', {"object": boolean}))

    mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('WELD', "VRD_LAST_WELD"))
    mod_fac.add_modifier(bot_obj, mod_fac.ModSettings(
        'BEVEL',
        "VRD_LAST_BVL",
        {
            "limit_method": 'ANGLE',
            "width": 0.002,
            "segments": settings.lod // 4,
            "angle_limit": pi * 0.45,
        }))

    for boolean in (pipes,):
        boolean.parent = bot_obj
        mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('BOOLEAN', 'VRD_BOOL_MAIN', {"object": boolean}))

    mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('WEIGHTED_NORMAL', "VRD_NRML_WGHT", {"keep_sharp": True}))

    return bot_obj


def create_manhole(settings) -> bpy.types.Object:
    manhole_bottom = create_manhole_bottom(settings)
    return manhole_bottom
