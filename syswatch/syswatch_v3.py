import csv
import json
import time
import sys
import traitement


def octets_vers_go(octets):
    """Convertit un nombre d'octets en Go avec 2 décimales."""
    return f"{octets / (1024 ** 3):.2f} GB"


def afficher_systeme(data):
    print("=== Système ===")
    print("OS :", data["os"])
    print("Version :", data["version"])
    print("Architecture :", data["architecture"])
    print("Hostname :", data["hostname"])
    print()


def afficher_cpu(data):
    print("=== CPU ===")
    print("Cœurs physiques :", data["coeurs_physiques"])
    print("Cœurs logiques :", data["coeurs_logiques"])
    print("Utilisation :", f"{data['utilisation']:.2f}%")
    print()


def afficher_memoire(data):
    print("=== Mémoire ===")
    print("Total :", octets_vers_go(data["total"]))
    print("Disponible :", octets_vers_go(data["disponible"]))
    print("Utilisation :", f"{data['pourcentage']:.2f}%")
    print()


def afficher_disques(data):
    print("=== Disques ===")
    for d in data:
        print(f"{d['point_montage']} : {d['pourcentage']:.2f}% utilisé")
    print()


def exporter_csv(metriques, fichier):
    """Exporte les données essentielles dans un CSV."""
    ligne = {
        "timestamp": metriques["timestamp"],
        "hostname": metriques["systeme"]["hostname"],
        "cpu_percent": metriques["cpu"]["utilisation"],
        "mem_total_gb": metriques["memoire"]["total"] / (1024 ** 3),
        "mem_dispo_gb": metriques["memoire"]["disponible"] / (1024 ** 3),
        "mem_percent": metriques["memoire"]["pourcentage"],
        "disk_root_percent": metriques["disques"][0]["pourcentage"]
    }

    # On vérifie si le fichier existe
    fichier_existe = False
    try:
        with open(fichier, "r"):
            fichier_existe = True
    except FileNotFoundError:
        pass

    # On écrit la ligne CSV
    with open(fichier, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ligne.keys())

        if not fichier_existe:
            writer.writeheader()

        writer.writerow(ligne)


def exporter_json(metriques, fichier):
    """Sauvegarde les métriques complètes dans un fichier JSON."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(metriques, f, indent=2)


def collecter_en_continu(intervalle, nombre):
    """Collecte les métriques en boucle (continuellement)."""
    compteur = 0
    try:
        while nombre == 0 or compteur < nombre:
            metriques = traitement.recuperer_tout()
            print(f"[Collecte] {metriques['timestamp']}")

            exporter_csv(metriques, "historique.csv")

            compteur += 1
            time.sleep(intervalle)

    except KeyboardInterrupt:
        print("\nArrêt manuel.")


def calculer_moyennes(fichier_csv):
    """Affiche les statistiques CPU et RAM à partir du CSV."""
    cpu = []
    mem = []

    try:
        with open(fichier_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for ligne in reader:
                cpu.append(float(ligne["cpu_percent"]))
                mem.append(float(ligne["mem_percent"]))

    except FileNotFoundError:
        print("Aucun fichier historique.csv trouvé.")
        return

    if not cpu:
        print("Aucune donnée dans le CSV.")
        return

    print("=== STATISTIQUES ===")
    print(f"CPU → Moyenne: {sum(cpu)/len(cpu):.2f}% | Min: {min(cpu):.2f}% | Max: {max(cpu):.2f}%")
    print(f"RAM → Moyenne: {sum(mem)/len(mem):.2f}% | Min: {min(mem):.2f}% | Max: {max(mem):.2f}%")


if __name__ == "__main__":

    args = sys.argv

    # COLLECTE CONTINUE
    if "--continu" in args:
        intervalle = 5
        nombre = 0

        if "--intervalle" in args:
            intervalle = int(args[args.index("--intervalle") + 1])

        if "--nombre" in args:
            nombre = int(args[args.index("--nombre") + 1])

        collecter_en_continu(intervalle, nombre)
        sys.exit()

    # MODE STATISTIQUES
    if "--stats" in args:
        calculer_moyennes("historique.csv")
        sys.exit()

    # COLLECTE SIMPLE
    metriques = traitement.recuperer_tout()

    afficher_systeme(metriques["systeme"])
    afficher_cpu(metriques["cpu"])
    afficher_memoire(metriques["memoire"])
    afficher_disques(metriques["disques"])

    exporter_csv(metriques, "historique.csv")
    exporter_json(metriques, "derniere_collecte.json")
