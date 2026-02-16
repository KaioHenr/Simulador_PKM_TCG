def classify(table):
    sn = table["bench"].count("Snorunt")
    bu = table["bench"].count("Budew") + (1 if table["active"] == "Budew" else 0)

    if sn >= 2 and bu >= 1:
        return "completo"
    if sn >= 1 or bu >= 1:
        return "parcial"
    return "incompleto"


def auto_loss(prizes):
    return (
        prizes.count("Snorunt") >= 4 or
        prizes.count("Budew") >= 3 or
        prizes.count("Munkidori") >= 4 or
        prizes.count("Froslass") >= 3
    )
