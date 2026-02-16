import random
from rules.constants import ACTIVE_PRIORITY, BASICS
from core.actions import *
from core.state import classify

def choose_active(hand):
    for p in ACTIVE_PRIORITY:
        if p in hand:
            hand.remove(p)
            return p


def pokegear_priority(table):
    return ["Lillie", "Arven", "Kissera", "Xerosic"] if classify(table) == "completo" \
           else ["Arven", "Lillie", "Kissera", "Xerosic"]


def use_pokegear(hand, deck, table):
    if "Pokégear" not in hand:
        return
    hand.remove("Pokégear")

    top = deck[:7]
    for sup in pokegear_priority(table):
        if sup in top:
            hand.append(sup)
            deck.remove(sup)
            return


def turn_cycle(hand, deck, table, supporter_used=False):
    play_basics_from_hand(hand, table)

    while "Poffin" in hand:
        use_poffin(hand, deck, table)

    while "NestBall" in hand or "UltraBall" in hand:
        use_ball(hand, deck, table)

    use_artazon(hand, deck, table)
    use_pokegear(hand, deck, table)
    attach_energy(hand, table)

    if supporter_used:
        return

    if "Arven" in hand:
        hand.remove("Arven")
        for item in ["Poffin", "NestBall", "UltraBall"]:
            if item in deck:
                deck.remove(item)
                hand.append(item)
                break
        turn_cycle(hand, deck, table, True)

    elif "Lillie" in hand:
        hand.remove("Lillie")
        random.shuffle(deck)
        hand[:] = deck[:8]
        del deck[:8]
        turn_cycle(hand, deck, table, True)

    elif "Kissera" in hand:
        hand.remove("Kissera")
        hand[:] = deck[:6]
        del deck[:6]
        turn_cycle(hand, deck, table, True)
