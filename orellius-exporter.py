import bpy
import os

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

	fp.write("test")

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