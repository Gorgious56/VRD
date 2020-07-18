import bpy
from ..operators import object_generation


class VRDMainPanel(bpy.types.Panel):
    bl_idname = "VRD_PT_MainPanel"
    bl_label = "VRD"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VRD'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        row = layout.row()
        row.operator(object_generation.CreateManholeOperator.bl_idname)
