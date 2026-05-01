import bpy
import bmesh
import random
from bmesh.types import BMFace, BMesh, BMVert
from bpy.types import Object
from mathutils import Vector

class Flatana:

    @classmethod
    def flatten(cls, obj: Object, mode: str = 'AVERAGED', iterations: int = 100, strength: float = 0.3,
                only_selected_faces: bool = False) -> None:
        # flatten
        if obj and obj.type == 'MESH':
            obj_mode = obj.mode
            if obj.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            if mode == 'SEQUENTIAL':
                cls._flatten_sequential(
                    bm=bm,
                    iterations=iterations,
                    strength=strength,
                    only_selected_faces=only_selected_faces,
                )
            elif mode == 'AVERAGED':
                cls._flatten_averaged(
                    bm=bm,
                    iterations=iterations,
                    strength=strength,
                    only_selected_faces=only_selected_faces,
                )
            bm.to_mesh(obj.data)
            bm.free()
            bpy.ops.object.mode_set(mode=obj_mode)

    @staticmethod
    def _face_plane(face: BMFace) -> tuple[Vector, Vector]:
        """Unit normal and a point on the face plane (median center)."""
        n = face.normal.copy()
        if n.length_squared < 1e-20:
            return Vector((0.0, 0.0, 1.0)), face.calc_center_median()
        n.normalize()
        return n, face.calc_center_median()

    @staticmethod
    def _project_point_on_plane(p: Vector, plane_normal: Vector, plane_point: Vector) -> Vector:
        """Orthogonal projection of p onto the plane (plane_normal, plane_point)."""
        d = (p - plane_point).dot(plane_normal)
        return p - d * plane_normal

    @classmethod
    def _flatten_averaged(cls, bm: BMesh, iterations: int = 100, strength: float = 0.3,
                          only_selected_faces: bool = False, min_face_area: float = 1e-12,) -> None:
        """
        Each iteration: for every face, each of its vertices gets a target on
        that face's plane. Vertex positions are updated by strength * average
        of all targets from incident faces.
        """
        faces = [_face for _face in bm.faces if not only_selected_faces or _face.select]

        for _ in range(iterations):
            bm.normal_update()

            deltas: dict[BMVert, Vector] = {v: Vector() for v in bm.verts}
            counts: dict[BMVert, int] = {v: 0 for v in bm.verts}

            for face in faces:
                if face.calc_area() < min_face_area:
                    continue
                n, c = cls._face_plane(face=face)
                for v in face.verts:
                    target = cls._project_point_on_plane(p=v.co, plane_normal=n, plane_point=c)
                    deltas[v] += target - v.co
                    counts[v] += 1

            for v in bm.verts:
                k = counts[v]
                if k:
                    v.co += strength * (deltas[v] / k)
    @classmethod
    def _flatten_sequential(cls, bm: BMesh, iterations: int = 50, strength: float = 0.15,
                            only_selected_faces: bool = False, shuffle_faces: bool = True,
                            min_face_area: float = 1e-12 ) -> None:
        """
        Each iteration: visit each face once (optionally shuffled) and move
        only that face's vertices a fraction of the way toward its plane.
        Closer to "one face at a time"; use lower strength than averaged mode.
        """
        faces = [_face for _face in bm.faces if not only_selected_faces or _face.select]

        for _ in range(iterations):
            bm.normal_update()
            order = list(faces)
            if shuffle_faces:
                random.shuffle(order)

            for face in order:
                if face.calc_area() < min_face_area:
                    continue
                n, c = cls._face_plane(face=face)
                for v in face.verts:
                    target = cls._project_point_on_plane(p=v.co, plane_normal=n, plane_point=c)
                    v.co += strength * (target - v.co)
