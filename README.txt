I Wanna Return 0

This is a small pygame-ce fangame project / learning framework, intended to learn and practise python programming and level design using Tiled. Game mechanics are based off classic "I wanna be the guy" fangames with the physics as close as possible to the Yuuutu engine.

Built with:
- pygame-ce
- PyTMX
- Tiled

Controls

Keyboard:
- Move: A/D or Arrow Keys
- Jump / Double Jump: Z or Space
- Shoot: X
- Restart: R

Controller:
- Move: Left Stick / D-Pad
- Jump / Double Jump: A / Cross 
- Shoot: X / Square
- Restart: Y / Triangle

## Running from Source

Requires: 
Python3, pygame-ce, PyTMX(for reading the .tmx files)
(Tiled for level editing, not required to run the game)

Install dependencies:
pip install pygame-ce pytmx

Run:
python main.py

Current features:
- controller support
- room loading
- Tiled collisions / hazards / saves / warps / collectables, etc. each on their own object layer.
- animated coins, must collect each coin to activate a warp
- shooting, moving platforms
- timer and death counter
- water object layer from Tiled
- dynamic sized room snapping
- trigger-> moving spikes
- F3 debug mode (includes mouse click to teleport player to anywhere on screen)
- resizeable/maximised window
- in map properties in tiled make string for camera_mode - horizontal_follow or leave blank for single rooms . room snapping
  (each room must be 800x608)

Planned / Experimental features (TODO LIST):
- parallax background layers 
    (under construction)
- wall jumps (been avoiding this due to never being a huge fan of iwbtg style wall jumps, 
    and still traumatized from previous player movement programming but i will eventually try to get this in)
- save files 
    (also perhaps we can package assets better when building a .exe)
- simple boss fight. 
    try to implement object pooling code from the unity project and shmup style bullet patterns    
- button remapping for controller/keyboard maybe? 
    (maybe build its own reusable script? or try find an open source one already made?)
- main menu and pause menu

