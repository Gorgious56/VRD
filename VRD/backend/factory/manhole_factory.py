import bpy
from math import pi
from . import primitive_factory as prim_fac
from . import modifier_factory as mod_fac


def create_manhole_bottom(settings) -> bpy.types.Mesh:
    bot_height = 0.61
    bot_thickness = 0.1
    bot_bot_thickness = 0.25

    bot_obj_bool_main = prim_fac.create_cylinder(
        radius=settings.radius - bot_thickness,
        height=bot_height,
        lod=settings.lod,
        name="Manhole_Bottom_Bool_Main",
        location=(0, 0, bot_bot_thickness),
        used_as_boolean=True)

    bot_obj_bool_top = prim_fac.create_cylinder(
        radius=settings.radius - bot_thickness / 2,
        height=bot_height,
        lod=settings.lod,
        name="Manhole_Bottom_Bool_Top",
        location=(0, 0, bot_height - bot_thickness / 2),
        used_as_boolean=True)

    intake_radius = int(settings.intake_diameter) / 2000
    bot_obj_bool_intake = prim_fac.create_cylinder(
        radius=intake_radius,
        height=settings.radius * 2,
        lod=settings.lod / 1.5,
        name="Manhole_Bottom_Bool_Intake",
        location=(0, 0, bot_bot_thickness),
        rotation=(.001, - pi / 2, settings.intake_angle),
        used_as_boolean=True)

    bot_obj_bool_outlet = prim_fac.create_cylinder(
        radius=intake_radius,
        height=settings.radius * 2,
        lod=settings.lod / 1.5,
        name="Manhole_Bottom_Bool_Outlet",
        location=(0, 0, bot_bot_thickness),
        rotation=(.001, pi / 2, settings.outlet_angle),
        used_as_boolean=True)

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
            # "use_clamp_overlap": False,
            # "harden_normals": True
        }))

    for boolean in (bot_obj_bool_intake, bot_obj_bool_outlet):
        boolean.parent = bot_obj
        mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('BOOLEAN', 'VRD_BOOL_MAIN', {"object": boolean}))

    mod_fac.add_modifier(bot_obj, mod_fac.ModSettings('WEIGHTED_NORMAL', "VRD_NRML_WGHT", {"keep_sharp": True}))

    return bot_obj


def create_manhole(settings) -> bpy.types.Object:
    manhole_bottom = create_manhole_bottom(settings)
    return manhole_bottom
