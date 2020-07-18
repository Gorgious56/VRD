import bpy
from math import pi
from ...backend.factory import manhole_factory
from ...backend.data_tree import collection_operations


DIAMETERS = (
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
        )


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

    outlet_diameter: bpy.props.EnumProperty(
        name="Outlet Diameter",
        items=DIAMETERS,
        default='315',
    )

    inlets: bpy.props.IntProperty(
        name="Inlets Amount",
        default=1,
        soft_min=1,
        min=0,
        max=3,
    )

    inlet_1_angle: bpy.props.FloatProperty(
        name="Inlet 1 Angle",
        default=0,
        soft_min=-pi / 2,
        soft_max=pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        step=100,
    )

    inlet_1_diameter: bpy.props.EnumProperty(
        name="Inlet 1 Diameter",
        items=DIAMETERS,
        default='315',
    )

    inlet_2_angle: bpy.props.FloatProperty(
        name="Inlet 2 Angle",
        default=-pi / 4,
        soft_min=-pi / 2,
        soft_max=pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        step=100,
    )    
    
    inlet_2_diameter: bpy.props.EnumProperty(
        name="Inlet 2 Diameter",
        items=DIAMETERS,
        default='315',
    )

    inlet_3_angle: bpy.props.FloatProperty(
        name="Inlet 3 Angle",
        default=pi / 4,
        soft_min=-pi / 2,
        soft_max=pi / 2,
        subtype='ANGLE',
        unit='ROTATION',
        step=100,
    )    

    inlet_3_diameter: bpy.props.EnumProperty(
        name="Inlet 3 Diameter",
        items=DIAMETERS,
        default='315',
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        for i in reversed(range(self.inlets)):
            sub_box = box.box()
            row = sub_box.row()
            row.label(text=f"Inlet {i + 1}")
            row.prop_menu_enum(self, f"inlet_{i+1}_diameter", text="Diameter")
            row.prop(self, f"inlet_{i+1}_angle", text="Angle")
        box.prop(self, "inlets", slider=False)
        box.prop_menu_enum(self, "outlet_diameter")
        layout.prop(self, "lod")

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
