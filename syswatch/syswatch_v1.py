import platform
import psutil

# System general #
def afficher_systeme():
    print("=== Système ===")
    print("OS :", platform.system())
    print("Version :", platform.release())
    print("Architecture :", platform.machine())
    print("Nom d'ordinateur :", platform.node())
    print("Python version :", platform.python_version())
    print()

# CPU  #
def afficher_cpu():
    print("=== CPU ===")
    coeurs_physiques = psutil.cpu_count(logical=False)
    coeurs_logiques = psutil.cpu_count(logical=True)
    utilisation = psutil.cpu_percent(interval=1)

    print("Cœurs physiques :", coeurs_physiques)
    print("Cœurs logiques :", coeurs_logiques)
    print("Utilisation :", f"{utilisation:.2f}%")
    print()

# RAM  #
def afficher_memoire():
    print("=== Mémoire ===")
    mem = psutil.virtual_memory()

    total_go = mem.total / (1024 ** 3)
    disponible_go = mem.available / (1024 ** 3)

    print("Total :", f"{total_go:.2f} GB")
    print("Disponible :", f"{disponible_go:.2f} GB")
    print("Utilisation :", f"{mem.percent:.2f}%")
    print()

# Disque #
def afficher_disques():
    print("=== Disques ===")
    partitions = psutil.disk_partitions()

    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            print(f"{p.mountpoint} : {usage.percent:.2f}% utilisé")
        except PermissionError:
            continue

    print()

# lancer le script #
if __name__ == "__main__":
    print("=== SysWatch v1 ===\n")

    afficher_systeme()
    afficher_cpu()
    afficher_memoire()
    afficher_disques()
print("=== Fin du rapport ===")