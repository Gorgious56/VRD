import bpy


class RemoveObjectRecursivelyOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = 'mesh.vrd_remove_object'
    bl_label = 'Remove Object'
    bl_description = 'Remove Object'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.selected_objects

    def execute(self, context):
        def recursive_remove(obj):
            for child in obj.children:
                recursive_remove(child)
            bpy.data.objects.remove(obj, do_unlink=True)

        for obj in context.selected_objects:
            recursive_remove(obj)

        return {'FINISHED'}
