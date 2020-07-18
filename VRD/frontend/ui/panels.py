import bpy
from ..operators import object_generation
from ..operators import object_destruction


class VRDMainPanel(bpy.types.Panel):
    bl_idname = "VRD_PT_MainPanel"
    bl_label = "VRD"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VRD'

    def draw(self, context):
        layout = self.layout

        layout.operator(object_generation.CreateManholeOperator.bl_idname)
        layout.operator(object_destruction.RemoveObjectRecursivelyOperator.bl_idname)
