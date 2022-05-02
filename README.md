# Get Out of my Fucking Maze

This is a 2D top-down adventure game made for a high school project using as a base the open world of our previous game [**Barbarism**](https://github.com/Matimed/Barbarism).

## Controls

* Arrow keys to move.
* Return key to interact.


## How to install the game

### Requirements

* Python 3.10.0
* Python-pip.
* See the rest of depencies in the [requirements](requirements.txt) file.

## Unix

Execute [setup.sh](setup.sh) to install all dependencies needed to run the game.

Start the game by executing [GOFM.py](GOFM.py).


## Windows:

### To install all dependencies needed to run the game:

Run in shell: _$ pip install -r requirements.txt_ 

### To create an exe file:

1. Run in shell:   _$ pip install pyinstaller_ 

2. Go to the root of the proyect and execute:  _$ pyinstaller GOFM.py --onefile --noconsole_ 

3. Finally move the [GOFM.exe](dist/GOFM.exe) file from dist folder to the root folder.

## Custom maps:
You can use our [map-editor](https://github.com/Matimed/map-editor) tool to create custom dungeon layouts. Then to add them to the game, you just need to paste all the generated files in the [maps](assets/data/maps) folder and that's it! 

There will be a random chance that your dungeons will appear in the game.


## Authors

* **Arcos Juan** - [ArcosJuan](https://github.com/ArcosJuan).
* **Carazo Medley Matías** - [Matimed](https://github.com/Matimed).

## License

_GOFM as a whole is licensed under the MIT License - Look the [LICENSE](LICENSE) file for details._


