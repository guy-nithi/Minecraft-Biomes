from ursina import *
from ursina import vec3
from perlin import Perlin
from random import random
from swirl_engine import SwirlEngine
from mining_system import *

class MeshTerrain:
    def __init__(self):

        self.block = load_model('block.obj')
        self.textureAtlas = 'texture_atlas_3.png'
        self.numVertices = len(self.block.vertices)
        
        self.subsets = []
        self.numSubsets = 128

        # Must be even number! See genTerrain()
        self.subWidth = 4
        self.swirlEngine = SwirlEngine(self.subWidth)
        self.currentSubset = 0

        # Our terrain dicionary :D
        self.td = {}

        # Our vertex dictionary -- for mining
        self.vd = {}

        self.perlin = Perlin()

        for i in range(0,self.numSubsets):
            e = Entity( model=Mesh(),
                        texture=self.textureAtlas)
            e.texture_scale*=64/e.texture.width
            self.subsets.append(e)

    # Highlight looked-at block :)
    def update(self,pos,cam):
        highlight(pos,cam,self.td)

    def input(self,key):
        if key=='left mouse up' and bte.visible==True:
            epi = mine(self.td,self.vd,self.subsets)
            if epi != None:
                self.genWalls(epi[0],epi[1])
                self.subsets[epi[1]].model.generate()

    # I.e. after mining, to create illusion of depth.
    def genWalls(self,epi,subset):
        if epi==None: return
        # Refactor self -- place in mining system
        # except for call to genBlock?
        wp =    [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)]
        for i in range(0,6):
            np = epi +wp[i]
            if self.td.get( 'x'+str(floor(np.x))+
                            'y'+str(floor(np.y))+
                            'z'+str(floor(np.z)))==None:
                self.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')
        
    def genBlock(self,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset==-1: subset=self.currentSubset
        # Extend or add to the vertices of our model.
        model = self.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                self.block.vertices])


        self.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t"
        # Also, record gap above self position to
        # correct for spawning walls after mining.
        if gap==True:
            key =   ("x"+str(floor(x))+
                    "y"+str(floor(y+1))+
                    "z"+str(floor(z)))
            if self.td.get(key)==None:
                self.td[key] = "g"


        # Record subset index and first vertex of self block.
        vob = (subset, len(model.vertices)-37)
        self.vd["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = vob

        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                self.numVertices)

        # self is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        if blockType=='soil':
            uu = 10
            uv = 7
        elif blockType=='stone':
            uu = 8
            uv = 5
        elif blockType=='ice':
            uu = 9
            uv = 7
            # Randomly place stone blocks.
        if random() > 0.86:
            uu = 8
            uv = 5
        # If high enough, cap with snow blocks :D
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in self.block.uvs])

    def genTerrain(self):
        # Get current position as we swirl around world.
        x = floor(self.swirlEngine.pos.x)
        z = floor(self.swirlEngine.pos.y)

        d = int(self.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(self.perlin.getHeight(x+k,z+j))
                if self.td.get( "x"+str(floor(x+k))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z+j)))==None:
                    self.genBlock(x+k,y,z+j,blockType='ice')

        self.subsets[self.currentSubset].model.generate()
        # Current subset hack ;)
        if self.currentSubset<self.numSubsets-1:
            self.currentSubset+=1
        else: self.currentSubset=0
        # self.currentSubset+=1
        self.swirlEngine.move()