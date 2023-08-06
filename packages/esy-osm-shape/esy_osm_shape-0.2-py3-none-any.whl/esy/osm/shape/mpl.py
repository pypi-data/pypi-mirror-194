import shapely
import matplotlib.collections
from matplotlib.path import Path


def empty_style():
    empty = {}
    while True:
        yield empty


def render(shapes, path_patch_options=None, point_radius=0.0001):
    if path_patch_options is None:
        path_patch_options = empty_style()
    pathpatches = []
    for shape, path_patch_option in zip(shapes, path_patch_options):
        if type(shape) is shapely.geometry.LineString:
            pathpatches.append(matplotlib.patches.PathPatch(
                matplotlib.path.Path(list(shape.coords), closed=False),
                **{'fill': False, **path_patch_option},
            ))
        elif type(shape) is shapely.geometry.LinearRing:
            pathpatches.append(matplotlib.patches.PathPatch(
                matplotlib.path.Path(list(shape.coords), closed=True),
                **{'fill': False, **path_patch_option},
            ))
        elif type(shape) is shapely.geometry.Polygon:
            vertices = list(shape.exterior.coords)
            codes = (
                [Path.MOVETO] +
                [Path.LINETO] * (len(vertices) - 2) +
                [Path.CLOSEPOLY]
            )

            for ring in shape.interiors:
                ring_vertices = list(ring.coords)
                ring_codes = (
                    [Path.MOVETO] +
                    [Path.LINETO] * (len(ring_vertices) - 2) +
                    [Path.CLOSEPOLY]
                )
                vertices += ring_vertices
                codes += ring_codes
            pathpatches.append(matplotlib.patches.PathPatch(
                matplotlib.path.Path(vertices, codes, closed=True),
                **{'fill': True, **path_patch_option},
            ))
        elif type(shape) is shapely.geometry.MultiPolygon:
            for shape in shape.geoms:
                vertices = list(shape.exterior.coords)
                codes = (
                    [Path.MOVETO] +
                    [Path.LINETO] * (len(vertices) - 2) +
                    [Path.CLOSEPOLY]
                )

                for ring in shape.interiors:
                    ring_vertices = list(ring.coords)
                    ring_codes = (
                        [Path.MOVETO] +
                        [Path.LINETO] * (len(ring_vertices) - 2) +
                        [Path.CLOSEPOLY]
                    )
                    vertices += ring_vertices
                    codes += ring_codes
                pathpatches.append(matplotlib.patches.PathPatch(
                    matplotlib.path.Path(vertices, codes, closed=True),
                    **{'fill': True, **path_patch_option},
                ))
        elif type(shape) is shapely.geometry.Point:
            pathpatches.append(matplotlib.patches.PathPatch(
                matplotlib.path.Path.circle(
                    center=(shape.x, shape.y), radius=point_radius
                ),
                **{'edgecolor': 'none', **path_patch_option},
            ))
        else:
            raise ValueError('Unsupported shape type {}'.format(shape))

    return pathpatches


def patches(shapes, path_patch_options=None):
    return matplotlib.collections.PatchCollection(
        render(shapes, path_patch_options), match_original=True
    )
