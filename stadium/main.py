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

        self.pokemon = tuple(self.buff.pokemon)

        moves = sorted([
            key
            for key, value in
            maps.moves.iteritems()
        ])

        def enter_species():
            self.start_editing(caption="Species: ", callback=self.setSpecies)

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
            shiftFunc=self.updateCenterColumn
        )

        hpIndex = moves.index('hidden power')

        self.moves = moves[:hpIndex] + [
            'hidden power(%s)' % t.capitalize()
            for t in sorted(maps.hidden_power.keys())
        ] + moves[hpIndex+1:]

        self.moveWidgets = [
            urwidgets.MappedWrap(
                urwid.Text(utility.capWord(move)),
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
            hitBottom=self.centerShiftDown,
        )

        self.baseHp = ui.LeftRightWidget("HP: ", "Test",
                                         attrmap='base', focusmap='base',
                                         selectable=False)
        self.baseAtt = ui.LeftRightWidget("Attack: ", "Test",
                                          attrmap='base', focusmap='base',
                                          selectable=False)
        self.baseDef = ui.LeftRightWidget("Defense: ", "Test",
                                          attrmap='base', focusmap='base',
                                          selectable=False)
        self.baseSatt = ui.LeftRightWidget("Special Attack: ", "Test",
                                           attrmap='base', focusmap='base',
                                           selectable=False)
        self.baseSdef = ui.LeftRightWidget("Special Defense: ", "Test",
                                           attrmap='base', focusmap='base',
                                           selectable=False)
        self.baseSpeed = ui.LeftRightWidget("Speed: ", "Test",
                                            attrmap='base', focusmap='base',
                                            selectable=False)

        self.basePile = urwidgets.MappedPile([
            self.baseHp,
            self.baseAtt,
            self.baseDef,
            self.baseSatt,
            self.baseSdef,
            self.baseSpeed,
        ])

        self.level_meter = ui.LabeledMeter(
            'Level', 1, 100, 'progress', 'progress_red',
            initial=self.currentPokemon.level,
            shiftFunc=self.setLevel
        )
        self.happiness_meter = ui.LabeledMeter(
            'Happiness', 0, 255, 'progress', 'progress_red',
            initial=self.currentPokemon.happiness,
            shiftFunc=self.setHappiness
        )
        self.attack_exp_meter = ui.LabeledMeter(
            'Attack Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.attackExp,
            shiftAmount=100,
            shiftFunc=self.setAttackExp
        )
        self.hp_exp_meter = ui.LabeledMeter(
            'HP Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.hpExp,
            shiftAmount=100,
            shiftFunc=self.setHpExp
        )
        self.defense_exp_meter = ui.LabeledMeter(
            'Defense Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.defenseExp,
            shiftAmount=100,
            shiftFunc=self.setDefenseExp
        )
        self.speed_exp_meter = ui.LabeledMeter(
            'Speed Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.speedExp,
            shiftAmount=100,
            shiftFunc=self.setSpeedExp
        )
        self.special_exp_meter = ui.LabeledMeter(
            'Special Exp.', 0, 65535, 'progress', 'progress_blue',
            initial=self.currentPokemon.specialExp,
            shiftAmount=100,
            shiftFunc=self.setSpecialExp
        )
        self.attack_dv_meter = ui.LabeledMeter(
            'Attack DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.attackDv,
            shiftFunc=self.setAttackDv
        )
        self.defense_dv_meter = ui.LabeledMeter(
            'Defense DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.defenseDv,
            shiftFunc=self.setDefenseDv
        )
        self.speed_dv_meter = ui.LabeledMeter(
            'Speed DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.speedDv,
            shiftFunc=self.setSpeedDv
        )
        self.special_dv_meter = ui.LabeledMeter(
            'Special DV.', 0, 15, 'progress', 'progress_cyan',
            initial=self.currentPokemon.specialDv,
            shiftFunc=self.setSpecialDv
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
                self.basePile,
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.level_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.happiness_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.hp_exp_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.attack_exp_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.defense_exp_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.speed_exp_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.special_exp_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.hp_dv_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.attack_dv_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.defense_dv_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.speed_dv_meter,
                    'item', 'item_active'
                ),
                urwid.Divider(' '),
                urwid.AttrMap(
                    self.special_dv_meter,
                    'item', 'item_active'
                ),
            ],
            constraint=lambda x, y: y.selectable()
        )

        # for convenience in meter setup
        def set_bar_value(func, bar):
            def inner(value_string):
                value = int(value_string)
                func(value)
                bar.set_completion(value)
            return inner

        # column transition functions
        def moves_to_current():
            self.unsetActive(self.currentMoveList.focus)
            self.columns.focus_position = 1

        def current_to_poke():
            self.unsetActive(self.pokeList.focus)
            self.columns.focus_position = 0

        def poke_to_current():
            self.setActive(self.pokeList.focus)
            self.columns.focus_position = 1
            self.centerPile.focus_position = 0
            self.currentMoveList.focus_position = 0

        def current_to_moves():
            self.setActive(self.currentMoveList.focus)
            self.columns.focus_position = 2

        def moves_set_move():
            index = self.currentMoveList.focus_position
            move = self.moveList.focus.text
            poke = self.pokemon[self.pokeList.body.focus]
            self.setMove(poke, move, index)
            self.updateCenterColumn()
            moves_to_current()

        def start_searching(direction):
            current_list = self.columns.focus
            current_pos = current_list.focus_position
            current_list.body[current_pos].attrmap = 'item_focus'

            # handles keypresses
            def handler(widget, text):
                w = current_list.focus
                self.inc_search(text, start=current_pos, direction=direction)
                if current_list.focus is not w:
                    w.attrmap = 'item'
                    current_list.focus.attrmap = 'item_focus'

            # for canceling
            def stop_searching():
                current_list.focus.attrmap = 'item'
                urwid.disconnect_signal(self.comand_line, 'change', handler)
                current_list.set_focus(current_pos)

            # for submitting
            def exit_handler(text):
                stop_searching()
                self.search(text, start=current_pos, direction=direction)

            caption = '/' if direction == 'forward' else '?'
            self.start_editing(caption=caption, callback=exit_handler)
            urwid.connect_signal(self.comand_line, 'change', handler)
            self.comand_line.keymap['esc'] = utility.chain(
                stop_searching,
                self.comand_line.keymap['esc']
            )

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
        self.pokeList.keymap['l'] = lambda x: poke_to_current()
        self.currentMoveList.keymap['l'] = current_to_moves
        self.currentMoveList.keymap['h'] = current_to_poke

        self.moveList.keymap['h'] = lambda x: moves_to_current()
        self.moveList.keymap['enter'] = lambda x: moves_set_move()
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
        self.moveList.keymap['/'] = (lambda x: start_searching('forward'))
        self.moveList.keymap['?'] = (lambda x: start_searching('backward'))
        self.moveList.keymap['n'] = (lambda x: self.searchNext())
        self.moveList.keymap['N'] = (lambda x: self.searchPrev())
        self.moveList.keymap['g'] = (lambda x: self.moveList.top())
        self.moveList.keymap['G'] = (lambda x: self.moveList.bottom())

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
        self.pokeList.keymap['/'] = (lambda x: start_searching('forward'))
        self.pokeList.keymap['?'] = (lambda x: start_searching('backward'))
        self.pokeList.keymap['n'] = (lambda x: self.searchNext())
        self.pokeList.keymap['N'] = (lambda x: self.searchPrev())
        self.pokeList.keymap['g'] = (lambda x: self.pokeList.top())
        self.pokeList.keymap['G'] = (lambda x: self.pokeList.bottom())

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
            self.changeStatus('No write since last change (add ! to override)')
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
                self.changeStatus('File not found')
        
    def quit(self, discard=False):
        if self.buff.dirty and not discard:
            self.changeStatus('No write since last change (add ! to override)')
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
        except IOError:
            self.changeStatus('File not found')
        self.updateCenterColumn()
        self.updateLeftColumn()

    def export_json(self, fname):
        with open(fname, 'w') as fp:
            mappers.json.dump(fp, self.buff)

    def inc_search(self, query, start=0, direction='forward'):
        current_list = self.columns.focus
        current_pos = current_list.focus_position if start is None else start
        predicate = (lambda x: query.lower() in x.base_widget.text.lower())
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
        self.last_search = query
        self.last_search_direction = direction
        current_list = self.columns.focus
        current_pos = current_list.focus_position if start is None else start
        predicate = (lambda x: query.lower() in x.base_widget.text.lower())
        index = current_list.find(
            predicate,
            start=current_pos,
            direction=direction
        )
        if index == -1:
            self.changeStatus('%s Not Found.' % query)
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

    def updateMoves(self):
        self.currentMoveList.set(self.currentMoves())

    def updateStats(self):
        poke = self.currentPokemon
        self.baseHp.setRight(str(poke.hp))
        self.baseAtt.setRight(str(poke.attack))
        self.baseDef.setRight(str(poke.defense))
        self.baseSatt.setRight(str(poke.spattack))
        self.baseSdef.setRight(str(poke.spdefense))
        self.baseSpeed.setRight(str(poke.speed))

    def updateCenterColumn(self):
        self.updateMoves()
        poke = self.currentPokemon
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
        self.updateStats()

    def updateLeftColumn(self):
        def enter_species():
            self.start_editing(caption="Species: ", callback=self.setSpecies)

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

    def maxPokemon(self, overwrite=False):
        poke = self.currentPokemon
        h_type = poke.hiddenPowerType
        poke.max()

        if not overwrite and 'hidden power' in poke.moves:
            poke.hiddenPowerType = h_type

        self.updateCenterColumn()
        self.updateHpDv()

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
        self.updateHpDv()

    def setSpecies(self, species):
        poke = self.currentPokemon
        species = species.lower()
        if species in maps.pokemon:
            poke.species = species
            self.updateLeftColumn()
            self.updateCenterColumn()
        else:
            self.changeStatus('Pokemon not recognized')

    def setAttackDv(self, value):
        poke = self.currentPokemon
        poke.attackDv = value
        self.updateHpDv()

        self.updateStats()
        # Update moves to refresh hidden power
        self.updateMoves()

    def setDefenseDv(self, value):
        poke = self.currentPokemon
        poke.defenseDv = value
        self.updateHpDv()

        self.updateStats()
        # Update moves to refresh hidden power
        self.updateMoves()

    def setSpeedDv(self, value):
        poke = self.currentPokemon
        poke.speedDv = value
        self.updateHpDv()
        self.updateStats()

    def setSpecialDv(self, value):
        poke = self.currentPokemon
        poke.specialDv = value
        self.updateHpDv()
        self.updateStats()

    def setSpecialExp(self, value):
        poke = self.currentPokemon
        poke.specialExp = value
        self.updateStats()

    def setSpeedExp(self, value):
        poke = self.currentPokemon
        poke.speedExp = value
        self.updateStats()

    def setDefenseExp(self, value):
        poke = self.currentPokemon
        poke.defenseExp = value
        self.updateStats()

    def setHpExp(self, value):
        poke = self.currentPokemon
        poke.hpExp = value
        self.updateStats()

    def setAttackExp(self, value):
        poke = self.currentPokemon
        poke.attackExp = value
        self.updateStats()

    def setHappiness(self, happiness):
        poke = self.currentPokemon
        poke.happiness = happiness

    def setMove(self, pokemon, move, index):
        if 'hidden power' in move.lower():
            t = move[13:move.index(')')]
            poke = self.currentPokemon
            poke.hiddenPowerType = t
            move = 'hidden power'
        pokemon.moves[index] = move

    def setLevel(self, level):
        poke = self.currentPokemon
        poke.level = level
        self.level_meter.set_completion(poke.level)
        self.updateStats()

    def centerShiftDown(self):
        self.centerPile.shiftDown()

    @property
    def currentPokemon(self):
        return self.pokemon[self.pokeList.body.focus]

    def currentMoves(self):
        poke = self.currentPokemon
        return [
            urwidgets.MappedWrap(
                urwid.Text(
                    '-----' if move is None else
                    'Hidden Power(%s)' % poke.hiddenPowerType
                    if move == 'hidden power'
                    else utility.capWord(move)
                ),
                attrmap='item',
                focusmap='item_focus'
            )
            for move in poke.moves
        ]

    def setActive(self, widget):
        widget.set_attr_map({None: 'item_active'})

    def unsetActive(self, widget):
        widget.set_attr_map({None: 'item'})
