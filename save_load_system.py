"""
Saving and Loading a terrain 'map'
"""

def saveMap(_subPos, _td):
    import os, sys, pickle

    # Open main module directiory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('terrain_map_1.panda', 'wb') as f:

        mapdata=[_subPos,_td]

        pickle.dump(mapdata, f)
        mapdata.clear()

def loadMap(_subject,_terrain):
    import os, sys, pickle, copy
    from ursina import destroy

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('terrain_map_1.panda','rb') as f:
        map_data = pickle.load(f)

        # Empty out current terrain objects.
        for s in _terrain.subsets:
            destroy(s)
        _terrain.td={}
        _terrain.vd={}
        _terrain.subsets=[]
        _terrain.setup_subsets()
        _terrain.currentSubset=1
        # Without copy?
        _terrain.td=map_data[1]
        # _terrain.td=copy.copy(map_data[1])
        # Iterate over terrain dictionary and
        # if we find 't' then generate a block.
        # Note this means we'll lose colour info etc.
        i = 0 # Which subset to build block on?
        for key in _terrain.td:
            if _terrain.td.get(key)=='t':
                x = key[0]
                y = key[1]
                z = key[2]
                if i>=len(_terrain.subsets)-1:
                    i=0
                _terrain.genBlock(x,y,z,subset=i,gap=False,blockType='grass')
                i+=1

        # Reset swirl engine.
        _terrain.swirlEngine.reset(     _subject.position.x,
                                        _subject.position.z)
        # Regenerate subset models, so that we can see terrain
        for s in _terrain.subsets:
            s.model.generate()
        # # And reposition subject according to saved map
        # _subject.position=copy.copy(map_data[0])