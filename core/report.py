def print_report(results, iterations, label):
    c = results["completo"]
    p = results["parcial"]
    i = results["incompleto"]
    a = results["auto_loss"]

    print("\n" + "="*50)
    print(f"BUILD: {label}")
    print("="*50)
    print(f"Total de partidas: {iterations:,}")

    print("\n--- RESULTADOS ---")
    for k, v in results.items():
        print(f"{k:12}: {v/iterations*100:.2f}%")

    print("\n--- CONSISTÊNCIA ---")
    print(f"Jogáveis : {(c+p)/iterations*100:.2f}%")
    print(f"Brick    : {(i+a)/iterations*100:.2f}%")
    print("="*50)
