import random

# ---------------- CONFIGURAÇÕES ----------------

ACTIVE_PRIORITY = ["Budew", "Yveltal", "Munkidori", "Snorunt", "Psyduck"]

SETUP_LIMITS = {
    "Snorunt": 2,
    "Budew": 2,
    "Munkidori": 1,
    "Yveltal": 1
}

BASICS = {"Snorunt", "Budew", "Munkidori", "Yveltal", "Psyduck"}

# ---------------- DECK ----------------

def build_deck():
    deck = (
        # ===== POKÉMON =====
        ["Munkidori"]*4 +
        ["Snorunt"]*3 +
        ["Froslass"]*3 +
        ["Budew"]*3 +
        ["Yveltal"]*1 +
        ["Psyduck"]*1 +

        # ===== APOIADORES =====
        ["Arven"]*4 +
        ["Lillie"]*4 +
        ["Kissera"]*3 +
        ["Xerosic"]*2 +

        # ===== ITENS =====
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

        # ===== ESTÁDIOS =====
        ["Artazon"]*1 +
        ["RocketWatchtower"]*2 +

        # ===== ENERGIAS =====
        ["Energy"]*7 
    )

    assert len(deck) == 60, f"Deck inválido: {len(deck)} cartas"

    random.shuffle(deck)
    return deck

# ---------------- FUNÇÕES AUXILIARES ----------------

def choose_active(hand):
    for p in ACTIVE_PRIORITY:
        if p in hand:
            hand.remove(p)
            return p
    return None

def auto_loss(prizes):
    return (
        prizes.count("Snorunt") >= 3 or
        prizes.count("Budew") >= 3 or
        prizes.count("Munkidori") >= 4 or
        prizes.count("Froslass") >= 3
    )

def pokegear_priority(table):
    state = classify(table)
    if state == "completo":
        return ["Lillie", "Arven", "Kissera", "Xerosic"]
    else:
        return ["Arven", "Lillie", "Kissera", "Xerosic"]

def print_report(results, iterations, label):
    completo = results["completo"]
    parcial = results["parcial"]
    incompleto = results["incompleto"]
    auto_loss = results["auto_loss"]

    bricks = incompleto + auto_loss
    jogos_ok = completo + parcial

    print("\n" + "="*50)
    print(f"BUILD: {label}")
    print("="*50)

    print(f"Total de partidas: {iterations:,}")

    print("\n--- RESULTADOS ABSOLUTOS ---")
    print(f"Setup completo : {completo:,}")
    print(f"Setup parcial  : {parcial:,}")
    print(f"Incompleto     : {incompleto:,}")
    print(f"Auto-loss      : {auto_loss:,}")

    print("\n--- PERCENTUAIS ---")
    print(f"Setup completo : {completo/iterations*100:.2f}%")
    print(f"Setup parcial  : {parcial/iterations*100:.2f}%")
    print(f"Incompleto     : {incompleto/iterations*100:.2f}%")
    print(f"Auto-loss      : {auto_loss/iterations*100:.2f}%")

    print("\n--- CONSISTÊNCIA ---")
    print(f"Jogos jogáveis (completo + parcial): {jogos_ok/iterations*100:.2f}%")
    print(f"Brick + auto-loss                  : {bricks/iterations*100:.2f}%")

    print("="*50)

def classify(table):
    sn = table["bench"].count("Snorunt")
    bu = table["bench"].count("Budew") + (1 if table["active"] == "Budew" else 0)
    if sn >= 2 and bu >= 1:
        return "completo"
    if sn >= 1 or bu >= 1:
        return "parcial"
    return "incompleto"

# ---------------- AÇÕES DE JOGO ----------------

def play_basics_from_hand(hand, table):
    for p in ["Snorunt", "Budew", "Munkidori", "Yveltal"]:
        while (
            p in hand and
            table["bench"].count(p) < SETUP_LIMITS[p] and
            len(table["bench"]) < 5
        ):
            hand.remove(p)
            table["bench"].append(p)

def use_poffin(hand, deck, table):
    if "Poffin" not in hand:
        return
    hand.remove("Poffin")

    for target in ["Snorunt", "Budew"]:
        while (
            table["bench"].count(target) < SETUP_LIMITS[target] and
            target in deck and
            len(table["bench"]) < 5
        ):
            deck.remove(target)
            table["bench"].append(target)
            break  # Poffin busca só 2 no total

def use_nest_or_ultra(hand, deck, table):
    for ball in ["NestBall", "UltraBall"]:
        if ball in hand:
            hand.remove(ball)
            for target in ["Munkidori", "Snorunt", "Budew", "Yveltal"]:
                if (
                    target in deck and
                    table["bench"].count(target) < SETUP_LIMITS.get(target, 1) and
                    len(table["bench"]) < 5
                ):
                    deck.remove(target)
                    table["bench"].append(target)
                    return

def use_artazon(deck, table):
    for target in ["Snorunt", "Budew", "Munkidori", "Yveltal"]:
        if (
            target in deck and
            table["bench"].count(target) < SETUP_LIMITS.get(target, 1) and
            len(table["bench"]) < 5
        ):
            deck.remove(target)
            table["bench"].append(target)
            return
    
def use_pokegear(hand, deck, table):
    if "Pokégear" not in hand:
        return False

    priority = pokegear_priority(table)
    top = deck[:7]

    for sup in priority:
        if sup in top:
            hand.append(sup)
            deck.remove(sup)
            return True

    return False

def attach_energy(hand, table):
    if "Energy" in hand and "Munkidori" in table["bench"]:
        hand.remove("Energy")
        table["energy_on_munkidori"] = True

# ---------------- CICLO DO TURNO 1 ----------------

def turn_cycle(hand, deck, table, supporter_used=False):
    play_basics_from_hand(hand, table)

    while "Poffin" in hand:
        use_poffin(hand, deck, table)
        random.shuffle(deck)

    while "NestBall" in hand or "UltraBall" in hand:
        use_nest_or_ultra(hand, deck, table)
        random.shuffle(deck)

    if "Artazon" in hand:
        hand.remove("Artazon")
        use_artazon(deck, table)
        random.shuffle(deck)

    if "Pokégear" in hand:
        hand.remove("Pokégear")
        use_pokegear(hand, deck, table)
        random.shuffle(deck)

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
        random.shuffle(deck)
        turn_cycle(hand, deck, table, supporter_used=True)

    elif "Lillie" in hand:
        hand.remove("Lillie")
        random.shuffle(deck)
        hand.clear()
        hand.extend(deck[:8])
        del deck[:8]
        random.shuffle(deck)
        turn_cycle(hand, deck, table, supporter_used=True)

    elif "Kissera" in hand:
        hand.remove("Kissera")
        hand.clear()
        hand.extend(deck[:6])
        del deck[:6]
        turn_cycle(hand, deck, table, supporter_used=True)

# ---------------- SIMULAÇÃO ----------------

def simulate_turn1( iterations):
    results = {"completo":0, "parcial":0, "incompleto":0, "auto_loss":0}

    for _ in range(iterations):
        deck = build_deck()

        # Mulligan
        while True:
            hand = deck[:7]
            if any(c in BASICS for c in hand):
                break
            random.shuffle(deck)

        del deck[:7]

        table = {"active": None, "bench": [], "energy_on_munkidori": False}
        table["active"] = choose_active(hand)

        prizes = deck[:6]
        del deck[:6]

        if auto_loss(prizes):
            results["auto_loss"] += 1
            continue

        hand.append(deck.pop(0))  # draw T1
        turn_cycle(hand, deck, table)

        results[classify(table)] += 1

    return results

# ---------------- EXECUÇÃO ----------------
ITERATIONS = 150_000

results = simulate_turn1(ITERATIONS)
print_report(results, ITERATIONS, "2 Pokégear 3 Snorunt")
