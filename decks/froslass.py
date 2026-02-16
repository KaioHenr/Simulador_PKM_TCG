import random

def build():
    deck = (
        ["Munkidori"]*4 +
        ["Snorunt"]*3 +
        ["Froslass"]*3 +
        ["Budew"]*3 +
        ["Yveltal"]*1 +
        ["Psyduck"]*1 +

        ["Arven"]*4 +
        ["Lillie"]*4 +
        ["Kissera"]*3 +
        ["Xerosic"]*2 +

        ["Poffin"]*3 +
        ["NestBall"]*3 +
        ["UltraBall"]*2 +
        ["NightStretcher"]*2 +
        ["CounterCatcher"]*3 +
        ["Pokégear"]*2 +
        ["EarthVessel"]*1 +
        ["UnfairStamp"]*1 +
        ["SuperRod"]*1 +
        ["TM_Devolution"]*2 +
        ["BraveryCharm"]*1 +
        ["RescueBoard"]*1 +

        ["Artazon"]*1 +
        ["RocketWatchtower"]*2 +

        ["Energy"]*7
    )

    assert len(deck) == 60
    random.shuffle(deck)
    return deck

NAME = "2 Pokégear 3 Snorunt"
