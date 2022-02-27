from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap,loadMap

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.height=1.86
subject.frog=False # For jumping
subject.runSpeed = 10
subject.walkSpeed = 4
camera.dash=10 # Rate at which fov changes when running.
window.fullscreen=False

terrain = MeshTerrain(subject,camera)
# snowfall = SnowFall(subject)
# How do you at atmospheric fog
scene.fog_density=(0,75)
# scene.fog_color=indra.color
scene.fog_color=color.white
generatingTerrain=False

for i in range(64):
    terrain.genTerrain()

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

def input(key):
    global generatingTerrain
    terrain.input(key)
    if key=='g':
        generatingTerrain = not generatingTerrain
    # Jumping...
    if key == 'space': subject.frog=True
    # Changing dash speed
    if subject.runSpeed < 30:
        if key == 'u': 
            subject.runSpeed += 5
    else:
        subject.runSpeed = 30

    if subject.runSpeed > 4:
        if key == 'p': 
            subject.runSpeed -= 5
    else:
        subject.runSpeed = 4
    # Saving and loading...
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)

count = 0
def update():
    global count, pX, pZ

    # Highlight terrain block for mining/building...
    terrain.update(subject.position,camera)

    # Handle mob ai.
    mob_movement(Greninja028, subject.position, terrain.td)
    if subject.y < -50:
        subject.y = 100

    count+=1
    if count == 4:

        count = 0

        # Generate terrain at current swirl position.
        if generatingTerrain:
            for i in range(4):
                terrain.genTerrain()


    # Change subset position based on subject position.
    if abs(subject.x - pX)>4 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=ra.random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=ra.random()+0.7
            grass_audio.play()

    # Walk on solid terrain, and check wall collisions.
    bumpWall(subject, terrain)
    # Running and Dashing Effect.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        if camera.fov>90:
            camera.fov-= camera.dash*4*time.dt
            if camera.fov<90: camera.fov = 90

from mob_system import *

app.run()