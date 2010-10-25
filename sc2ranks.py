#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A Python library for the sc2ranks.com API (ags 2010)

import urllib

# find a json parser
try:
    import json
    _json_parser = lambda s: json.loads(s)
except ImportError:
    # this should throw an exception if no json library can be found
    import simplejson
    _json_parser = lambda s: simplejson.loads(s)

class Character(object):
    '''Abstraction of a SC2 player and associated data'''

    def __init__(self, json):
        '''Constructs a Character from given JSON data. Any team data 
           will be converted into Team objects.
        '''
        for key in json:
            if key == 'teams':
                self.__dict__[key] = [Team(t) for t in json[key]]
                # only 1 team
                if len(self.__dict__[key]) == 1:
                    self.__dict__['team'] = self.__dict__[key][0]
            else:
                self.__dict__[key] = json[key]
    
    def __eq__(self, character):
        '''Compare characters based on unique battle.net ID'''
        try:
            return self.bnet_id == character.bnet_id
        except Exception:
            return False

    def __repr__(self):
        '''Returns a string of form name#character_code'''
        return '%s#%s' % (self.name, self.character_code)

class CharacterError(Exception):
    '''Base exception class for API returns'''
    pass

class Team(object):
    '''Abstraction of a SC2 team and associated data'''

    def __init__(self, json):
        '''Constructs a character from given JSON data. Any members
           of the team will be converted into Character objects'''
        for key in json:
            if key == 'members':
                self.__dict__[key] = [Character(c) for c in json[key]]
            else:
                self.__dict__[key] = json[key]

class SC2RanksAPI(object):
    base_url = "http://sc2ranks.com/api" # API base query url
    
    def __init__(self, app_key = 'sc2ranks Python API'):
        '''Constructs an API object with an optional application key.'''
        self.app_key = app_key
    
    def base_character(self, name, char_id, region='us'):
        '''Returns base character data, acheivement points, character 
           code and battle.net ID info.

           CharacterError raised if no such character exists.
        '''
        json = self.get('base/char/%s/%s$%s' % (region, name, char_id))
        return Character(json)

    def base_character_team(self, name, char_id, region='us'):
        '''Returns base character data and base data on the 
           player's teams.

           CharacterError raised if no such character exists.
        '''
        json = self.get('base/teams/%s/%s$%s' % (region, name, char_id))
        return Character(json)

    def extended_character_team(self, name, char_id, region='us',
                                bracket=0, random=0):
        '''Returns base character data and extended team information
           for a given bracket. To find random teams can be specified 
           through the random parameter.

           CharacterError raised if no such character exists.
        '''
        json = self.get('char/teams/%s/%s$%s/%s/%s' % 
                    (region, name, char_id, bracket, random))
        return Character(json)

    def mass_base_characters(self, characters):
        '''Pulls up to 100 characters at once.
           `characters` parameter is a list of dictionaries in
           the following form, either:

           {'bnet_id', 'region', 'name' } 
           or
           {'code', 'region', 'name'}
           where 'code' is the player's character code.

           Returns a list of Character objects.

           CharacterError raised if character does not match
           parameters or if more than 100 characters are passed.
        '''
        data = [('characters[%s][%s]' % (characters.index(c), k), c[k])
                for c in characters for k in c]
        json = self.get_encoded('mass/base/char/', data)
        return [Character(c) for c in json]

    def mass_base_characters_teams(self, characters, bracket=1, is_random=0):
        '''
        '''
        data = [('team[bracket]', bracket), ('team[is_random]', is_random)]
        data += [('characters[%s][%s]' % (characters.index(c), k), c[k])
                for c in characters for k in c]
        json = self.get_encoded('mass/base/teams/', data)
        return [Character(c) for c in json]

    def search(self, s_type, region, name, offset=0):
        '''Returns the battle.net ID and name of the first 10 
           characters that match the search criteria and the total 
           number of matches.

           `s_type` may be one of 'exact', 'contains', 'starts', 'ends'.
           `offset` may be specified to retrieve more characters.

           CharacterError raised if no characters match criteria.
        '''
        json = self.get('search/%s/%s/%s/%s' % (s_type, region, name, offset))
        result = {'total' : json['total']}
        result['characters'] = [Character(c) for c in json['characters']]
        return result

    def custom_division_list(self, div_id, region='all', league='all', 
                             bracket=1, random=0):
        '''Returns every team in a custom division.

           CharacterError raised if no characters have been added to
           the division or no such division exists.
        '''
        json = self.get('clist/%s/%s/%s/%s/%s' % 
                (div_id, region, league, bracket, random))
        return [Team(c) for c in json]

    def get(self, query):
        url = '%s/%s.json?appKey=%s' % (self.base_url, query, self.app_key)
        json = urllib.urlopen(url).read()
        result = _json_parser(json)
        if 'error' in result:
            raise CharacterError(result['error'])
        return result

    def get_encoded(self, url, data):
        enc_data = urllib.urlencode(data)
        url = urllib.urlopen('%s/%s?appKey=%s' % 
                            (self.base_url, url, self.app_key), enc_data)
        result = _json_parser(url.read())
        if 'error' in result:
            raise CharacterError(result['error'])
        return result
