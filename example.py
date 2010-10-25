#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Example usage of library

import sc2ranks

huk_name = 'HuK'
huk_code = 530

# create api instance with a custom key
api = sc2ranks.SC2RanksAPI(app_key='sc2ranks example')

# get HuK's basic data and basic team data.
# 'us' is the default for optional region parameter 
# and not specified here.
huk = api.base_character_team(huk_name, huk_code)

# HuK's acheivement points
print huk.name, huk.achievement_points

# HuK's 1v1 ranking could be retrieved like so:

# go through HuK's teams
for team in huk.teams:
    # find his 1v1 team
    if team.bracket == 1:
        print team.region_rank, team.world_rank

# or like this:

huk = api.extended_character_team(huk_name, huk_code, bracket=1)

print huk.name, '\'s 1v1 division name is', huk.team.division

# if the player has multiple teams, ie. 2v2 teams, 
# the 'team' attribute is not created and you must
# use 'teams'

# find out HuK's 2v2 buddies

# default to no random teams, set with random=1
huk = api.extended_character_team(huk_name, huk_code, bracket=2)

print huk.name, 'plays 2v2 with:'
for team in huk.teams:
    for member in team.members:
        # Characters are compared based on battle.net ID
        if member != huk:
            # repr of Character object is 'name$code' string
            print member
