import bpy


def create_empty(name: str):
    empty = bpy.data.objects.new( "empty", None )

    return empty


def create_mesh_object(name: str, auto_smooth: bool = True, vertices=None, edges=None, faces=None, used_as_boolean: bool = False) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)

    if not vertices:
        vertices = []
    if not edges:
        edges = []
    if not faces:
        faces = []
    mesh.from_pydata(vertices, edges, faces)
    mesh.use_auto_smooth = auto_smooth

    obj = bpy.data.objects.new(mesh.name, mesh)
    if used_as_boolean:
        make_visibility_boolean(obj)

    return obj


def make_visibility_boolean(obj: bpy.types.Object, show_viewport: bool = False) -> None:
    obj.display_type = 'BOUNDS'
    obj.hide_render = True
    obj.hide_viewport = not show_viewport
    obj.cycles_visibility.camera = False
    obj.cycles_visibility.transmission = False
    obj.cycles_visibility.scatter = False
    obj.cycles_visibility.diffuse = False
    obj.cycles_visibility.shadow = False
    obj.cycles_visibility.glossy = False
