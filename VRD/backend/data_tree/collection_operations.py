import bpy
from typing import Iterable


def link_object_to_collection(
        obj: bpy.types.Object,
        new_col: bpy.types.Collection,
        unlink_from_existing: bool = True) -> None:
    if unlink_from_existing:
        for col in obj.users_collection:
            col.objects.unlink(obj)
    if obj.name not in new_col.objects:
        new_col.objects.link(obj)


def link_objects_to_collection(
        objects: Iterable[bpy.types.Object],
        new_col: bpy.types.Collection,
        unlink_from_existing: bool = True) -> None:
    for obj in (obj for obj in objects if obj):
        link_object_to_collection(obj, new_col, unlink_from_existing)
