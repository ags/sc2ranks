#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unit tests for sc2ranks.com API Python library

import unittest
import sc2ranks

class TestSC2RanksAPI(unittest.TestCase):
   
    def setUp(self):
        self.api = sc2ranks.SC2RanksAPI()

        tlo_team = {
            'division': u'Division Tal\u2019darim Theta'
        }
        
        socke_team = {
            'division': u'Division Feld Delta'
        }

        tlo = {
            'name': 'LiquidTLO',
            'character_code': 481,
            'region': 'eu',
            'bnet_id': 326029,
            'teams': [tlo_team]
        }

        socke = {
            'name': 'aTnSocke', 
            'region': 'eu', 
            'bnet_id': 172567,
            'character_code': 521,
            'teams': [socke_team]
        }

        self.tlo = sc2ranks.Character(tlo)
        self.socke = sc2ranks.Character(socke)

    def test_base_character(self):
        c = self.api.base_character(self.tlo.name, self.tlo.character_code,
                                    self.tlo.region)
        # simple check of battle.net id
        self.assertTrue(c == self.tlo)
        # check that other data is correct too
        self.assertEqual(c.character_code, self.tlo.character_code)
        self.assertEqual(c.name, self.tlo.name)
        self.assertEqual(c.region, self.tlo.region)

    def test_base_character_team(self):
        c = self.api.base_character_team(self.tlo.name, 
                                         self.tlo.character_code, 
                                         self.tlo.region)

        tlo_td = self.tlo.teams[0].division
        self.assertTrue(any(t.division == tlo_td for t in c.teams))

    def test_character_equal(self):
        self.assertTrue(self.tlo == self.tlo)

    def test_search(self):
        # successful search
        s = self.api.search('exact', self.tlo.region, self.tlo.name)
        self.assertTrue(self.tlo in s['characters'])

        # fail search
        self.assertRaises(sc2ranks.CharacterError, self.api.search, 
            'exact', 'us', '012fakename345')
    
    def test_mass_base_characters(self):
        data = [ {'name': self.tlo.name,
                  'region': self.tlo.region,
                  'bnet_id': self.tlo.bnet_id
                 },
                 {'name': self.socke.name,
                  'region': self.socke.region,
                  'code': self.socke.character_code
                 } ]
        l = self.api.mass_base_characters(data)
        self.assertTrue(self.tlo in l)
        self.assertTrue(self.socke in l)

    def test_mass_base_characters_teams(self):
        data = [ {'name': self.tlo.name,
                  'region': self.tlo.region,
                  'bnet_id': self.tlo.bnet_id
                 },
                 {'name': self.socke.name,
                  'region': self.socke.region,
                  'code': self.socke.character_code
                 } ]
        l = self.api.mass_base_characters_teams(data, 1, 0)
        self.assertTrue(self.tlo in l)
        self.assertTrue(self.socke in l)

        for player in [self.socke, self.tlo]:
            c = l[l.index(player)]
            td = player.teams[0].division
            self.assertTrue(any(t.division == td for t in c.teams))

    def test_custom_division_list(self):
        l = self.api.custom_division_list(1)

        self.assertTrue(any(self.socke in t.members for t in l))

if __name__ == '__main__':
    unittest.main()
