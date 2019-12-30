import os

try:
    import aostats
except:
    class aostats:
        @staticmethod
        def initialize(_):
            return InitializationResult.NetworkInterfaceListMissing
        @staticmethod
        def stats(_):
            return {
                'players': [],
                'main': None
            }

from .config import config
from .number import Number

TESTING_ENABLED = bool(os.getenv('TESTING'))


class StatType:
    Unknown = 0
    LastFight = 1
    Zone = 2
    Overall = 3

class InitializationResult:
    Ok = 0
    UnknownFailure = 1
    NetworkInterfaceListMissing = 2

INITIALIZATION_RESULT = {
    0: InitializationResult.Ok,
    1: InitializationResult.UnknownFailure,
    2: InitializationResult.NetworkInterfaceListMissing
}

class DamageStat:
    def __init__(self, name, items, damage, time_in_combat, dps, percentage, best_damage):
        self.name = name
        self.items = items
        self.damage = Number(damage)
        self.time_in_combat = Number(time_in_combat)
        self.dps = Number(dps)
        self.percentage = Number(percentage)
        self.best_damage = Number(best_damage)

    def __str__(self):
        return "Name {} Damage {} DPS {} percentage {}".format(self.name, self.damage, self.dps, self.percentage)

    def __eq__(self, other):
        return self.name == other.name and self.damage == other.damage and self.time_in_combat == other.time_in_combat and self.dps == other.dps


class FameStat:
    def __init__(self, fame, fame_per_minute):
        self.fame = fame
        self.fame_per_minute = fame_per_minute


def stats(session, with_dmg=False):
    players = session['players']
    main_player = session['main']

    with_damage = [s for s in players if s['damage'] != 0.0] if with_dmg else players
    extended_session = with_percentage(with_damage)
    statistics = [DamageStat(
        s['player'],
        s['items'],
        s['damage'], 
        s['time_in_combat'], 
        s['dps'], 
        s['dmg_percentage'], 
        s['best_damage']) for s in extended_session]

    elapsed = 0
    fame = FameStat(Number(0.0), Number(0.0))
    if main_player:
        if 'fame' in main_player:
            fame = FameStat(Number(main_player['fame']), Number(main_player['fame_per_minute']))
        if 'seconds_in_game' in main_player:
            elapsed = main_player['seconds_in_game']

    return statistics, fame, elapsed


def with_percentage(session):
    best_damage = 0.0
    damage_done = 0.0
    for s in session:
        damage = s['damage']
        if damage > best_damage:
            best_damage = damage
        damage_done += damage

    for s in session:
        s['dmg_percentage'] = s['damage'] / damage_done * 100 if s['damage']  else 0.0
        s['best_damage'] = best_damage

    return session

def zone_stats(with_damage=False):
    if TESTING_ENABLED:
        session = {
            'players': [
            {'player': 'Arcane', 'damage': 200.0, 'time_in_combat': 12.0, 'dps': 142.4234, 'fame': 20.0, 'fame_per_minute': 30, 'items': {
                'weapon': 'T4_MAIN_ARCANESTAFF@3'
            }},
            {'player': 'Cursed', 'damage': 1100.0, 'time_in_combat': 12.0, 'dps': 222, 'items': {
                'weapon': 'T5_MAIN_CURSEDSTAFF@2'
            }},
            {'player': 'Fire', 'damage': 775.0, 'time_in_combat': 12.0, 'dps': 132, 'items': {
                'weapon': 'T5_MAIN_FIRESTAFF@1'
            }},
            {'player': 'Frost', 'damage': 2800.0, 'time_in_combat': 12.0, 'dps': 743, 'items': {
                'weapon': 'T5_MAIN_FROSTSTAFF@1'
            }},
            {'player': 'Holy', 'damage': 500.0, 'time_in_combat': 12.0, 'dps': 99, 'items': {
                'weapon': 'T6_MAIN_HOLYSTAFF'
            }},
            {'player': 'Nature', 'damage': 500.0, 'time_in_combat': 12.0, 'dps': 123, 'items': {
                'weapon': 'T8_MAIN_NATURESTAFF@3'
            }},
            {'player': 'Axe', 'damage': 2430.0, 'time_in_combat': 120.0, 'dps': 631, 'items': {
                'weapon': 'T8_MAIN_AXE'
            }},
            {'player': 'Dagger', 'damage': 1900.0, 'time_in_combat': 12.0, 'dps': 551, 'items': {
                'weapon': 'T8_MAIN_DAGGER@2'
            }},
            {'player': 'Hammer', 'damage': 500.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T7_MAIN_HAMMER@2'
            }},
            {'player': 'Mace', 'damage': 500.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T6_MAIN_MACE@2'
            }},
            {'player': 'Quarterstaff', 'damage': 250.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T5_2H_IRONCLADEDSTAFF'
            }},
            {'player': 'Spear', 'damage': 250.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T8_MAIN_SPEAR@2'
            }},
            {'player': 'Sword', 'damage': 250.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T7_2H_CLAYMORE@1'
            }},
            {'player': 'Bow', 'damage': 250.0, 'time_in_combat': 12.0, 'dps': 13, 'items': {
                'weapon': 'T8_2H_BOW'
            }},
            {'player': 'Crossbow', 'damage': 1800.0, 'time_in_combat': 450.0, 'dps': 450, 'items': {
                'weapon': 'T8_2H_CROSSBOWLARGE@3'
            }},
        ],
        'main': {'player': 'Crossbow', 'damage': 250.0, 'time_in_combat': 120000.0, 'dps': 13, 'items': {
                'weapon': 'T8_2H_CROSSBOWLARGE@3'
            }, 'fame': 2300000, 'fame_per_minute': 46000.0, 'seconds_in_game': 3000 }
        }
    else:
        session = aostats.stats(StatType.Zone)

    return stats(session, with_damage)


def overall_stats(with_damage=False):
    if TESTING_ENABLED:
        session = {'players': [
            {'player': 'overall', 'damage': 1000.0,
                'time_in_combat': 12.0, 'dps': 12.4234, 'items': {'weapon': 'T8_2H_CROSSBOWLARGE@3'}},
        ], 'main': {}}
    else:
        session = aostats.stats(StatType.Overall)

    return stats(session, with_damage)


def last_fight_stats(with_damage=False):
    if TESTING_ENABLED:
        session = {'players': [
            {'player': 'last', 'damage': 1000.0,
                'time_in_combat': 12.0, 'dps': 12.4234, 'items': {'weapon': 'T8_2H_CROSSBOWLARGE@3'}},
        ], 'main': {}}
    else:
        session = aostats.stats(StatType.LastFight)

    return stats(session, with_damage)

def reset_zone_stats():
    aostats.reset(StatType.Zone)

def reset_last_fight_stats():
    aostats.reset(StatType.LastFight)

def reset_stats():
    aostats.reset(StatType.Overall)

def initialize():
    if TESTING_ENABLED:
        return InitializationResult.Ok
    cfg = config()
    try:
        return INITIALIZATION_RESULT[aostats.initialize()]
    except:
        pass
