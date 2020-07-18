import bpy
from . import modifier_factory as mod_fac
from . import object_factory as obj_fac


# vg = new_obj.vertex_groups.new("group name")
# vg.add([vertice index], weight, "ADD")


def create_cylinder(radius: float, height: float, lod: int, name: str, location=None, rotation=None, caps: bool = True, used_as_boolean: bool = False) -> bpy.types.Object:
    epsilon = 0.001
    caps_obj_bot = obj_fac.create_mesh_object(name=name + "_Caps_Bot", auto_smooth=True, vertices=((0, 0, 0),), used_as_boolean=True)

    for mod_settings in (
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_RADIUS",
            attributes={
                "axis": 'X',
                "screw_offset": radius,
                "steps": lod / 2,
                "render_steps": lod / 2,
                "angle": 0,
            },
        ),
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_CYLINDER",
            attributes={
                "steps": lod * 4,
                "render_steps": lod * 4,
                "use_merge_vertices": True,
            },
        ),
    ):
        mod_fac.add_modifier(caps_obj_bot, mod_settings)

    caps_obj_bot.location[2] -= epsilon

    caps_obj_top = obj_fac.create_mesh_object(name=name + "_Caps_Top", auto_smooth=True, vertices=((0, 0, 0),), used_as_boolean=True)

    for mod_settings in (
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_RADIUS",
            attributes={
                "axis": 'X',
                "screw_offset": radius,
                "steps": lod / 2,
                "render_steps": lod / 2,
                "angle": 0,
            },
        ),
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_CYLINDER",
            attributes={
                "steps": lod * 4,
                "render_steps": lod * 4,
                "use_merge_vertices": True,
                "use_normal_flip": True,
            },
        ),
        mod_fac.ModSettings(
            mod_type='DISPLACE',
            mod_name="VRD_CAPS_TOP",
            attributes={
                "mid_level": 0,
                "strength": height + epsilon,
                "direction": 'Z',
            },
        ),
    ):
        mod_fac.add_modifier(caps_obj_top, mod_settings)

    cyl_obj = obj_fac.create_mesh_object(name=name, auto_smooth=True, vertices=((0, 0, 0),), used_as_boolean=used_as_boolean)

    caps_obj_top.parent = cyl_obj
    caps_obj_bot.parent = cyl_obj

    for mod_settings in (
        mod_fac.ModSettings(
            mod_type='DISPLACE',
            mod_name="VRD_RADIUS",
            attributes={
                "direction": 'X',
                "mid_level": 0,
                "strength": radius,
            },
        ),
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_HEIGHT",
            attributes={
                "steps": lod,
                "render_steps": lod,
                "angle": 0,
                "screw_offset": height,
            },
        ),
        mod_fac.ModSettings(
            mod_type='SCREW',
            mod_name="VRD_CYLINDER",
            attributes={
                "steps": lod * 4,
                "render_steps": lod * 4,
                "use_merge_vertices": True
            },
        ),
        mod_fac.ModSettings(
            mod_type='BOOLEAN',
            mod_name="VRD_CAPS_BOT",
            attributes={
                "operation": 'UNION',
                "object": caps_obj_bot,
            },
        ),
        mod_fac.ModSettings(
            mod_type='BOOLEAN',
            mod_name="VRD_CAPS_TOP",
            attributes={
                "operation": 'UNION',
                "object": caps_obj_top,
            },
        ),
        mod_fac.ModSettings(
            mod_type='WELD',
            mod_name="VRD_CAPS_WELD",
            attributes={
                "merge_threshold": 2 * epsilon,
            },
        ),
    ):
        mod_fac.add_modifier(cyl_obj, mod_settings)

    if location:
        cyl_obj.location = location
    if rotation:
        cyl_obj.rotation_euler = rotation

    return cyl_obj
