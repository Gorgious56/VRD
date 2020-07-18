import bpy
from math import pi
from ...backend.factory import manhole_factory
from ...backend.data_tree import collection_operations


class CreateManholeOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = 'mesh.vrd_create_manhole'
    bl_label = 'Create Manhole'
    bl_description = 'Create Manhole'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}

    radius: bpy.props.FloatProperty(
        name="Radius",
        default=0.5,
        min=0,
        soft_max=0.5,
    )

    lod: bpy.props.IntProperty(
        name="Level Of Detail",
        default=8,
        min=0,
        soft_min=1,
        soft_max=16,
    )

    intake_diameter: bpy.props.EnumProperty(
        name="Intake Diameter",
        items=(
            ('150', "150", ""),
            ('160', "160", ""),
            ('200', "200", ""),
            ('250', "250", ""),
            ('315', "315", ""),
            ('400', "400", ""),
            ('500', "500", ""),
            ('600', "600", ""),
            ('800', "800", ""),
            ('1000', "1000", ""),
        ),
        default='315',
    )

    intake_angle: bpy.props.FloatProperty(
        name="Intake Angle",
        default=0,
        soft_min=-pi / 4,
        soft_max=pi / 4,
        min=-pi / 2,
        max=pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        step=100,
    )    
    
    outlet_angle: bpy.props.FloatProperty(
        name="Outlet Angle",
        default=0,
        soft_min=-pi / 4,
        soft_max=pi / 4,
        min=-pi / 2,
        max=pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        step=100,
    )

    def execute(self, context):
        obj = manhole_factory.create_manhole(self)

        def recursive_link(obj):
            collection_operations.link_object_to_collection(obj, context.scene.collection)
            for child in obj.children:
                recursive_link(child)

        recursive_link(obj)

        context.view_layer.objects.active = obj
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
