#!/usr/bin/python2
import maps
import math

class ROMBuffer(object):

    _base = 0x99080
    _baseHp = 1
    _baseAtt = 2
    _baseDef = 3
    _baseSpeed = 4
    _baseSatt = 5
    _baseSdef = 6

    def __init__(self, fp):
        self.fname = fp.name
        self.binary = bytearray(fp.read())
        fp.close()

        self.pokeStart = 0x1708CB4

    def baseStats(self, species):
        index = self._base + 22 * (maps.pokemon[species] - 1)
        return {
            'dex': self.binary[index],
            'attack': self.binary[index + self._baseAtt],
            'defense': self.binary[index + self._baseDef],
            'sattack': self.binary[index + self._baseSatt],
            'sdefense': self.binary[index + self._baseSdef],
            'hp': self.binary[index + self._baseHp],
            'speed': self.binary[index + self._baseSpeed],
        }

    @property
    def pokemon(self):
        return (
            Pokemon(self, i) for i in xrange(246)
        )

    def pokemonAt(self, index):
        return self.binary[self.pokeStart+index*24:self.pokeStart+(index+1)*24]

    def setValue(self, index, byte, value):
        self.binary[self.pokeStart+index*24+byte] = value

    def write(self, fname=None):
        fname = self.fname if not fname else fname
        with open(fname, 'wb') as fp:
            fp.write(self.binary)


class Moveset(object):
    def __init__(index, buff):
        self.byteIndex = index
        self.buff = buff

    def __contains__(self, value):
        return value in (
            self[0]
            self[1]
            self[2]
            self[3]
        )

    def __getitem__(self, index):
        if index > 3 or index < 0:
            raise ValueError("Invalid index")
        byte = self.buff[self.byteIndex + index]
        if byte == 0:
            return None
        return maps.moves_reversed[byte]

    def __setitem__(self, index, value):
        if index > 3 or index < 0:
            raise ValueError("Invalid index")
        move = maps.moves[value.lower()] if value is not None else 0
        self.rom[self.byteIndex + index] = move
    
class Pokemon(object):
    _level = 0
    _species = 1
    _moveStart = 4
    _happiness = 9
    _hpExp = 10
    _attackExp = 12
    _defenseExp = 14
    _speedExp = 16
    _specialExp = 18
    _attackDv = 20
    _defenseDv = 20
    _speedDv = 21
    _specialDv = 21

    def __init__(self, rom, index):
        self.rom = rom
        self.index = index
        self.moves = Moveset(index + self._moveStart, rom)

    def _getPokemon(self, index):
        return self.rom.pokemonAt(self.index)[index]

    def _sepBytes(self, number):
        b = b'%04x' % number
        return (
            int(b[:2], 16),
            int(b[2:], 16),
        )

    def max(self):
        self.level = 100
        self.happiness = 2**8 - 1
        self.hpExp = 2**16 - 1
        self.attackExp = 2**16 - 1
        self.defenseExp = 2**16 - 1
        self.specialExp = 2**16 - 1
        self.speedExp = 2**16 - 1
        self.attackDv = 2**4 - 1
        self.defenseDv = 2**4 - 1
        self.specialDv = 2**4 - 1
        self.speedDv = 2 ** 4 - 1

    @property
    def hiddenPowerType(self):
        return maps.hidden_power_reversed[(
            self.attackDv % 4,
            self.defenseDv % 4,
        )]

    @hiddenPowerType.setter
    def hiddenPowerType(self, value):
        attack, defense = maps.hidden_power[value]
        self.attackDv = self.attackDv + (attack - (self.attackDv % 4))
        self.defenseDv = self.defenseDv + (defense - (self.defenseDv % 4))

    @property
    def species(self):
        return maps.pokemon_reversed[self._getPokemon(self._species)]

    @species.setter
    def species(self, value):
        self.rom.setValue(self.index, self._species, maps.pokemon[value.lower()])

    @property
    def level(self):
        return self._getPokemon(self._level)

    @level.setter
    def level(self, value):
        if value >= 1 and value <= 100:
            self.rom.setValue(self.index, self._level, value)

    @property
    def happiness(self):
        return self._getPokemon(self._happiness)

    @happiness.setter
    def happiness(self, value):
        self.rom.setValue(self.index, self._happiness, value)

    @property
    def hpExp(self):
        return (self._getPokemon(self._hpExp) << 8) + self._getPokemon(self._hpExp + 1)

    @hpExp.setter
    def hpExp(self, value):
        byteOne, byteTwo = self._sepBytes(value)
        self.rom.setValue(self.index, self._hpExp, byteOne)
        self.rom.setValue(self.index, self._hpExp + 1, byteTwo)

    @property
    def attackExp(self):
        return (self._getPokemon(self._attackExp) << 8) + self._getPokemon(self._attackExp + 1)

    @attackExp.setter
    def attackExp(self, value):
        byteOne, byteTwo = self._sepBytes(value)
        self.rom.setValue(self.index, self._attackExp, byteOne)
        self.rom.setValue(self.index, self._attackExp + 1, byteTwo)

    @property
    def defenseExp(self):
        return (self._getPokemon(self._defenseExp) << 8) + self._getPokemon(self._defenseExp + 1)

    @defenseExp.setter
    def defenseExp(self, value):
        byteOne, byteTwo = self._sepBytes(value)
        self.rom.setValue(self.index, self._defenseExp, byteOne)
        self.rom.setValue(self.index, self._defenseExp + 1, byteTwo)

    @property
    def speedExp(self):
        return (self._getPokemon(self._speedExp) << 8) + self._getPokemon(self._speedExp + 1)

    @speedExp.setter
    def speedExp(self, value):
        byteOne, byteTwo = self._sepBytes(value)
        self.rom.setValue(self.index, self._speedExp, byteOne)
        self.rom.setValue(self.index, self._speedExp + 1, byteTwo)

    @property
    def specialExp(self):
        return (self._getPokemon(self._specialExp) << 8) + self._getPokemon(self._specialExp + 1)

    @specialExp.setter
    def specialExp(self, value):
        byteOne, byteTwo = self._sepBytes(value)
        self.rom.setValue(self.index, self._specialExp, byteOne)
        self.rom.setValue(self.index, self._specialExp + 1, byteTwo)

    @property
    def attackDv(self):
        return (self._getPokemon(self._attackDv) & 0xf0) >> 4

    @attackDv.setter
    def attackDv(self, value):
        byte = self.defenseDv + (value << 4)
        self.rom.setValue(self.index, self._attackDv, byte)

    @property
    def defenseDv(self):
        return self._getPokemon(self._defenseDv) & 0x0f

    @defenseDv.setter
    def defenseDv(self, value):
        byte = (self.attackDv << 4) + value
        self.rom.setValue(self.index, self._defenseDv, byte)

    @property
    def speedDv(self):
        return (self._getPokemon(self._speedDv) & 0xf0) >> 4

    @speedDv.setter
    def speedDv(self, value):
        byte = self.specialDv + (value << 4)
        self.rom.setValue(self.index, self._speedDv, byte)

    @property
    def specialDv(self):
        return self._getPokemon(self._specialDv) & 0x0f

    @specialDv.setter
    def specialDv(self, value):
        byte = (self.speedDv << 4) + value
        self.rom.setValue(self.index, self._specialDv, byte)

    @property
    def hpDv(self):
        return 8 * (self.attackDv % 2) + \
            4 * (self.defenseDv % 2) + \
            2 * (self.speedDv % 2) + \
            (self.specialDv % 2)

    @property
    def hp(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['hp'],
            self.hpDv,
            self.hpExp,
        ) + self.level + 5

    @property
    def attack(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['attack'],
            self.attackDv,
            self.attackExp,
        )

    @property
    def defense(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['defense'],
            self.defenseDv,
            self.defenseExp,
        )

    @property
    def spattack(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['sattack'],
            self.specialDv,
            self.specialExp,
        )

    @property
    def spdefense(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['sdefense'],
            self.specialDv,
            self.specialExp,
        )

    @property
    def speed(self):
        return self._statCalc(
            self.rom.baseStats(self.species)['speed'],
            self.speedDv,
            self.speedExp,
        )

    def _statCalc(self, base, dv, se):
        sp = min(63, (int(math.sqrt(max(0, se - 1))) + 1) / 4)
        return (((2 * (base + dv) + sp) * self.level) / 100) + 5
