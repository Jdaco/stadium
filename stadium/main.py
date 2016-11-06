from functools import partial
import urwid
import ui
import maps
import domain
import urwidgets
import utility
import mappers


class MainWidget(urwidgets.CommandFrame):
    def __init__(self, buff):
        self.commands = {
            'w': self.write,
            'q': self.quit,
            'q!': partial(self.quit, discard=True),
            'wq': utility.chain(self.write, self.quit),
            'quit': self.quit,
            'quit!': partial(self.quit, discard=True),
            'edit': self.edit_file,
            'edit!': partial(self.edit_file, discard=True),
            'write': self.write,
            'import': self.import_json,
            'export': self.export_json,
            'max': self.maxPokemon,
            'max!': partial(self.maxPokemon, overwrite=True),
            'maxall': self.maxAllPokemon,
            'maxall!': partial(self.maxAllPokemon, overwrite=True),
        }

        self.last_search = None
        self.last_search_direction = None

        self.buff = buff

        self.current_json = None

        self.pokemon = tuple(self.buff.pokemon)

        self.moves = sorted([
            key
            for key, value in
            maps.moves.iteritems()
        ])

        #Start command to change species
        def enter_species():
            self.start_editing(
                caption="Species: ",
                callback=self.setSpecies,
                completion_set = maps.pokemon.keys(),
            )

        # --- Create Widgets ---
        self.pokemonWidgets = [
            urwidgets.MappedWrap(
                urwid.Text(poke.species.capitalize()),
                attrmap='item', 
                focusmap='item_focus',
                keymap={'enter': enter_species}
            )
            for poke in self.pokemon
        ]
        self.pokeList = urwidgets.MappedList(
            urwid.SimpleFocusListWalker(self.pokemonWidgets),
        )
        urwid.connect_signal(self.pokeList, 'shift', self.updateCenterColumn)

        self.moveWidgets = [
            urwidgets.MappedWrap(
                urwid.Text(utility.capitalize_move(move)),
                attrmap='item',
                focusmap='item_focus'
            )
            for move in self.moves
        ]
        self.moveList = urwidgets.MappedList(
            urwid.SimpleFocusListWalker(self.moveWidgets)
        )

        self.currentMoveList = urwidgets.MappedPile(
            self.currentMoves(),
        )

        urwid.connect_signal(self.currentMoveList, 'bottom', self.centerShiftDown)

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

        self.level_meter = ui.LabeledMeter(
            'Level', 1, 100, 'progress', 'progress_red',
            initial=self.currentPokemon.level,
        )
        self.happiness_meter = ui.LabeledMeter(
            'Happiness', 0, 255, 'progress', 'progress_red',
            initial=self.currentPokemon.happiness,
        )
        self.attack_exp_meter = ui.LabeledMeter(
            'Attack Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.attackExp,
            shift_amount=100,
        )
        self.hp_exp_meter = ui.LabeledMeter(
            'HP Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.hpExp,
            shift_amount=100,
        )
        self.defense_exp_meter = ui.LabeledMeter(
            'Defense Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.defenseExp,
            shift_amount=100,
        )
        self.speed_exp_meter = ui.LabeledMeter(
            'Speed Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.speedExp,
            shift_amount=100,
        )
        self.special_exp_meter = ui.LabeledMeter(
            'Special Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.specialExp,
            shift_amount=100,
        )
        self.attack_dv_meter = ui.LabeledMeter(
            'Attack DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.attackDv,
        )
        self.defense_dv_meter = ui.LabeledMeter(
            'Defense DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.defenseDv,
        )
        self.speed_dv_meter = ui.LabeledMeter(
            'Speed DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.speedDv,
        )
        self.special_dv_meter = ui.LabeledMeter(
            'Special DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.specialDv,
        )
        self.hp_dv_meter = ui.LabeledMeter(
            'HP DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.specialDv,
            selectable=False
        )
        self.centerPile = urwidgets.MappedPile(
            [
                self.currentMoveList,
                urwid.Divider('-', top=1, bottom=1),
            ] + utility.inner_lace([
                self.base_pile,
                self.hidden_power_field,
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
            def inner(value_string):
                try:
                    value = int(value_string)
                except ValueError:
                    self.change_status("Invalid Value")
                else:
                    func(value)
                    bar.set_completion(value)
            return inner

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
            index = self.currentMoveList.focus_position
            move = self.moveList.focus.text
            self.setMove(move, index)
            moves_to_current()

        def delete_current_move():
            index = self.currentMoveList.focus_position
            self.deleteMove(index)

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
            self.setHiddenPower(value.lower())
            types_to_hidden_power()

        def start_searching(direction):
            current_list = self.columns.focus
            current_pos = current_list.focus_position
            current_list.body[current_pos].attrmap = {None: 'item_focus'}

            # handles keypresses
            def handler(widget, text):
                w = current_list.focus
                self.inc_search(text, start=current_pos, direction=direction)
                if current_list.focus is not w:
                    w.attrmap = {None: 'item'}
                    current_list.focus.attrmap = {None: 'item_focus'}

            # for canceling
            def stop_searching():
                current_list.focus.attrmap = {None: 'item'}
                urwid.disconnect_signal(self.command_line, 'change', handler)
                current_list.set_focus(current_pos)

            # for submitting
            def exit_handler(text):
                stop_searching()
                self.search(text, start=current_pos, direction=direction)

            #cleans up after a backspace cancel
            #this should be removed in favor of events
            def backspace_handler():
                if self.command_line.edit_text == '':
                    stop_searching()

            caption = '/' if direction == 'forward' else '?'
            self.start_editing(caption=caption, callback=exit_handler)
            urwid.connect_signal(self.command_line, 'change', handler)
            self.command_line.keymap['esc'] = utility.chain(
                stop_searching,
                self.command_line.keymap['esc']
            )
            self.command_line.keymap['backspace'] = utility.chain(
                backspace_handler,
                self.command_line.keymap['backspace'],
            )


        # Connect signals
        urwid.connect_signal(self.level_meter, 'shift', self.setLevel)
        urwid.connect_signal(self.happiness_meter, 'shift', self.setHappiness)
        urwid.connect_signal(self.hp_exp_meter, 'shift', self.setHpExp)
        urwid.connect_signal(self.attack_exp_meter, 'shift', self.setAttackExp)
        urwid.connect_signal(self.defense_exp_meter, 'shift', self.setDefenseExp)
        urwid.connect_signal(self.speed_exp_meter, 'shift', self.setSpeedExp)
        urwid.connect_signal(self.special_exp_meter, 'shift', self.setSpecialExp)
        urwid.connect_signal(self.attack_dv_meter, 'shift', self.setAttackDv)
        urwid.connect_signal(self.defense_dv_meter, 'shift', self.setDefenseDv)
        urwid.connect_signal(self.speed_dv_meter, 'shift', self.setSpeedDv)
        urwid.connect_signal(self.special_dv_meter, 'shift', self.setSpecialDv)
        urwid.connect_signal(self.centerPile, 'shift', check_hidden_power_focus)

        # --- Key Mappings ---
        self.level_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Level: ',
                callback=set_bar_value(self.setLevel, self.level_meter)
            )
        )
        self.level_meter.keymap['>'] = self.level_meter.increment
        self.level_meter.keymap['<'] = self.level_meter.decrement

        self.happiness_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Happiness: ',
                callback=set_bar_value(self.setHappiness, self.happiness_meter)
            )
        )
        self.happiness_meter.keymap['>'] = self.happiness_meter.increment
        self.happiness_meter.keymap['<'] = self.happiness_meter.decrement

        self.attack_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Attack Exp: ',
                callback=set_bar_value(
                    self.setAttackExp, self.attack_exp_meter
                )
            )
        )
        self.attack_exp_meter.keymap['>'] = self.attack_exp_meter.increment
        self.attack_exp_meter.keymap['<'] = self.attack_exp_meter.decrement

        self.hp_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='HP Exp: ',
                callback=set_bar_value(self.setHpExp, self.hp_exp_meter)
            )
        )
        self.hp_exp_meter.keymap['>'] = self.hp_exp_meter.increment
        self.hp_exp_meter.keymap['<'] = self.hp_exp_meter.decrement

        self.defense_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Defense Exp: ',
                callback=set_bar_value(
                    self.setDefenseExp, self.defense_exp_meter
                )
            )
        )
        self.defense_exp_meter.keymap['>'] = self.defense_exp_meter.increment
        self.defense_exp_meter.keymap['<'] = self.defense_exp_meter.decrement

        self.speed_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Speed Exp: ',
                callback=set_bar_value(self.setSpeedExp, self.speed_exp_meter)
            )
        )
        self.speed_exp_meter.keymap['>'] = self.speed_exp_meter.increment
        self.speed_exp_meter.keymap['<'] = self.speed_exp_meter.decrement

        self.special_exp_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Special Exp: ',
                callback=set_bar_value(
                    self.setSpecialExp, self.special_exp_meter
                )
            )
        )
        self.special_exp_meter.keymap['>'] = self.special_exp_meter.increment
        self.special_exp_meter.keymap['<'] = self.special_exp_meter.decrement

        self.attack_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Attack DV: ',
                callback=set_bar_value(self.setAttackDv, self.attack_dv_meter)
            )
        )
        self.attack_dv_meter.keymap['>'] = self.attack_dv_meter.increment
        self.attack_dv_meter.keymap['<'] = self.attack_dv_meter.decrement

        self.defense_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Defense DV: ',
                callback=set_bar_value(self.setDefenseDv, self.defense_dv_meter)
            )
        )
        self.defense_dv_meter.keymap['>'] = self.defense_dv_meter.increment
        self.defense_dv_meter.keymap['<'] = self.defense_dv_meter.decrement

        self.speed_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Speed DV: ',
                callback=set_bar_value(self.setSpeedDv, self.speed_dv_meter)
            )
        )
        self.speed_dv_meter.keymap['>'] = self.speed_dv_meter.increment
        self.speed_dv_meter.keymap['<'] = self.speed_dv_meter.decrement

        self.special_dv_meter.keymap['enter'] = (
            lambda: self.start_editing(
                caption='Special DV: ',
                callback=set_bar_value(self.setSpecialDv, self.special_dv_meter)
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
        self.moveList.keymap['/'] = lambda: start_searching('forward')
        self.moveList.keymap['?'] = lambda: start_searching('backward')
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
        self.pokeList.keymap['/'] = lambda: start_searching('forward')
        self.pokeList.keymap['?'] = lambda: start_searching('backward')
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

        fname_widget = urwid.AttrMap(
            urwid.Text('%s\n' % self.buff.fname, align='center'),
            'buffername', 'buffername',
        )
        super(MainWidget, self).__init__(self.columns, header=fname_widget)

    def edit_file(self, fname, discard=False):
        if self.buff.dirty and not discard:
            self.change_status('No write since last change (add ! to override)')
        else:
            try:
                with open(fname, 'rb') as fp:
                    self.buff = domain.ROMBuffer(fp)
                self.pokemon = tuple(self.buff.pokemon)
                self.updateLeftColumn()
                self.updateCenterColumn()
                fname_widget = urwid.AttrMap(
                    urwid.Text('%s\n' % self.buff.fname, align='center'),
                    'buffername', 'buffername',
                )
                self.header = fname_widget
            except IOError:
                self.change_status('File not found')

    def quit(self, discard=False):
        if self.buff.dirty and not discard:
            self.change_status('No write since last change (add ! to override)')
        else:
            raise urwid.ExitMainLoop()

    def write(self, fname=None):
        fname = fname if fname else self.buff.fname
        with open(fname, 'wb') as fp:
            self.buff.write(fp)

    def import_json(self, fname):
        try:
            with open(fname, 'r') as fp:
                mappers.json.load(fp, self.buff)
                self.current_json = fname
        except IOError:
            self.change_status('File not found')
        self.updateCenterColumn()
        self.updateLeftColumn()

    def export_json(self, fname=None):
        if not fname:
            if self.current_json:
                fname = self.current_json
            else:
                self.change_status("Not a valid file name")
                return
        with open(fname, 'w') as fp:
            mappers.json.dump(fp, self.buff)

    def inc_search(self, query, start=0, direction='forward'):
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

    def search(self, query, start=None, direction='forward'):
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

    def maxPokemon(self, overwrite=False):
        poke = self.currentPokemon
        h_type = poke.hiddenPowerType
        poke.max()

        if not overwrite and 'hidden power' in poke.moves:
            poke.hiddenPowerType = h_type

        self.updateCenterColumn()

    def maxAllPokemon(self, overwrite=False):
        if not overwrite:
            for pokemon in self.pokemon:
                h_type = pokemon.hiddenPowerType
                pokemon.max()
                if 'hidden power' in pokemon.moves:
                    pokemon.hiddenPowerType = h_type
        else:
            for pokemon in self.pokemon:
                pokemon.max()
            
        self.updateCenterColumn()

    def updateMoves(self):
        self.currentMoveList.set(self.currentMoves())

    def updateStats(self):
        poke = self.currentPokemon
        self.base_hp.setRight(str(poke.hp) + " ")
        self.base_att.setRight(str(poke.attack) + " ")
        self.base_def.setRight(str(poke.defense) + " ")
        self.base_satt.setRight(str(poke.spattack) + " ")
        self.base_sdef.setRight(str(poke.spdefense) + " ")
        self.base_speed.setRight(str(poke.speed) + " ")
        self.hidden_power_field.setRight(poke.hiddenPowerType.capitalize() + " ")

    def updateCenterColumn(self):
        self.updateMoves()
        poke = self.currentPokemon
        self.level_meter._set_completion(poke.level)
        self.happiness_meter._set_completion(poke.happiness)
        self.attack_exp_meter._set_completion(poke.attackExp)
        self.hp_exp_meter._set_completion(poke.hpExp)
        self.defense_exp_meter._set_completion(poke.defenseExp)
        self.speed_exp_meter._set_completion(poke.speedExp)
        self.special_exp_meter._set_completion(poke.specialExp)
        self.updateHpDv()
        self.attack_dv_meter._set_completion(poke.attackDv)
        self.defense_dv_meter._set_completion(poke.defenseDv)
        self.speed_dv_meter._set_completion(poke.speedDv)
        self.special_dv_meter._set_completion(poke.specialDv)
        self.updateStats()

    def updateLeftColumn(self):
        def enter_species():
            self.start_editing(
                caption="Species: ",
                callback=self.setSpecies,
                completion_set = maps.pokemon,
            )

        self.pokeList.set([
            urwidgets.MappedWrap(
                urwid.Text(poke.species.capitalize()),
                attrmap='item',
                focusmap='item_focus',
                keymap={'enter': enter_species})
            for poke in self.pokemon
        ])

    def updateHpDv(self):
        poke = self.currentPokemon
        self.hp_dv_meter.set_completion(poke.hpDv)

    def setHiddenPower(self, value):
        poke = self.currentPokemon
        if value in maps.hidden_power:
            poke.hiddenPowerType = value
            self.updateCenterColumn()
        else:
            self.change_status('Invalid type')

    def setSpecies(self, species):
        poke = self.currentPokemon
        species = species.lower()
        if species in maps.pokemon:
            poke.species = species
            self.updateLeftColumn()
            self.updateCenterColumn()
        else:
            self.change_status('Pokemon not recognized')

    def setAttackDv(self, value):
        self.currentPokemon.attackDv = value
        self.updateHpDv()
        self.updateStats()

    def setDefenseDv(self, value):
        self.currentPokemon.defenseDv = value
        self.updateHpDv()

        self.updateStats()

    def setSpeedDv(self, value):
        self.currentPokemon.speedDv = value
        self.updateHpDv()
        self.updateStats()

    def setSpecialDv(self, value):
        self.currentPokemon.specialDv = value
        self.updateHpDv()
        self.updateStats()

    def setSpecialExp(self, value):
        self.currentPokemon.specialExp = value
        self.updateStats()

    def setSpeedExp(self, value):
        self.currentPokemon.speedExp = value
        self.updateStats()

    def setDefenseExp(self, value):
        self.currentPokemon.defenseExp = value
        self.updateStats()

    def setHpExp(self, value):
        self.currentPokemon.hpExp = value
        self.updateStats()

    def setAttackExp(self, value):
        self.currentPokemon.attackExp = value
        self.updateStats()

    def setHappiness(self, happiness):
        poke = self.currentPokemon
        poke.happiness = happiness

    def deleteMove(self, index):
        poke = self.currentPokemon
        poke.moves[index] = None
        self.updateCenterColumn()

    def setMove(self, move, index):
        poke = self.currentPokemon
        if move.lower() in maps.moves:
            poke.moves[index] = move
            self.updateCenterColumn()
        else:
            self.change_status("Move not found")

    def setLevel(self, value):
        self.currentPokemon.level = value
        self.updateStats()

    def centerShiftDown(self):
        self.centerPile.shiftDown()

    @property
    def currentPokemon(self):
        return self.pokemon[self.pokeList.body.focus]

    def currentMoves(self):
        poke = self.currentPokemon
        
        def enter_move():
            self.start_editing(
                caption="Move: ",
                callback = partial(
                    self.setMove,
                    index=self.currentMoveList.focus_position,
                ),
                completion_set=maps.moves,
            )

        return [
            urwidgets.MappedWrap(
                urwid.Text(
                    '-----' if move is None
                    else utility.capitalize_move(move)
                ),
                attrmap='item',
                focusmap='item_focus',
                keymap={'enter': enter_move},
            )
            for move in poke.moves
        ]
