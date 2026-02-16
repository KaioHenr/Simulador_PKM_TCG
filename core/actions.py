from rules.constants import SETUP_LIMITS

def play_basics_from_hand(hand, table):
    for p in ["Snorunt", "Budew", "Munkidori", "Yveltal"]:
        while p in hand and table["bench"].count(p) < SETUP_LIMITS[p] and len(table["bench"]) < 5:
            hand.remove(p)
            table["bench"].append(p)


def use_poffin(hand, deck, table):
    if "Poffin" not in hand:
        return
    hand.remove("Poffin")

    for target in ["Snorunt", "Budew"]:
        if target in deck and table["bench"].count(target) < SETUP_LIMITS[target] and len(table["bench"]) < 5:
            deck.remove(target)
            table["bench"].append(target)
            return


def use_ball(hand, deck, table):
    for ball in ["NestBall", "UltraBall"]:
        if ball in hand:
            hand.remove(ball)
            for target in ["Munkidori", "Snorunt", "Budew", "Yveltal"]:
                if target in deck and table["bench"].count(target) < SETUP_LIMITS.get(target, 1) and len(table["bench"]) < 5:
                    deck.remove(target)
                    table["bench"].append(target)
                    return


def use_artazon(hand, deck, table):
    if "Artazon" not in hand:
        return
    hand.remove("Artazon")

    for target in ["Snorunt", "Budew", "Munkidori", "Yveltal"]:
        if target in deck and table["bench"].count(target) < SETUP_LIMITS.get(target, 1):
            deck.remove(target)
            table["bench"].append(target)
            return


def attach_energy(hand, table):
    if "Energy" in hand and "Munkidori" in table["bench"]:
        hand.remove("Energy")
        table["energy_on_munkidori"] = True
