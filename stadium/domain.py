#!/usr/bin/python2
import maps
import math

class ROMBuffer(object):

    _rentalStart = 0x1708CB4
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
        self.dirty = False

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
            Pokemon(self, i) for i in xrange(self._rentalStart, self._rentalStart + 246 * 24, 24)
        )

    def write(self, fp):
        fp.write(self.binary)
        self.dirty = False

    def __getitem__(self, index):
        return self.binary[index]

    def __setitem__(self, index, value):
        self.binary[index] = value
        self.dirty = True


class Moveset(object):
    def __init__(self, buff, addr):
        self.addr = addr
        self.buff = buff

    def __contains__(self, value):
        return value in (
            self[0],
            self[1],
            self[2],
            self[3],
        )

    def __getitem__(self, index):
        if index > 3 or index < 0:
            raise IndexError("Invalid index")
        byte = self.buff[self.addr + index]
        if byte == 0:
            return None
        return maps.moves_reversed[byte]

    def __setitem__(self, index, value):
        if index > 3 or index < 0:
            raise IndexError("Invalid index")
        elif value is not None and value.lower() not in maps.moves:
            raise ValueError("Invalud Move")
        move = maps.moves[value.lower()] if value is not None else 0
        self.buff[self.addr + index] = move

    def __iter__(self):
        return (
            self[i]
            for i in xrange(0, 4)
        )


class Pokemon(object):
    # Each pokemon is 24 bytes long
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

    def __init__(self, buff, addr):
        self.buff = buff
        self.addr = addr
        self.moves = Moveset(buff, addr + self._moveStart)

    def __getitem__(self, index):
        return self.buff[self.addr + index] 

    def __setitem__(self, index, value):
        self.buff[self.addr + index] = value

    def _sepBytes(self, number):
        b = b'%04x' % number
        return (
            int(b[:2], 16),
            int(b[2:], 16),
        )

    def _statCalc(self, base, dv, se):
        sp = min(63, int(math.sqrt(max(0, se))) / 4)
        return (((2 * (base + dv) + sp) * self.level) / 100)

    def max(self):
        self.level = 100
        self.happiness = 0xFF
        self.hpExp = 0xFFFF
        self.attackExp = 0xFFFF
        self.defenseExp = 0xFFFF
        self.specialExp = 0xFFFF
        self.speedExp = 0xFFFF
        self.attackDv = 0xF
        self.defenseDv = 0xF
        self.specialDv = 0xF
        self.speedDv = 0xF

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
    def hiddenPowerDamage(self):
        v = (self.specialDv & 8) % 7
        w = (self.speedDv & 8) % 7
        x = (self.defenseDv & 8) % 7
        y = (self.attackDv & 8) % 7
        z = self.specialDv % 4

        value = ((5 * (v + 2*w + 4*x + 8*y) + z) / 2) + 31
        return value


    @property
    def species(self):
        return maps.pokemon_reversed[self[self._species]]

    @species.setter
    def species(self, value):
        self[self._species] = maps.pokemon[value.lower()]

    @property
    def level(self):
        return self[self._level]

    @level.setter
    def level(self, value):
        value = min(value, 100)
        value = max(value, 1)
        self[self._level] = value

    @property
    def happiness(self):
        return self[self._happiness]

    @happiness.setter
    def happiness(self, value):
        value = min(value, 255)
        value = max(value, 0)
        self[self._happiness] = value

    @property
    def hpExp(self):
        return (self[self._hpExp] << 8) + self[self._hpExp + 1]

    @hpExp.setter
    def hpExp(self, value):
        value = min(value, 0xFFFF)
        value = max(value, 0)
        byteOne, byteTwo = self._sepBytes(value)
        self[self._hpExp] = byteOne
        self[self._hpExp + 1] = byteTwo

    @property
    def attackExp(self):
        return (self[self._attackExp] << 8) + self[self._attackExp + 1]

    @attackExp.setter
    def attackExp(self, value):
        value = min(value, 0xFFFF)
        value = max(value, 0)
        byteOne, byteTwo = self._sepBytes(value)
        self[self._attackExp] = byteOne
        self[self._attackExp + 1] = byteTwo

    @property
    def defenseExp(self):
        return (self[self._defenseExp] << 8) + self[self._defenseExp + 1]

    @defenseExp.setter
    def defenseExp(self, value):
        value = min(value, 0xFFFF)
        value = max(value, 0)
        byteOne, byteTwo = self._sepBytes(value)
        self[self._defenseExp] = byteOne
        self[self._defenseExp + 1] = byteTwo

    @property
    def speedExp(self):
        return (self[self._speedExp] << 8) + self[self._speedExp + 1]

    @speedExp.setter
    def speedExp(self, value):
        value = min(value, 0xFFFF)
        value = max(value, 0)
        byteOne, byteTwo = self._sepBytes(value)
        self[self._speedExp] = byteOne
        self[self._speedExp + 1] = byteTwo

    @property
    def specialExp(self):
        return (self[self._specialExp] << 8) + self[self._specialExp + 1]

    @specialExp.setter
    def specialExp(self, value):
        value = min(value, 0xFFFF)
        value = max(value, 0)
        byteOne, byteTwo = self._sepBytes(value)
        self[self._specialExp] = byteOne
        self[self._specialExp + 1] = byteTwo

    @property
    def attackDv(self):
        return (self[self._attackDv] & 0xf0) >> 4

    @attackDv.setter
    def attackDv(self, value):
        value = min(15, value)
        value = max(0, value)
        byte = self.defenseDv + (value << 4)
        self[self._attackDv] = byte

    @property
    def defenseDv(self):
        return self[self._defenseDv] & 0x0f

    @defenseDv.setter
    def defenseDv(self, value):
        value = min(15, value)
        value = max(0, value)
        byte = (self.attackDv << 4) + value
        self[self._defenseDv] = byte

    @property
    def speedDv(self):
        return (self[self._speedDv] & 0xf0) >> 4

    @speedDv.setter
    def speedDv(self, value):
        value = min(15, value)
        value = max(0, value)
        byte = self.specialDv + (value << 4)
        self[self._speedDv] = byte

    @property
    def specialDv(self):
        return self[self._specialDv] & 0x0f

    @specialDv.setter
    def specialDv(self, value):
        value = min(15, value)
        value = max(0, value)
        byte = (self.speedDv << 4) + value
        self[self._specialDv] = byte

    @property
    def hpDv(self):
        return 8 * (self.attackDv % 2) + \
            4 * (self.defenseDv % 2) + \
            2 * (self.speedDv % 2) + \
            (self.specialDv % 2)

    @property
    def hp(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['hp'],
            self.hpDv,
            self.hpExp,
        ) + self.level + 10

    @property
    def attack(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['attack'],
            self.attackDv,
            self.attackExp,
        ) + 5

    @property
    def defense(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['defense'],
            self.defenseDv,
            self.defenseExp,
        ) + 5

    @property
    def spattack(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['sattack'],
            self.specialDv,
            self.specialExp,
        ) + 5

    @property
    def spdefense(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['sdefense'],
            self.specialDv,
            self.specialExp,
        ) + 5

    @property
    def speed(self):
        return self._statCalc(
            self.buff.baseStats(self.species)['speed'],
            self.speedDv,
            self.speedExp,
        ) + 5
