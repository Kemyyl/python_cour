import collector


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


if __name__ == "__main__":
    print("=== SysWatch v2.0 ===\n")

    metriques = collector.recuperer_tout()

    afficher_systeme(metriques["systeme"])
    afficher_cpu(metriques["cpu"])
    afficher_memoire(metriques["memoire"])
    afficher_disques(metriques["disques"])
print("=== Fin du rapport ===")
