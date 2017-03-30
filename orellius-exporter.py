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

class Face(object):

	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

class Vertex(object):

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Uv(object):

	def __init__(self, s, t):
		self.s = s
		self.t = t

class VertexData(object):
    
    def __init__(self, x, y, z, s, t):
        self.x = x
        self.y = y
        self.z = z
        self.s = s
        self.t = t

	def __eq__(self, other): 
        return self.__dict__ == other.__dict__

def checkIfVertexAlreadyExists(VBOData, vertex):

    for i,vert in enumerate(VBOData):
        if vert == vertex:
            return i
        
    return -1

def convertGeometryDataToVBOFormat(vertices, uvs, faces):

    VBOData = []
    indices = []
    sameVertecies = 0
    
    for i,face in enumerate(faces):
        
        vertexData = VertexData(vertices[face.a].x, vertices[face.a].y, vertices[face.a].z, uvs[i * 3].s, uvs[i * 3].t)
        index = checkIfVertexAlreadyExists(VBOData, vertexData)
        if index != -1:
            indices.append(index)
            sameVertecies += 1
        else:
            indices.append((i * 3) - sameVertecies)
            VBOData.append(vertexData)
        
        vertexData = VertexData(vertices[face.b].x, vertices[face.b].y, vertices[face.b].z, uvs[i * 3 + 1].s, uvs[i * 3 + 1].t)
        index = checkIfVertexAlreadyExists(VBOData, vertexData)
        if index != -1:
            indices.append(index)
            sameVertecies += 1
        else:
            indices.append((i * 3 + 1) - sameVertecies)
            VBOData.append(vertexData)
            
        vertexData = VertexData(vertices[face.c].x, vertices[face.c].y, vertices[face.c].z, uvs[i * 3 + 2].s, uvs[i * 3 + 2].t)
        index = checkIfVertexAlreadyExists(VBOData, vertexData)
        if index != -1:
            indices.append(index)
            sameVertecies += 1
        else:
            indices.append((i * 3 + 2) - sameVertecies)
            VBOData.append(vertexData)
    
    return [ VBOData, indices ] 

class ExportOrelliusMesh(bpy.types.Operator, ExportHelper):
	"""Export Orellius mesh"""

	bl_idname = "export_orellius.orl"
	bl_label = "Export Orellius Mesh"
	filename_ext = ".orl"

	def execute(self, context):
		return save(self, context, self.properties.filepath)

def save(operator, context, filepath):

	filepath = os.fsencode("/home/lazar/Desktop/test.orl")
	fp = open(filepath, 'w')

	for sceneObject in bpy.context.scene.objects:
		if sceneObject.type == "MESH":
			fp.write("mesh " + sceneObject.name + "\n")

			vertexList = []
			uvList = []
			faceList = []

			mesh = bmesh.new()
			mesh.from_mesh(sceneObject.data)
			bmesh.ops.triangulate(mesh, faces=mesh.faces[:], quad_method=0, ngon_method=0)
			mesh.to_mesh(sceneObject.data)

			for vertex in sceneObject.data.vertices:
				#fp.write("vertex " + str(vertex.co.x) + " " + str(vertex.co.y) + " " + str(vertex.co.z) + "\n")
				vertexObject = Vertex(vertex.co.x, vertex.co.y, vertex.co.z)
				vertexList.append(vertexObject)

			uv_layer = mesh.loops.layers.uv.active
			for face in mesh.faces:
				for vert in face.loops:
					#fp.write("uv1 " + str(vert[uv_layer].uv.x) + " " + str(vert[uv_layer].uv.y) + "\n")
					uvObject = Uv(vert[uv_layer].uv.x, vert[uv_layer].uv.y)
					uvList.append(uvObject)

			for face in sceneObject.data.polygons:
				#fp.write("face " + str(face.vertices[0]) + " " + str(face.vertices[1]) + " " + str(face.vertices[2]) + "\n")
				faceObject = Face(face.vertices[0], face.vertices[1], face.vertices[2])
				faceList.append(faceObject)

			[ VBO, indices ] = convertGeometryDataToVBOFormat(vertexList, uvList, faceList)
			
			for vboEntry in VBO:
				fp.write("v " + str(round(vboEntry.x, 2)) + " " + str(round(vboEntry.y, 2)) + " " + str(round(vboEntry.z, 2)) + " " + str(round(vboEntry.s, 3)) + " " + str(round(vboEntry.t, 3)) + "\n")
			
			fp.write("i ")
			for indice in indices:
				fp.write(str(indice) + " ")
			fp.write("\n")
			
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