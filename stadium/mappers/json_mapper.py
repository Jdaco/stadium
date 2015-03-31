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
        poke.species = \
            str(i_poke[u'species'].lower())
        poke.moves[0] = \
            str(i_poke[u'move1'].lower()) \
            if u'move1' in i_poke \
            and i_poke[u'move1'] \
            else None
        poke.moves[1] = \
            str(i_poke[u'move2'].lower()) \
            if u'move2' in i_poke \
            and i_poke[u'move2'] \
            else None
        poke.moves[2] = \
            str(i_poke[u'move3'].lower()) \
            if u'move3' in i_poke \
            and i_poke[u'move3'] \
            else None
        poke.moves[3] = \
            str(i_poke[u'move4'].lower()) \
            if u'move4' in i_poke \
            and i_poke[u'move4'] \
            else None
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
        {'species': poke.species,
         'move1': poke.moves[0],
         'move2': poke.moves[1],
         'move3': poke.moves[2],
         'move4': poke.moves[3],
         'level': poke.level,
         'happiness': poke.happiness,
         'attackDv': poke.attackDv,
         'defenseDv': poke.defenseDv,
         'speedDv': poke.speedDv,
         'specialDv': poke.specialDv,
         'attackExp': poke.attackExp,
         'defenseExp': poke.defenseExp,
         'speedExp': poke.speedExp,
         'specialExp': poke.specialExp,
         'hpExp': poke.hpExp}

        for poke in buff.pokemon
    ]
    json.dump(exportedPokes, fp, indent=4)
