from collections import OrderedDict
import itertools
import json
from stadium import maps

def load(fp, buff):
    importedPokes = sorted(
        json.load(fp),
        cmp=(
            lambda x, y: cmp(
                maps.pokemon[str(x[u'species']).lower()],
                maps.pokemon[str(y[u'species']).lower()]
            )
        )
    )
    for poke, i_poke in itertools.izip(buff.pokemon, importedPokes):
        for index, move in enumerate(i_poke[u'moves']):
            poke.moves[index] = str(move).lower() \
                if move else None
        poke.species = \
            str(i_poke[u'species'].lower())
        poke.level = i_poke[u'level']
        poke.happiness = i_poke[u'happiness']
        poke.attackDv = i_poke[u'attackDv']
        poke.defenseDv = i_poke[u'defenseDv']
        poke.speedDv = i_poke[u'speedDv']
        poke.specialDv = i_poke[u'specialDv']
        poke.attackExp = i_poke[u'attackExp']
        poke.defenseExp = i_poke[u'defenseExp']
        poke.speedExp = i_poke[u'speedExp']
        poke.specialExp = i_poke[u'specialExp']
        poke.hpExp = i_poke[u'hpExp']


def dump(fp, buff):
    exportedPokes = [
        OrderedDict((
            ('species', poke.species),
            ('moves', list(poke.moves)),
            ('level', poke.level),
            ('happiness', poke.happiness),
            ('attackDv', poke.attackDv),
            ('defenseDv', poke.defenseDv),
            ('speedDv', poke.speedDv),
            ('specialDv', poke.specialDv),
            ('attackExp', poke.attackExp),
            ('defenseExp', poke.defenseExp),
            ('speedExp', poke.speedExp),
            ('specialExp', poke.specialExp),
            ('hpExp', poke.hpExp)
        ))
        for poke in buff.pokemon
    ]
    json.dump(exportedPokes, fp, indent=4)
