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
- Tiled collisions / hazards / saves / warps / collectables
- animated coins, must collect each coin to activate a warp
- shooting
- death / restart
- timer and death counter
- water object layer from Tiled
- dynamic sized room snapping
- trigger-> moving spikes

Planned / Experimental features:
- TODO: we need to be able to create spikes wherever we want instead of strictly 32x32 placement. 
  the plan is to remove the spike sprites from the ground tiles and put them into the Hazards object layer
- moving platforms
- wall jumps
- save files (also package assets better when building a .exe)
- parallax background layers
- camera follow player or follow with padding, for different type of level making

