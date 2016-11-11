from itertools import izip
from functools import partial
import urwid
import ui
import maps
from domain import ROMFile
import urwidgets
import utility
import mappers


class SearchController(object):
    def __init__(self):
        self.last_search = None
        self.last_search_direction = None

    def inc_search(self):
        pass

class FileController(object):
    def __init__(self):
        pass

    def edit_file(self):
        pass

    def write(self):
        pass

    def import_json(self):
        pass

    def export_json(self):
        pass


class PokemonWidget(urwid.Text):
    def __init__(self, pokemon):
        self._pokemon = pokemon

        super(PokemonWidget, self).__init__(pokemon.species.capitalize())

    @property
    def pokemon(self):
        return self._pokemon

    @pokemon.setter
    def pokemon(self, pokemon):
        self._pokemon = pokemon
        self.set_text(pokemon.species.capitalize())




class MoveWidget(urwid.Text):
    def __init__(self, move):
        self._move = move

        super(MoveWidget, self).__init__( self._get_move_text() )

    @property
    def move(self):
        return self._move

    @move.setter
    def move(self, move):
        self._move = move
        self.set_text( self._get_move_text() )

    def _get_move_text(self):
        return utility.capitalize_move(
            str(move)
        ) if move else '-----'

class MainWidgetController(object):
    def __init__(self, widget, rom_file):
        self._widget = widget
        self._file = rom_file

        self.current_json = None

        self.pokemon = tuple(self._file.buffer.pokemon)

        self.moves = sorted([
            key
            for key, value in
            maps.moves.iteritems()
        ])

    def check_meter_value(self, func):
        def inner(value_string):
            try:
                value = int(value_string)
            except ValueError:
                self._widget.change_status("Invalid Value")
            else:
                func(value)
        return inner

    def enter_species(self):
        self._widget.start_editing(
            caption="Species: ",
            callback=self.set_species,
            completion_set = maps.pokemon.keys(),
        )

    def set_species(self, species):
        poke = self._widget.current_pokemon
        species = species.lower()
        if species in maps.pokemon:
            poke.species = species
            self._widget.updateLeftColumn()
            self._widget.updateCenterColumn()
        else:
            self._widget.change_status('Pokemon not recognized')
        
    def enter_move(self, move):
        self._widget.start_editing(
            caption="Move: ",
            callback = partial(
                self.set_move,
                move=move,
            ),
            completion_set=maps.moves,
        )

    def set_move(self, move, value):
        if move.lower() in maps.moves:
            move.set(move)
            self._widget.updateCenterColumn()
        else:
            self._widget.change_status("Move not found")

    @property
    def current_pokemon(self):
        pass

    def delete_move(self, move):
        move.set(None)
        self._widget.updateCenterColumn()

    def set_hidden_power(self, value):
        poke = self._widget.current_pokemon
        if value in maps.hidden_power:
            poke.hiddenPowerType = value
            self._widget.updateCenterColumn()
        else:
            self._widget.change_status('Invalid type')

    def edit_file(self, fname, discard=False):
        if self._file.dirty and not discard:
            self._widgetchange_status('No write since last change (add ! to override)')
        elif not path.local(fname).exists():
            self._widget.change_status('File not found')
        else:
            self._file = ROMFile(fname)
            self.pokemon = tuple(self._file.buffer.pokemon)
            self._widget.updateLeftColumn()
            self._widget.updateCenterColumn()
            self._widget.filename = fname

    def quit(self, discard=False):
        if self._file.dirty and not discard:
            self._widget.change_status('No write since last change (add ! to override)')
        else:
            self._widget.quit()

    def write(self, fname=None):
        self._file.write(fname)

    def import_json(self, fname):
        try:
            with open(fname, 'r') as fp:
                mappers.json.load(fp, self._file.buffer)
        except IOError:
            self._widget.change_status('File not found')
        else:
            self.current_json = fname
            self.updateCenterColumn()
            self.updateLeftColumn()

    def export_json(self, fname=None):
        if not fname:
            if self.current_json:
                fname = self.current_json
            else:
                self._change_status("Not a valid file name")
        else:
            with open(fname, 'w') as fp:
                mappers.json.dump(fp, self.rom_file.buffer)

    def inc_search(self):
        current_list = self.columns.focus
        current_pos = current_list.focus_position if start is None else start
        predicate = (lambda x: query.strip() != '' and query.lower() in x.text.lower())
        index = current_list.find(
            predicate,
            start=current_pos,
            direction=direction
        )
        if index == -1:
            current_list.set_focus(start)
        else:
            current_list.set_focus(index)

    def search(self):
        if query.strip() != '':
            self.last_search = query
            self.last_search_direction = direction
            current_list = self.columns.focus
            current_pos = current_list.focus_position if start is None else start
            predicate = (lambda x: query.lower() in x.text.lower())
            index = current_list.find(
                predicate,
                start=current_pos,
                direction=direction
            )
            if index == -1:
                self.change_status('%s Not Found.' % query)
            else:
                current_list.set_focus(index)

    def searchNext(self):
        if self.last_search:
            self.search(self.last_search, direction=self.last_search_direction)

    def searchPrev(self):
        if self.last_search:
            last_search = self.last_search_direction
            _direction = 'forward' if self.last_search_direction == 'backward' else 'backward'
            self.search(self.last_search, direction=_direction)
            self.last_search_direction = last_search


    def start_searching(current_list, direction):
        # handles keypresses
        def handler(widget, text):
            self.inc_search(text, start=current_pos, direction=direction)


        # for submitting
        def exit_handler(text):
            stop_searching()
            self.search(text, start=current_pos, direction=direction)

        #cleans up after a backspace cancel
        #this should be removed in favor of events
        def backspace_handler():
            if self.command_line.edit_text == '':
                stop_searching()
        # for canceling
        def stop_searching():
            current_list.focus.attrmap = {None: 'item'}
            urwid.disconnect_signal(self.command_line, 'change', handler)
            current_list.set_focus(current_pos)

        current_pos = current_list.focus_position
        current_list.body[current_pos].attrmap = {None: 'item_focus'}


        urwid.connect_signal(self.command_line, 'change', handler)
        self.command_line.keymap['esc'] = utility.chain(
            stop_searching,
            self.command_line.keymap['esc']
        )
        self.command_line.keymap['backspace'] = utility.chain(
            backspace_handler,
            self.command_line.keymap['backspace'],
        )


        caption = '/' if direction == 'forward' else '?'
        self._widget.start_editing(caption=caption, callback=exit_handler)

    def max_pokemon(pokemon, overwrite):
        h_type = pokemon.hiddenPowerType
        pokemon.max()

        if not overwrite and 'hidden power' in pokemon.moves:
            pokemon.hiddenPowerType = h_type

        self._widget.updateCenterColumn()

    def max_all_pokemon(self, overwrite=False):
        if not overwrite:
            for pokemon in self.pokemon:
                h_type = pokemon.hiddenPowerType
                pokemon.max()
                if 'hidden power' in pokemon.moves:
                    pokemon.hiddenPowerType = h_type
        else:
            for pokemon in self.pokemon:
                pokemon.max()
            
        self._widget.updateCenterColumn()

    def set_attack_dv(self, value):
        self._widget.current_pokemon.attackDv = value
        self._widget.updateHpDv()
        self._widget.update_stats()

    def set_defense_dv(self, value):
        self._widget.current_pokemon.defenseDv = value
        self._widget.updateHpDv()
        self._widget.update_stats()

    def set_speed_dv(self, value):
        self._widget.current_pokemon.speedDv = value
        self._widget.updateHpDv()
        self._widget.update_stats()

    def set_special_dv(self, value):
        self._widget.current_pokemon.specialDv = value
        self._widget.updateHpDv()
        self._widget.update_stats()

    def set_special_exp(self, value):
        self._widget.current_pokemon.specialExp = value
        self._widget.update_stats()

    def set_speed_exp(self, value):
        self._widget.current_pokemon.speedExp = value
        self._widget.update_stats()

    def set_defense_exp(self, value):
        self._widget.current_pokemon.defenseExp = value
        self._widget.update_stats()

    def set_hp_exp(self, value):
        self._widget.current_pokemon.hpExp = value
        self._widget.update_stats()

    def set_attack_exp(self, value):
        self._widget.current_pokemon.attackExp = value
        self._widget.update_stats()

    def set_happiness(self, happiness):
        poke = self._widget.currentPokemon
        poke.happiness = happiness

    def set_level(self, value):
        self._widget.current_pokemon.level = value
        self._widget.update_stats()


class MainWidget(urwidgets.CommandFrame):
    def __init__(self, rom_file):
        self.controller = MainWidgetController(self, rom_file)

        commands = {
            'w': self.controller.write,
            'q': self.controller.quit,
            'q!': partial(self.controller.quit, discard=True),
            'wq': utility.chain(self.controller.write, self.controller.quit),
            'quit': self.controller.quit,
            'quit!': partial(self.controller.quit, discard=True),
            'edit': self.edit_file, #Check this
            'edit!': partial(self.edit_file, discard=True), #Check this
            'write': self.controller.write,
            'import': self.controller.import_json,
            'export': self.controller.export_json,
            'max': self._max_pokemon,
            'max!': partial(self._max_pokemon, overwrite=True), 
            'maxall': self.controller.max_all_pokemon,
            'maxall!': partial(self.controller.max_all_pokemon, overwrite=True),
        }


        # --- Create Widgets ---
        self.pokemonWidgets = [
            urwidgets.MappedWrap(
                PokemonWidget(poke)
                attrmap='item', 
                focusmap='item_focus',
                keymap={'enter': self.controller.enter_species}
            )
            for poke in self.controller.pokemon
        ]
        self.pokeList = urwidgets.MappedList(
            urwid.SimpleFocusListWalker(self.pokemonWidgets),
        )
        urwid.connect_signal(self.pokeList, 'shift', self.updateCenterColumn)

        self.moveWidgets = [
            urwidgets.MappedWrap(
                MoveWidget(move)
                attrmap='item',
                focusmap='item_focus'
            )
            for move in self.controller.moves
        ]
        self.moveList = urwidgets.MappedList(
            urwid.SimpleFocusListWalker(self.moveWidgets)
        )

        current_move_widgets = [
            urwidgets.MappedWrap(
                MoveWidget(move),
                attrmap='item',
                focusmap='item_focus',
            )
            for move in self.current_pokemon.moves
        )

        for widget in current_move_widgets:
            widget.keymap['enter'] = lambda: self.controller.enter_move(widget.move)

        self.currentMoveList = urwidgets.MappedPile( current_move_widgets )

        self.base_hp = urwidgets.MappedWrap(
            ui.LeftRightWidget(" HP: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )
        self.base_att = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Attack: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )
        self.base_def = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Defense: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )
        self.base_satt = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Special Attack: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )
        self.base_sdef = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Special Defense: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )
        self.base_speed = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Speed: ", ''),
            attrmap='base', focusmap='base',
            selectable=False,
        )

        self.base_pile = urwidgets.MappedPile([
            self.base_hp,
            self.base_att,
            self.base_def,
            self.base_satt,
            self.base_sdef,
            self.base_speed,
        ])

        self.hidden_power_field = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Hidden Power Type: ", ''),
            attrmap='item', focusmap='item_focus',
            selectable=True
        )

        self.hidden_power_damage = urwidgets.MappedWrap(
            ui.LeftRightWidget(" Hidden Power Damage: ", ''),
            attrmap='item', focusmap='item_focus',
            selectable=False
        )

        self.level_meter = ui.LabeledMeter(
            'Level', 1, 100, 'progress', 'progress_red',
            initial=self.controller.current_pokemon.level,
        )
        self.happiness_meter = ui.LabeledMeter(
            'Happiness', 0, 255, 'progress', 'progress_red',
            initial=self.controller.current_pokemon.happiness,
        )
        self.attack_exp_meter = ui.LabeledMeter(
            'Attack Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.controller.current_pokemon.attackExp,
            shift_amount=100,
        )
        self.hp_exp_meter = ui.LabeledMeter(
            'HP Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.controller.current_pokemon.hpExp,
            shift_amount=100,
        )
        self.defense_exp_meter = ui.LabeledMeter(
            'Defense Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.controller.current_pokemon.defenseExp,
            shift_amount=100,
        )
        self.speed_exp_meter = ui.LabeledMeter(
            'Speed Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.controller.current_pokemon.speedExp,
            shift_amount=100,
        )
        self.special_exp_meter = ui.LabeledMeter(
            'Special Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.controller.current_pokemon.specialExp,
            shift_amount=100,
        )
        self.attack_dv_meter = ui.LabeledMeter(
            'Attack DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.controller.current_pokemon.attackDv,
        )
        self.defense_dv_meter = ui.LabeledMeter(
            'Defense DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.controller.current_pokemon.defenseDv,
        )
        self.speed_dv_meter = ui.LabeledMeter(
            'Speed DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.controller.current_pokemon.speedDv,
        )
        self.special_dv_meter = ui.LabeledMeter(
            'Special DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.controller.current_pokemon.specialDv,
        )
        self.hp_dv_meter = ui.LabeledMeter(
            'HP DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.controller.current_pokemon.specialDv,
            selectable=False
        )
        self.centerPile = urwidgets.MappedPile(
            [
                self.currentMoveList,
                urwid.Divider('-', top=1, bottom=1),
            ] + utility.inner_lace([
                self.base_pile,
                self.hidden_power_field,
                self.hidden_power_damage,
                urwid.AttrMap(
                    self.level_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.happiness_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.hp_exp_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.attack_exp_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.defense_exp_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.speed_exp_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.special_exp_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.hp_dv_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.attack_dv_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.defense_dv_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.speed_dv_meter,
                    'item', 'item_active'
                ),
                urwid.AttrMap(
                    self.special_dv_meter,
                    'item', 'item_active'
                ),
            ], urwid.Divider(' ')),
            constraint=lambda x, y: y.selectable()
        )

        hidden_power_widgets = [
            urwidgets.MappedWrap(
                urwid.Text(utility.capitalize_move(t)),
                attrmap='item',
                focusmap='item_focus'
            )
            for t in sorted(maps.hidden_power.keys())
        ]

        self.hidden_power_list = urwidgets.MappedList(
            urwid.SimpleListWalker(hidden_power_widgets)
        )

        # --- Actions for Key Mapping ---
        # for convenience in meter setup
        def set_bar_value(func, bar):
            def inner(value):
                func(value)    
                bar.set_completion(value)
            return self.controller.check_meter_value(inner)

        # column transition functions

        def moves_to_current():
            self.currentMoveList.focus.attrmap = 'item'
            self.columns.focus_position = 1

        def current_to_poke():
            self.pokeList.focus.attrmap = 'item'
            self.columns.focus_position = 0
            self.columns.widget_list[2] = self.moveList

        def poke_to_current():
            self.pokeList.focus.attrmap = 'item_active'
            self.columns.focus_position = 1
            self.centerPile.focus_position = 0
            self.currentMoveList.focus_position = 0

        def current_to_moves():
            self.currentMoveList.focus.attrmap = 'item_active'
            self.columns.focus_position = 2

        def moves_set_move():
            widget = self.currentMoveList.focus
            move = widget.move
            current_move = self.current_move
            self.controller.set_move(current_move, move)
            moves_to_current()

        def delete_current_move():
            move = self.currentMoveList.focus.move
            self.controller.delete_move(move)

        def check_hidden_power_focus():
            focus = self.centerPile.focus
            if self.hidden_power_field is focus:
                self.columns.widget_list[2] = urwid.AttrMap(self.hidden_power_list, 'item')
            else:
                self.columns.widget_list[2] = self.moveList

        def hidden_power_to_types():
            self.hidden_power_field.attrmap = 'item_active'
            self.columns.focus_position = 2

        def types_to_hidden_power():
            self.hidden_power_field.attrmap = 'item'
            self.columns.focus_position = 1

        def set_hidden_power():
            value = self.hidden_power_list.focus.text
            self.controller.set_hidden_power(poke, value)
            types_to_hidden_power()

        # Connect signals
        urwid.connect_signal(self.level_meter, 'shift', self.controller.set_level)
        urwid.connect_signal(self.happiness_meter, 'shift', self.controller.set_happiness)
        urwid.connect_signal(self.hp_exp_meter, 'shift', self.self.controller.set_hp_exp)
        urwid.connect_signal(self.attack_exp_meter, 'shift', self.controller.set_attack_exp)
        urwid.connect_signal(self.defense_exp_meter, 'shift', self.controller.set_defense_exp)
        urwid.connect_signal(self.speed_exp_meter, 'shift', self.controller.set_speed_exp)
        urwid.connect_signal(self.special_exp_meter, 'shift', self.controller.set_special_exp)
        urwid.connect_signal(self.attack_dv_meter, 'shift', self.controller.set_attack_dv)
        urwid.connect_signal(self.defense_dv_meter, 'shift', self.controller.set_defense_dv)
        urwid.connect_signal(self.speed_dv_meter, 'shift', self.controller.set_speed_dv)
        urwid.connect_signal(self.special_dv_meter, 'shift', self.controller.set_special_dv)
        urwid.connect_signal(self.centerPile, 'shift', check_hidden_power_focus)
        urwid.connect_signal(self.currentMoveList, 'bottom', self.centerPile.shiftDown)

        # --- Key Mappings ---
        self.level_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Level: ',
                callback=set_bar_value(self.controller.set_level, self.level_meter)
            )
        )
        self.level_meter.keymap['>'] = self.level_meter.increment
        self.level_meter.keymap['<'] = self.level_meter.decrement

        self.happiness_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Happiness: ',
                callback=set_bar_value(self.controller.set_happiness, self.happiness_meter)
            )
        )
        self.happiness_meter.keymap['>'] = self.happiness_meter.increment
        self.happiness_meter.keymap['<'] = self.happiness_meter.decrement

        self.attack_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Attack Exp: ',
                callback=set_bar_value(
                    self.controller.set_attack_exp, self.attack_exp_meter
                )
            )
        )
        self.attack_exp_meter.keymap['>'] = self.attack_exp_meter.increment
        self.attack_exp_meter.keymap['<'] = self.attack_exp_meter.decrement

        self.hp_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='HP Exp: ',
                callback=set_bar_value(self.controller.set_hp_exp, self.hp_exp_meter)
            )
        )
        self.hp_exp_meter.keymap['>'] = self.hp_exp_meter.increment
        self.hp_exp_meter.keymap['<'] = self.hp_exp_meter.decrement

        self.defense_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Defense Exp: ',
                callback=set_bar_value(
                    self.controller.set_defense_exp, self.defense_exp_meter
                )
            )
        )
        self.defense_exp_meter.keymap['>'] = self.defense_exp_meter.increment
        self.defense_exp_meter.keymap['<'] = self.defense_exp_meter.decrement

        self.speed_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Speed Exp: ',
                callback=set_bar_value(self.controller.set_speed_exp, self.speed_exp_meter)
            )
        )
        self.speed_exp_meter.keymap['>'] = self.speed_exp_meter.increment
        self.speed_exp_meter.keymap['<'] = self.speed_exp_meter.decrement

        self.special_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Special Exp: ',
                callback=set_bar_value(
                    self.controller.set_special_exp, self.special_exp_meter
                )
            )
        )
        self.special_exp_meter.keymap['>'] = self.special_exp_meter.increment
        self.special_exp_meter.keymap['<'] = self.special_exp_meter.decrement

        self.attack_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Attack DV: ',
                callback=set_bar_value(self.controller.set_attack_dv,
                self.attack_dv_meter)
            )
        )
        self.attack_dv_meter.keymap['>'] = self.attack_dv_meter.increment
        self.attack_dv_meter.keymap['<'] = self.attack_dv_meter.decrement

        self.defense_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Defense DV: ',
                callback=set_bar_value(self.controller.set_defense_dv,
                self.defense_dv_meter)
            )
        )
        self.defense_dv_meter.keymap['>'] = self.defense_dv_meter.increment
        self.defense_dv_meter.keymap['<'] = self.defense_dv_meter.decrement

        self.speed_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Speed DV: ',
                callback=set_bar_value(self.controller.set_speed_dv,
                self.speed_dv_meter)
            )
        )
        self.speed_dv_meter.keymap['>'] = self.speed_dv_meter.increment
        self.speed_dv_meter.keymap['<'] = self.speed_dv_meter.decrement

        self.special_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Special DV: ',
                callback=set_bar_value(self.controller.set_special_dv,
                self.special_dv_meter)
            )
        )
        self.special_dv_meter.keymap['>'] = self.special_dv_meter.increment
        self.special_dv_meter.keymap['<'] = self.special_dv_meter.decrement

        self.currentMoveList.keymap['j'] = self.currentMoveList.shiftDown
        self.currentMoveList.keymap['k'] = self.currentMoveList.shiftUp
        self.pokeList.keymap['l'] = poke_to_current
        self.pokeList.keymap['right'] = poke_to_current
        self.currentMoveList.keymap['l'] = current_to_moves
        self.currentMoveList.keymap['right'] = current_to_moves
        self.currentMoveList.keymap['h'] = current_to_poke
        self.currentMoveList.keymap['left'] = current_to_poke
        self.currentMoveList.keymap['D'] = delete_current_move

        self.moveList.keymap['h'] = moves_to_current
        self.moveList.keymap['left'] = moves_to_current
        self.moveList.keymap['enter'] = moves_set_move
        self.moveList.keymap['j'] = self.moveList.shiftDown
        self.moveList.keymap['k'] = self.moveList.shiftUp
        self.moveList.keymap['J'] = partial(
            self.moveList.shiftDown,
            amount=10
        )
        self.moveList.keymap['K'] = partial(
            self.moveList.shiftUp,
            amount=10
        )
        self.moveList.keymap['/'] = partial(
            self.controller.start_searching, self.moveList, 'forward'
        )
        self.moveList.keymap['?'] = partial(
            self.controller.start_searching, self.moveList, 'backward'
        )
        self.moveList.keymap['n'] = self.searchNext
        self.moveList.keymap['N'] = self.searchPrev
        self.moveList.keymap['g'] = self.moveList.top
        self.moveList.keymap['G'] = self.moveList.bottom

        self.pokeList.keymap['j'] = self.pokeList.shiftDown
        self.pokeList.keymap['k'] = self.pokeList.shiftUp
        self.pokeList.keymap['J'] = partial(
            self.pokeList.shiftDown,
            amount=10
        )
        self.pokeList.keymap['K'] = partial(
            self.pokeList.shiftUp,
            amount=10
        )
        self.pokeList.keymap['/'] = partial(
            self.controller.start_searching, self.pokeList, 'forward'
        )
        self.pokeList.keymap['?'] = partial(
            self.controller.start_searching, self.pokeList, 'foward'
        )
        self.pokeList.keymap['n'] = self.searchNext
        self.pokeList.keymap['N'] = self.searchPrev
        self.pokeList.keymap['g'] = self.pokeList.top
        self.pokeList.keymap['G'] = self.pokeList.bottom

        self.hidden_power_field.keymap['l'] = hidden_power_to_types

        self.hidden_power_list.keymap['j'] = self.hidden_power_list.shiftDown
        self.hidden_power_list.keymap['k'] = self.hidden_power_list.shiftUp
        self.hidden_power_list.keymap['g'] = self.hidden_power_list.top
        self.hidden_power_list.keymap['G'] = self.hidden_power_list.bottom
        self.hidden_power_list.keymap['h'] = types_to_hidden_power
        self.hidden_power_list.keymap['enter'] = set_hidden_power

        self.centerPile.keymap['j'] = self.centerPile.shiftDown
        self.centerPile.keymap['k'] = self.centerPile.shiftUp
        self.centerPile.keymap['g'] = self.centerPile.top
        self.centerPile.keymap['G'] = self.centerPile.bottom
        self.centerPile.keymap['h'] = current_to_poke

        self.columns = urwid.Columns([
                self.pokeList,
                urwid.Filler(self.centerPile, valign='top'),
                self.moveList
        ])

        self.updateCenterColumn()

        self.fname_widget = urwidgets.MappedWrap
            urwid.Text('%s\n' % self.rom_file.fname, align='center'),
            attrmap='buffername',
            focusmap='buffername',
        )
        super(MainWidget, self).__init__(self.columns, header=fname_widget, commands=commands)

    def _quit(self):
        raise urwid.ExitMainLoop()

    def _max_pokemon(self, overwrite=False):
        poke = self.currentPokemon
        self.controller.max_pokemon(poke, overwrite)

    def update_moves(self):
        for move_widget, move in izip(self.currentMoveList.body, self.current_pokemon.moves):
            move_widget.move = move

    def update_stats(self):
        poke = self.current_pokemon
        self.base_hp.setRight(str(poke.hp) + " ")
        self.base_att.setRight(str(poke.attack) + " ")
        self.base_def.setRight(str(poke.defense) + " ")
        self.base_satt.setRight(str(poke.spattack) + " ")
        self.base_sdef.setRight(str(poke.spdefense) + " ")
        self.base_speed.setRight(str(poke.speed) + " ")
        self.hidden_power_field.setRight(poke.hiddenPowerType.capitalize() + " ")
        self.hidden_power_damage.setRight(str(poke.hiddenPowerDamage) + " ")

    def updateCenterColumn(self):
        self.update_moves()
        poke = self.current_pokemon
        self.level_meter.set_completion(poke.level)
        self.happiness_meter.set_completion(poke.happiness)
        self.attack_exp_meter.set_completion(poke.attackExp)
        self.hp_exp_meter.set_completion(poke.hpExp)
        self.defense_exp_meter.set_completion(poke.defenseExp)
        self.speed_exp_meter.set_completion(poke.speedExp)
        self.special_exp_meter.set_completion(poke.specialExp)
        self.updateHpDv()
        self.attack_dv_meter.set_completion(poke.attackDv)
        self.defense_dv_meter.set_completion(poke.defenseDv)
        self.speed_dv_meter.set_completion(poke.speedDv)
        self.special_dv_meter.set_completion(poke.specialDv)
        self.update_stats()

    def updateLeftColumn(self):
        for pokemon_widget, pokemon in izip(self.pokeList.body, self.controller.pokemon):
            pokemon_widget.pokemon = pokemon

    def updateHpDv(self):
        poke = self.currentPokemon
        self.hp_dv_meter.set_completion(poke.hpDv)

    @property
    def current_pokemon(self):
        return self.pokeList.body.focus.pokemon

    @property
    def current_move(self):
        return self.currentMovesList.focus.move

    @property
    def filename(self):
        self.fname_widget.text

    @filename.setter
    def filename(self, fname):
        self.fname_widget.set_text(fname + '\n')
