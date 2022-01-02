from random import randrange
from ursina import *
from perlin import Perlin

class MeshTerrain:
    def __init__(self):
        
        self.block = load_model('block.obj')
        self.textureAtlas = 'texture_atlas_3.png'

        self.subsets = []
        self.numSubsets = 1
        self.subWidth = 128

        self.td = {}

        self.perlin = Perlin()

        for i in range(0,self.numSubsets):
            e = Entity( model=Mesh(),
                        texture=self.textureAtlas)
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)
        

    def genBlock(self,x,y,z):
        # Extend or add to the vertices of our model.
        model = self.subsets[0].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                self.block.vertices])

        self.td['x'+str(floor(x))+
                'y'+str(floor(y))+
                'z'+str(floor(z))] = 't'

        # self is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        # Snow? High enough?
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])


    def genTerrain(self):
        x = 0
        z = 0
        d = int(self.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                # y = randrange(-1,1)
                y = floor(self.perlin.getHeight(x+k,z+j))
                self.genBlock(x+k,y,z+j)

        self.subsets[0].model.generate()