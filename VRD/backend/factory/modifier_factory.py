import bpy
from typing import Iterable


class ModSettings:
    def __init__(self, mod_type: str, mod_name: str, attributes: dict = None):
        self.mod_type = mod_type
        self.mod_name = mod_name
        self.attributes = attributes


def add_modifier(
        obj: bpy.types.Object,
        settings: ModSettings,
        replace: bool = True) -> None:
    if settings.mod_name in obj.modifiers and not replace:
        return
    new_mod = obj.modifiers.new(name=settings.mod_name, type=settings.mod_type)
    if settings.attributes:
        for attr, value in settings.attributes.items():
            if hasattr(new_mod, attr):
                setattr(new_mod, attr, value)
    new_mod.show_expanded = False


def add_modifiers(
        obj: bpy.types.Object,
        mods: Iterable[ModSettings],
        replace: bool = True) -> None:
    (add_modifier(obj, mod, replace) for mod in mods)
