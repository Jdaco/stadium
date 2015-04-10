#!/usr/bin/python2
import argparse
from stadium import mappers
from stadium.domain import ROMBuffer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--import',
                        type=argparse.FileType('r'),
                        dest="imported",
                        help="JSON file containing rental information")
    parser.add_argument('-e', '--export',
                        type=argparse.FileType('w'),
                        dest="exported",
                        help="JSON file to export ROM info to")
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('wb'),
                        help="Write modified rom into new file")
    parser.add_argument('rom',
                        type=argparse.FileType('rb'),
                        help="Pokemon Stadium 2 ROM file to read from")
    args = parser.parse_args()
    
    rom = ROMBuffer(args.rom)
    args.rom.close()
    if args.imported:
        mappers.json.load(args.imported, rom)
        args.imported.close()
    if args.exported:
        mappers.json.dump(args.exported, rom)
        args.exported.close()
    if args.output:
        rom.write(args.output)
        args.output.close()
    if not args.output and not args.exported:
        import stadium.main
        import urwid
        palette = [
            ("item", '', '', '', 'g75', 'g4'),
            ("item_active", '', '', '', 'dark red', 'g4'),
            ("item_focus", '', '', '', 'g90', 'g15'),
            ("title", '', '', '', 'dark magenta', 'g4'),
            ("progress", '', '', '', 'g4', 'g4'),
            ("progress_red", '', '', '', 'dark red', 'dark red'),
            ("progress_blue", '', '', '', 'dark blue', 'dark blue'),
            ("progress_cyan", '', '', '', 'dark cyan', 'dark cyan'),
            ("base", '', '', '', 'g75', 'g4'),
            ("buffername", '', '', '', 'dark red', 'g4'),
            ]
        frame = stadium.main.MainWidget(rom)
        loop = urwid.MainLoop(frame, palette)
        loop.screen.set_terminal_properties(colors=256)
        loop.run()
