from core.turn1 import turn_cycle, choose_active
from core.state import classify, auto_loss
from rules.constants import BASICS

def run(deck_builder, iterations):
    results = {"completo":0, "parcial":0, "incompleto":0, "auto_loss":0}

    for _ in range(iterations):
        deck = deck_builder()

        while True:
            hand = deck[:7]
            if any(c in BASICS for c in hand):
                break

        del deck[:7]
        table = {"active": choose_active(hand), "bench": [], "energy_on_munkidori": False}

        prizes = deck[:6]
        del deck[:6]

        if auto_loss(prizes):
            results["auto_loss"] += 1
            continue

        hand.append(deck.pop(0))
        turn_cycle(hand, deck, table)

        results[classify(table)] += 1

    return results
