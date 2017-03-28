import bpy
import os
import bmesh

from bpy_extras.io_utils import ExportHelper

bl_info = {
	"name": "Orellius Format",
	"description": "Export mesh for Orellius web engine",
	"author": "Lazar Mitic",
	"version": (0, 1),
	"blender": (2, 78, 0),
	"location": "File > Import-Export",
	"category": "Import-Export"
}

class ExportOrelliusMesh(bpy.types.Operator, ExportHelper):
	"""Export Orellius mesh"""

	bl_idname = "export_orellius.orl"
	bl_label = "Export Orellius Mesh"
	filename_ext = ".orl"

	def execute(self, context):
		return save(self, context, self.properties.filepath)

def save(operator, context, filepath):

	filepath = os.fsencode(filepath)
	fp = open(filepath, 'w')

	for sceneObject in bpy.context.scene.objects:
		if sceneObject.type == "MESH":
			fp.write("mesh " + sceneObject.name + "\n")

			mesh = bmesh.new()
			mesh.from_mesh(sceneObject.data)
			bmesh.ops.triangulate(mesh, faces=mesh.faces[:], quad_method=0, ngon_method=0)
			mesh.to_mesh(sceneObject.data)

			for vertex in sceneObject.data.vertices:
				fp.write("vertex " + str(vertex.co.x) + " " + str(vertex.co.y) + " " + str(vertex.co.z) + "\n")

			uv_layer = mesh.loops.layers.uv.active
			for face in mesh.faces:
				for vert in face.loops:
					fp.write("uv1 " + str(vert[uv_layer].uv.x) + " " + str(vert[uv_layer].uv.y) + "\n")

			for face in sceneObject.data.polygons:
				fp.write("face " + str(face.vertices[0]) + " " + str(face.vertices[1]) + " " + str(face.vertices[2]) + "\n")

			for material in sceneObject.material_slots:
				for texture in material.material.texture_slots:
					if texture:
						if hasattr(texture.texture, "image"):
							fp.write("diffuseTexture " + texture.texture.image.filepath + "\n")

			mesh.free()

	fp.close()

	return { "FINISHED" }

def menu_func_export(self, context):
	self.layout.operator(ExportOrelliusMesh.bl_idname, text="Orellius Mesh (.orl)")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
	register()