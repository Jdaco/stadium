#!/usr/bin/python2
import stadium.maps as maps
from stadium.domain import Pokemon, Moveset
import pytest
from mock import patch, Mock, MagicMock


class BufferMock(Mock):
    def __init__(self, values, *args, **kwargs):
        super(BufferMock, self).__init__(*args, **kwargs)

        self._v = values

    def __getitem__(self, index):
        return self._v[index]

    def __setitem__(self, index, value):
        self._v[index] = value

class TestPokemon:
    def setup_method(self):
        self.buff = BufferMock([
            1,    # Level
            100,  # Species
            0,    
            0,
            101,  # Move 1
            102,  # Move 2
            103,  # Move 3
            104,  # Move 4
            0,
            50,   # Happiness
            60,   # HP Exp 1
            61,   # HP EXP 2
            62,   # Attack Exp 1
            63,   # Attack Exp 2
            64,   # Defense Exp 1
            65,   # Defense Exp 2
            66,   # Speed Exp 1
            67,   # Speed Exp 2
            68,   # Special Exp 1
            69,   # Special Exp 2
            0xab,   # Attack DV / Defense DV
            0xab,   # Speed DV / Special DV
        ])
        self.sut = Pokemon(
            self.buff, 0
        )

    def test_level_above_100(self):
        self.sut.level = 200

        assert self.sut.level == 100

    def test_level_below_1(self):
        self.sut.level = 0

        assert self.sut.level == 1

    def test_happiness_above_255(self):
        self.sut.happiness = 300

        assert self.sut.happiness == 0xFF

    def test_happiness_below_0(self):
        self.sut.happiness = -1

        assert self.sut.happiness == 0

    def test_hpExp_above_ffff(self):
        self.sut.hpExp = 0xFFFF5

        assert self.sut.hpExp == 0xFFFF

    def test_hpExp_below_0(self):
        self.sut.hpExp = -1

        assert self.sut.hpExp == 0

    def test_attackExp_above_ffff(self):
        self.sut.attackExp = 0xFFFF5

        assert self.sut.attackExp == 0xFFFF

    def test_attackExp_below_0(self):
        self.sut.attackExp = -1

        assert self.sut.attackExp == 0

    def test_defenseExp_above_ffff(self):
        self.sut.defenseExp = 0xFFFF5

        assert self.sut.defenseExp == 0xFFFF

    def test_defenseExp_below_0(self):
        self.sut.defenseExp = -1

        assert self.sut.defenseExp == 0

    def test_speedExp_above_ffff(self):
        self.sut.speedExp = 0xFFFF5

        assert self.sut.speedExp == 0xFFFF

    def test_speedExp_below_0(self):
        self.sut.speedExp = -1

        assert self.sut.speedExp == 0

    def test_specialExp_above_ffff(self):
        self.sut.specialExp = 0xFFFF5

        assert self.sut.specialExp == 0xFFFF

    def test_specialExp_below_0(self):
        self.sut.specialExp = -1

        assert self.sut.specialExp == 0

    def test_hp_calc(self):
        self.buff.baseStats = Mock(return_value = {'hp': 35})

        self.sut.attackDv = 8
        self.sut.defenseDv = 13
        self.sut.specialDv = 9
        self.sut.speedDv = 5
        self.sut.hpExp = 22850
        self.sut.level = 81

        value = self.sut.hp

        assert self.sut.hpDv == 7
        assert value == 189
        self.buff.baseStats.assert_called_once()

    def test_attack_calc(self):
        self.buff.baseStats = Mock(return_value = {'attack': 55})

        self.sut.attackDv = 8
        self.sut.attackExp = 23140
        self.sut.level = 81

        value = self.sut.attack

        assert value == 137
        self.buff.baseStats.assert_called_once()
        
    def test_defense_calc(self):
        self.buff.baseStats = Mock(return_value = {'defense': 30})

        self.sut.defenseDv = 13
        self.sut.defenseExp = 17280
        self.sut.level = 81

        value = self.sut.defense

        assert value == 100
        self.buff.baseStats.assert_called_once()
        
    def test_speed_calc(self):
        self.buff.baseStats = Mock(return_value = {'speed': 90})

        self.sut.speedDv = 5
        self.sut.speedExp = 24795
        self.sut.level = 81

        value = self.sut.speed

        assert value == 190
        self.buff.baseStats.assert_called_once()

    def test_special_attack_calc(self):
        self.buff.baseStats = Mock(return_value = {'sattack': 50})

        self.sut.specialDv = 9
        self.sut.specialExp = 19625
        self.sut.level = 81

        value = self.sut.spattack

        assert value == 128
        self.buff.baseStats.assert_called_once()

    def test_special_defense_calc(self):
        self.buff.baseStats = Mock(return_value = {'sdefense': 40})

        self.sut.specialDv = 9
        self.sut.specialExp = 19625
        self.sut.level = 81

        value = self.sut.spdefense

        assert value == 112
        self.buff.baseStats.assert_called_once()


    def test_max(self):
        self.sut.max()

        assert self.sut.level == 100
        assert self.sut.happiness == 0xFF
        assert self.sut.hpExp == 0xFFFF
        assert self.sut.attackExp == 0xFFFF
        assert self.sut.defenseExp == 0xFFFF
        assert self.sut.specialExp == 0xFFFF
        assert self.sut.speedExp == 0xFFFF
        assert self.sut.attackDv == 0xF
        assert self.sut.defenseDv == 0xF
        assert self.sut.specialDv == 0xF
        assert self.sut.speedDv == 0xF

    def test_hidden_power_get(self):
        self.sut.attackDv = 15
        self.sut.defenseDv = 15

        assert self.sut.hiddenPowerType == 'dark'

    def test_hidden_power_set(self):
        self.sut.attackDv = 1
        self.sut.defenseDv = 1
        self.sut.hiddenPowerType = 'dark'

        assert self.sut.attackDv == 3
        assert self.sut.defenseDv == 3

    def test_hidden_power_invalid(self):
        with pytest.raises(KeyError):
            self.sut.hiddenPowerType = 'not_a_type'

    def test_hidden_power_damage_msb_1(self):
        self.sut.specialDv = 15
        self.sut.speedDv = 15
        self.sut.defenseDv = 15
        self.sut.attackDv = 15

        value = self.sut.hiddenPowerDamage

        assert value == 70

    def test_hidden_power_damage_msb_0(self):
        self.sut.specialDv = 7
        self.sut.speedDv = 7
        self.sut.defenseDv = 7
        self.sut.attackDv = 7

        value = self.sut.hiddenPowerDamage

        assert value == 32

class TestMoveset:
    def setup_method(self):
        self.moves = [10, 20, 30, 40]
        self.buff = BufferMock( self.moves )
        self.sut = Moveset(self.buff, 0)

    def test_getitem_normal(self):
        index = 2
        move_name = 'fake move'
        maps.moves_reversed[
            self.moves[
                index
            ]
        ] = move_name
        value = self.sut[index]

        assert value == move_name

    def test_getitem_below_zero(self):
        with pytest.raises(IndexError):
            value = self.sut[-1]

    def test_getitem_above_three(self):
        with pytest.raises(IndexError):
            value = self.sut[4]

    def test_setitem_normal(self):
        index = 2
        move_name = 'fake_move'
        move_value = 123
        maps.moves[move_name] = move_value

        self.sut[index] = move_name

        assert self.buff[index] == move_value
        
    def test_setitem_below_zero(self):
        with pytest.raises(IndexError):
            self.sut[-1] = 'psychic'

    def test_setitem_above_three(self):
        with pytest.raises(IndexError):
            self.sut[4] = 'psychic'

    def test_setitem_invalid_move(self):
        with pytest.raises(ValueError):
            self.sut[0] = 'not a move'

    
