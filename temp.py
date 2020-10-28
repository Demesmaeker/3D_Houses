    densities = np.asarray(densities)
    density_colors = plt.get_cmap('viridis')(
        (densities - densities.min()) / (densities.max() - densities.min()))
    density_colors = density_colors[:, :3]
    density_mesh = o3d.geometry.TriangleMesh()
    density_mesh.vertices = poisson_mesh.vertices
    density_mesh.triangles = poisson_mesh.triangles
    density_mesh.triangle_normals = poisson_mesh.triangle_normals
    density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)

    vertices_to_remove = densities < np.quantile(densities, 0.01)
    density_mesh.remove_vertices_by_mask(vertices_to_remove)