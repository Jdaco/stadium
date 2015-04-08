#Stadium
A tool for modifying the rental set of Pokemon Stadium 2 N64 ROMs

##Usage
    $ ./stadium.py -h
    usage: stadium.py [-h] [-i IMPORTED] [-e EXPORTED] [-o OUTPUT] rom

    positional arguments:
        rom                   Pokemon Stadium 2 ROM file to read from

    optional arguments:
      -h, --help            show this help message and exit
      -i IMPORTED, --import IMPORTED
                        JSON file containing rental information
      -e EXPORTED, --export EXPORTED
                        JSON file to export ROM info to
      -o OUTPUT, --output OUTPUT
                        Write modified rom into new file
If the -o or -e flags are specified, the program exits after writing the file

##Keys
 - `:` - Ex mode
 - `esc` - Cancel command
 - `enter` - Submit Command
 - `j` - Scroll down
 - `k` - Scroll up
 - `J` - Page down
 - `K` - Page up
 - `g` - Top of list
 - `G` - Bottom of list
 - `/` - Search column
 - `?` - Search backwards
 - `n` - Next match
 - `N` - Previous match
 - `l` - Next column
 - `h` - Previous column
 - `>` - Increment meter
 - `<` - Decrement meter
 - `enter` - Set value (species, meter, move)

##Commands
 - `wq` - Write to current file and quit
 - `quit[!]` - Quit the program (add `!` to discard changes) 
 - `edit[!] filename` - Edit anothe rom file (add `!` to discard changes)
 - `write [filename]` - Write to the current file (or optional filename)
 - `import [filename]` - import data from json file
 - `export [filename]` - export data to json file
 - `max[!]` - Max out all meters for the current pokemon (add `!` to overwrite Hidden Power type)
 - `maxall[!]` - Max out all meters for everypokemon (add `!` to overwrite Hidden Power type)
