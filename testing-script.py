import bpy
import bmesh

print("\n\n=== SCRIPT START ===")

for obj in bpy.context.scene.objects: 
	print(obj.name, obj, obj.type)
	if obj.type == 'MESH': 
		print(">>>>", obj.name)

		print("Materials")

		for material in obj.material_slots:
			print(material.material.name)

			print("Textures")

			for texture in material.material.texture_slots:
				print("#")
				if texture:
					if hasattr(texture.texture, "image"):
						print(texture.texture.image.filepath)

		print("\n")

		obj.update_from_editmode()

		mesh = bmesh.new()
		mesh.from_mesh(obj.data)

		bmesh.ops.triangulate(mesh, faces=mesh.faces[:], quad_method=0, ngon_method=0)

		mesh.to_mesh(obj.data)


		print(mesh)


		mesh.free()


		print("\nVERTICES:")

		for vert in obj.data.vertices:
			print("v: %f %f %f" % (vert.co.x, vert.co.y, vert.co.z))

		print("\nFACES:")

		for face in obj.data.polygons:
			print("f: %f %f %f" % (face.vertices[0], face.vertices[1], face.vertices[2]))

print("=== SCRIPT END =====")
