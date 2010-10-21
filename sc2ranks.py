#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

# find a json parser
try:
    import json
    _json_parser = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _json_parser = lambda s: simplejson.loads(s)
    except:
        pass

class Character(object):
    def __init__(self, json):
        for key in json:
            if key == 'teams':
                self.__dict__[key] = [Team(t) for t in json[key]]
            else:
                self.__dict__[key] = json[key]

class CharacterError(Exception):
    pass

class Team(object):
    def __init__(self, json):
        for key in json:
            if key == 'members':
                self.__dict__[key] = [Character(c) for c in json[key]]
            else:
                self.__dict__[key] = json[key]

class SC2RanksAPI(object):
    base_url = "http://sc2ranks.com/api/"
    
    def __init__(self, app_key = 'sc2ranks Python API'):
        self.app_key = app_key
    
    def base_character(self, name, char_id, region = 'us'):
        json = self.get('base/char/%s/%s$%s' % (region, name, char_id))
        return Character(json)

    def base_character_team(self, name, char_id, region = 'us'):
        json = self.get('base/teams/%s/%s$%s' % (region, name, char_id))
        return Character(json)

    def extended_character_team(self, name, char_id, bracket=0, 
                                region='us', random=0):
        json = self.get('char/teams/%s/%s$%s/%s/%s' % 
                    (region, name, char_id, bracket, random))
        return Character(json)

    def search(self, s_type, region, name, offset=0):
        json = self.get('search/%s/%s/%s/%s' % (s_type, region, name, offset))
        result = { 'total' : json['total'] }
        result['characters'] = [Character(c) for c in json['characters']]
        return result

    def custom_division_list(self, div_id, region='all', league='all', 
                             bracket=1, random=0):
        json = self.get('clist/%s/%s/%s/%s/%s' % 
                (div_id, region, league, bracket, random))
        return [Team(c) for c in json]

    def get(self, query):
        url = self.base_url + query + '.json?appKey=' + self.app_key
        json = urllib.urlopen(url).read()
        result = _json_parser(json)
        if 'error' in result:
            raise CharacterError(result['error'])
        return result

if __name__ == '__main__':
    s = SC2RanksAPI()
#    c = s.base_character(name='ags', bnet_id='495', region='sea')
#    c = s.base_character_team(name='ags', bnet_id='495', region='sea')
