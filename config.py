"""
Our configurations files, where we setup default values
as well as handy lists and dictionaries for efficency.
"""

from ursina import Vec3

six_cube_dirs = [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)
                ]