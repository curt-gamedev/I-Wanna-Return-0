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

Requires Python 3 and:

- pygame-ce
- PyTMX

Install dependencies:
pip install pygame-ce pytmx

Run:
python main.py

Current features:
- classic-style movement and double jump
- controller support
- room loading
- Tiled collisions / hazards / saves / warps / collectables
- animated coins, must collect each coin to activate a warp
- shooting
- death / restart
- timer and death counter

Planned / Experimental features:
- moving platforms
- wall jumps
- trigger traps
- save files (also package assets better)
- parallax background layers
- dynamic sized rooms
- camera follow player or camera snaps to next 'room' in a single tmx room

