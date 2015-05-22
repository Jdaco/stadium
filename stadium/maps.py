import collections

pokemon = collections.OrderedDict((
    ('bulbasaur', 0x01,),
    ('ivysaur', 0x02,),
    ('venusaur', 0x03,),
    ('charmander', 0x04,),
    ('charmeleon', 0x05,),
    ('charizard', 0x06,),
    ('squirtle', 0x07,),
    ('wartortle', 0x08,),
    ('blastoise', 0x09,),
    ('caterpie', 0x0a,),
    ('metapod', 0x0b,),
    ('butterfree', 0x0c,),
    ('weedle', 0x0d,),
    ('kakuna', 0x0e,),
    ('beedrill', 0x0f,),
    ('pidgey', 0x10,),
    ('pidgeotto', 0x11,),
    ('pidgeot', 0x12,),
    ('rattata', 0x13,),
    ('raticate', 0x14,),
    ('spearow', 0x15,),
    ('fearow', 0x16,),
    ('ekans', 0x17,),
    ('arbok', 0x18,),
    ('pikachu', 0x19,),
    ('raichu', 0x1a,),
    ('sandshrew', 0x1b,),
    ('sandslash', 0x1c,),
    ('nidoran f', 0x1d,),
    ('nidorina', 0x1e,),
    ('nidoqueen', 0x1f,),
    ('nidoran m', 0x20,),
    ('nidorino', 0x21,),
    ('nidoking', 0x22,),
    ('clefairy', 0x23,),
    ('clefable', 0x24,),
    ('vulpix', 0x25,),
    ('ninetales', 0x26,),
    ('jigglypuff', 0x27,),
    ('wigglytuff', 0x28,),
    ('zubat', 0x29,),
    ('golbat', 0x2a,),
    ('oddish', 0x2b,),
    ('gloom', 0x2c,),
    ('vileplume', 0x2d,),
    ('paras', 0x2e,),
    ('parasect', 0x2f,),
    ('venonat', 0x30,),
    ('venomoth', 0x31,),
    ('diglett', 0x32,),
    ('dugtrio', 0x33,),
    ('meowth', 0x34,),
    ('persian', 0x35,),
    ('psyduck', 0x36,),
    ('golduck', 0x37,),
    ('mankey', 0x38,),
    ('primeape', 0x39,),
    ('growlithe', 0x3a,),
    ('arcanine', 0x3b,),
    ('poliwag', 0x3c,),
    ('poliwhirl', 0x3d,),
    ('poliwrath', 0x3e,),
    ('abra', 0x3f,),
    ('kadabra', 0x40,),
    ('alakazam', 0x41,),
    ('machop', 0x42,),
    ('machoke', 0x43,),
    ('machamp', 0x44,),
    ('bellsprout', 0x45,),
    ('weepinbell', 0x46,),
    ('victreebell', 0x47,),
    ('tentacool', 0x48,),
    ('tentacruel', 0x49,),
    ('geodude', 0x4a,),
    ('graveler', 0x4b,),
    ('golem', 0x4c,),
    ('ponyta', 0x4d,),
    ('rapidash', 0x4e,),
    ('slowpoke', 0x4f,),
    ('slowbro', 0x50,),
    ('magnemite', 0x51,),
    ('magneton', 0x52,),
    ('farfetch\'d', 0x53,),
    ('doduo', 0x54,),
    ('dodrio', 0x55,),
    ('seel', 0x56,),
    ('dewgong', 0x57,),
    ('grimer', 0x58,),
    ('muk', 0x59,),
    ('shellder', 0x5a,),
    ('cloyster', 0x5b,),
    ('gastly', 0x5c,),
    ('haunter', 0x5d,),
    ('gengar', 0x5e,),
    ('onix', 0x5f,),
    ('drowzee', 0x60,),
    ('hypno', 0x61,),
    ('krabby', 0x62,),
    ('kingler', 0x63,),
    ('voltorb', 0x64,),
    ('electrode', 0x65,),
    ('exeggcute', 0x66,),
    ('exeggutor', 0x67,),
    ('cubone', 0x68,),
    ('marowak', 0x69,),
    ('hitmonlee', 0x6a,),
    ('hitmonchan', 0x6b,),
    ('lickitung', 0x6c,),
    ('koffing', 0x6d,),
    ('weezing', 0x6e,),
    ('rhyhorn', 0x6f,),
    ('rhydon', 0x70,),
    ('chansey', 0x71,),
    ('tangela', 0x72,),
    ('kangaskhan', 0x73,),
    ('horsea', 0x74,),
    ('seadra', 0x75,),
    ('goldeen', 0x76,),
    ('seaking', 0x77,),
    ('staryu', 0x78,),
    ('starmie', 0x79,),
    ('mr. mime', 0x7a,),
    ('scyther', 0x7b,),
    ('jynx', 0x7c,),
    ('electabuzz', 0x7d,),
    ('magmar', 0x7e,),
    ('pinsir', 0x7f,),
    ('tauros', 0x80,),
    ('magikarp', 0x81,),
    ('gyarados', 0x82,),
    ('lapras', 0x83,),
    ('ditto', 0x84,),
    ('eevee', 0x85,),
    ('vaporeon', 0x86,),
    ('jolteon', 0x87,),
    ('flareon', 0x88,),
    ('porygon', 0x89,),
    ('omanyte', 0x8a,),
    ('omastar', 0x8b,),
    ('kabuto', 0x8c,),
    ('kabutops', 0x8d,),
    ('aerodactyl', 0x8e,),
    ('snorlax', 0x8f,),
    ('articuno', 0x90,),
    ('zapdos', 0x91,),
    ('moltres', 0x92,),
    ('dratini', 0x93,),
    ('dragonair', 0x94,),
    ('dragonite', 0x95,),
    ('mewtwo', 0x96,),
    ('mew', 0x97,),
    ('chikorita', 0x98,),
    ('bayleef', 0x99,),
    ('meganium', 0x9a,),
    ('cyndaquil', 0x9b,),
    ('quilava', 0x9c,),
    ('typhlosion', 0x9d,),
    ('totodile', 0x9e,),
    ('croconaw', 0x9f,),
    ('feraligatr', 0xa0,),
    ('sentret', 0xa1,),
    ('furret', 0xa2,),
    ('hoothoot', 0xa3,),
    ('noctowl', 0xa4,),
    ('ledyba', 0xa5,),
    ('ledian', 0xa6,),
    ('spinarak', 0xa7,),
    ('ariados', 0xa8,),
    ('crobat', 0xa9,),
    ('chinchou', 0xaa,),
    ('lanturn', 0xab,),
    ('pichu', 0xac,),
    ('cleffa', 0xad,),
    ('igglybuff', 0xae,),
    ('togepi', 0xaf,),
    ('togetic', 0xb0,),
    ('natu', 0xb1,),
    ('xatu', 0xb2,),
    ('mareep', 0xb3,),
    ('flaafy', 0xb4,),
    ('ampharos', 0xb5,),
    ('bellossom', 0xb6,),
    ('marill', 0xb7,),
    ('azumarill', 0xb8,),
    ('sudowoodo', 0xb9,),
    ('politoed', 0xba,),
    ('hoppip', 0xbb,),
    ('skiploom', 0xbc,),
    ('jumpluff', 0xbd,),
    ('aipom', 0xbe,),
    ('sunkern', 0xbf,),
    ('sunflora', 0xc0,),
    ('yanma', 0xc1,),
    ('wooper', 0xc2,),
    ('quagsire', 0xc3,),
    ('espeon', 0xc4,),
    ('umbreon', 0xc5,),
    ('murkrow', 0xc6,),
    ('slowking', 0xc7,),
    ('misdreavus', 0xc8,),
    ('unown', 0xc9,),
    ('wobbuffet', 0xca,),
    ('girafarig', 0xcb,),
    ('pineco', 0xcc,),
    ('forretress', 0xcd,),
    ('dunsparce', 0xce,),
    ('gligar', 0xcf,),
    ('steelix', 0xd0,),
    ('snubbull', 0xd1,),
    ('granbull', 0xd2,),
    ('qwilfish', 0xd3,),
    ('scizor', 0xd4,),
    ('shuckle', 0xd5,),
    ('heracross', 0xd6,),
    ('sneasel', 0xd7,),
    ('teddiursa', 0xd8,),
    ('ursaring', 0xd9,),
    ('slugma', 0xda,),
    ('magcargo', 0xdb,),
    ('swinub', 0xdc,),
    ('piloswine', 0xdd,),
    ('corsola', 0xde,),
    ('remoraid', 0xdf,),
    ('octillery', 0xe0,),
    ('delibird', 0xe1,),
    ('mantine', 0xe2,),
    ('skarmory', 0xe3,),
    ('houndour', 0xe4,),
    ('houndoom', 0xe5,),
    ('kingdra', 0xe6,),
    ('phanpy', 0xe7,),
    ('donphan', 0xe8,),
    ('porygon2', 0xe9,),
    ('stantler', 0xea,),
    ('smeargle', 0xeb,),
    ('tyrogue', 0xec,),
    ('hitmontop', 0xed,),
    ('smoochum', 0xee,),
    ('elekid', 0xef,),
    ('magby', 0xf0,),
    ('miltank', 0xf1,),
    ('blissey', 0xf2,),
    ('raikou', 0xf3,),
    ('entei', 0xf4,),
    ('suicune', 0xf5,),
    ('larvitar', 0xf6,),
    ('pupitar', 0xf7,),
    ('tyranitar', 0xf8,),
    ('lugia', 0xf9,),
    ('ho-oh', 0xfa,),
    ('celebi', 0xfb,),
))

moves = {
    'pound': 0x01,
    'karate chop': 0x02,
    'doubleslap': 0x03,
    'comet punch': 0x04,
    'mega punch': 0x05,
    'pay day': 0x06,
    'fire punch': 0x07,
    'ice punch': 0x08,
    'thunderpunch': 0x09,
    'scratch': 0x0a,
    'vicegrip': 0x0b,
    'guillotine': 0x0c,
    'razor wind': 0x0d,
    'swords dance': 0x0e,
    'cut': 0x0f,
    'gust': 0x10,
    'wing attack': 0x11,
    'whirlwind': 0x12,
    'fly': 0x13,
    'bind': 0x14,
    'slam': 0x15,
    'vine whip': 0x16,
    'stomp': 0x17,
    'double kick': 0x18,
    'mega kick': 0x19,
    'jump kick': 0x1a,
    'rolling kick': 0x1b,
    'sand attack': 0x1c,
    'headbutt': 0x1d,
    'horn attack': 0x1e,
    'fury attack': 0x1f,
    'horn drill': 0x20,
    'tackle': 0x21,
    'body slam': 0x22,
    'wrap': 0x23,
    'take down': 0x24,
    'thrash': 0x25,
    'double-edge': 0x26,
    'tail whip': 0x27,
    'poison sting': 0x28,
    'twineedle': 0x29,
    'pin missle': 0x2a,
    'leer': 0x2b,
    'bite': 0x2c,
    'growl': 0x2d,
    'roar': 0x2e,
    'sing': 0x2f,
    'supersonic': 0x30,
    'sonicboom': 0x31,
    'disable': 0x32,
    'acid': 0x33,
    'ember': 0x34,
    'flamethrower': 0x35,
    'mist': 0x36,
    'water gun': 0x37,
    'hydro pump': 0x38,
    'surf': 0x39,
    'ice beam': 0x3a,
    'blizzard': 0x3b,
    'psybeam': 0x3c,
    'bubblebeam': 0x3d,
    'aurora beam': 0x3e,
    'hyper beam': 0x3f,
    'peck': 0x40,
    'drill peck': 0x41,
    'submission': 0x42,
    'low kick': 0x43,
    'counter': 0x44,
    'seismic toss': 0x45,
    'strength': 0x46,
    'absorb': 0x47,
    'mega drain': 0x48,
    'leech seed': 0x49,
    'growth': 0x4a,
    'razor leaf': 0x4b,
    'solar beam': 0x4c,
    'poisonpowder': 0x4d,
    'stun spore': 0x4e,
    'sleep powder': 0x4f,
    'petal dance': 0x50,
    'string shot': 0x51,
    'dragon rage': 0x52,
    'fire spin': 0x53,
    'thundershock': 0x54,
    'thunderbolt': 0x55,
    'thunder wave': 0x56,
    'thunder': 0x57,
    'rock throw': 0x58,
    'earthquake': 0x59,
    'fissure': 0x5a,
    'dig': 0x5b,
    'toxic': 0x5c,
    'confusion': 0x5d,
    'psychic': 0x5e,
    'hypnosis': 0x5f,
    'meditate': 0x60,
    'agility': 0x61,
    'quick attack': 0x62,
    'rage': 0x63,
    'teleport': 0x64,
    'night shade': 0x65,
    'mimic': 0x66,
    'screech': 0x67,
    'double team': 0x68,
    'recover': 0x69,
    'harden': 0x6a,
    'minimize': 0x6b,
    'smokescreen': 0x6c,
    'confuse ray': 0x6d,
    'withdraw': 0x6e,
    'defense curl': 0x6f,
    'barrier': 0x70,
    'light screen': 0x71,
    'haze': 0x72,
    'reflect': 0x73,
    'focus energy': 0x74,
    'bide': 0x75,
    'metronome': 0x76,
    'mirror move': 0x77,
    'selfdestruct': 0x78,
    'egg bomb': 0x79,
    'lick': 0x7a,
    'smog': 0x7b,
    'sludge': 0x7c,
    'bone club': 0x7d,
    'fire blast': 0x7e,
    'waterfall': 0x7f,
    'clamp': 0x80,
    'swift': 0x81,
    'skull bash': 0x82,
    'spike cannon': 0x83,
    'constrict': 0x84,
    'amnesia': 0x85,
    'kinesis': 0x86,
    'softboiled': 0x87,
    'hi jump kick': 0x88,
    'glare': 0x89,
    'dream eater': 0x8a,
    'poison gas': 0x8b,
    'barrage': 0x8c,
    'leech life': 0x8d,
    'lovely kiss': 0x8e,
    'sky attack': 0x8f,
    'transform': 0x90,
    'bubble': 0x91,
    'dizzy punch': 0x92,
    'spore': 0x93,
    'flash': 0x94,
    'psywave': 0x95,
    'splash': 0x96,
    'acid armor': 0x97,
    'crabhammer': 0x98,
    'explosion': 0x99,
    'fury swipes': 0x9a,
    'bonemerang': 0x9b,
    'rest': 0x9c,
    'rock slide': 0x9d,
    'hyper fang': 0x9e,
    'sharpen': 0x9f,
    'conversion': 0xa0,
    'tri attack': 0xa1,
    'super fang': 0xa2,
    'slash': 0xa3,
    'substitute': 0xa4,
    'struggle': 0xa5,
    'sketch': 0xa6,
    'triple kick': 0xa7,
    'thief': 0xa8,
    'spider web': 0xa9,
    'mind reader': 0xaa,
    'nightmare': 0xab,
    'flame wheel': 0xac,
    'snore': 0xad,
    'curse': 0xae,
    'flail': 0xaf,
    'conversion2': 0xb0,
    'aeroblast': 0xb1,
    'cotton spore': 0xb2,
    'reversal': 0xb3,
    'spite': 0xb4,
    'powder snow': 0xb5,
    'protect': 0xb6,
    'mach punch': 0xb7,
    'scary face': 0xb8,
    'faint attack': 0xb9,
    'sweet kiss': 0xba,
    'belly drum': 0xbb,
    'sludge bomb': 0xbc,
    'mud-slap': 0xbd,
    'octazooka': 0xbe,
    'spikes': 0xbf,
    'zap cannon': 0xc0,
    'foresight': 0xc1,
    'destiny bond': 0xc2,
    'perish song': 0xc3,
    'icy wind': 0xc4,
    'detect': 0xc5,
    'bone rush': 0xc6,
    'lock-on': 0xc7,
    'outrage': 0xc8,
    'sandstorm': 0xc9,
    'giga drain': 0xca,
    'endure': 0xcb,
    'charm': 0xcc,
    'rollout': 0xcd,
    'false swipes': 0xce,
    'swagger': 0xcf,
    'milk drink': 0xd0,
    'spark': 0xd1,
    'fury cutter': 0xd2,
    'steel wing': 0xd3,
    'mean look': 0xd4,
    'attract': 0xd5,
    'sleep talk': 0xd6,
    'heal bell': 0xd7,
    'return': 0xd8,
    'present': 0xd9,
    'frustration': 0xda,
    'safeguard': 0xdb,
    'pain split': 0xdc,
    'sacred fire': 0xdd,
    'magnitude': 0xde,
    'dynamicpunch': 0xdf,
    'megahorn': 0xe0,
    'dragonbreath': 0xe1,
    'baton pass': 0xe2,
    'encore': 0xe3,
    'pursuit': 0xe4,
    'rapid spin': 0xe5,
    'sweet scent': 0xe6,
    'iron tail': 0xe7,
    'metal claw': 0xe8,
    'vital throw': 0xe9,
    'morning sun': 0xea,
    'synthesis': 0xeb,
    'moonlight': 0xec,
    'hidden power': 0xed,
    'cross chop': 0xee,
    'twister': 0xef,
    'rain dance': 0xf0,
    'sunny day': 0xf1,
    'crunch': 0xf2,
    'mirror coat': 0xf3,
    'psych up': 0xf4,
    'extremespeed': 0xf5,
    'ancientpower': 0xf6,
    'shadow ball': 0xf7,
    'future sight': 0xf8,
    'rock smash': 0xf9,
    'whirlpool': 0xfa,
    'beat up': 0xfb,
}

hidden_power = {
    'fighting': (0, 0),
    'flying': (0, 1),
    'poison': (0, 2),
    'ground': (0, 3),
    'rock': (1, 0),
    'bug': (1, 1),
    'ghost': (1, 2),
    'steel': (1, 3),
    'fire': (2, 0),
    'water': (2, 1),
    'grass': (2, 2),
    'electric': (2, 3),
    'psychic': (3, 0),
    'ice': (3, 1),
    'dragon': (3, 2),
    'dark': (3, 3),
}

pokemon_reversed = dict((
    (value, key) for key, value in pokemon.iteritems()
))
moves_reversed = dict((
    (value, key) for key, value in moves.iteritems()
))
hidden_power_reversed = dict((
    (value, key) for key, value in hidden_power.iteritems()
))
