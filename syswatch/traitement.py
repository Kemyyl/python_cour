import platform
import psutil
from datetime import datetime


def recuperer_info_systeme():
    """Retourne les infos système sans les afficher."""
    return {
        "os": platform.system(),
        "version": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node()
    }


def recuperer_cpu():
    """Retourne les infos sur le CPU."""
    return {
        "coeurs_physiques": psutil.cpu_count(logical=False),
        "coeurs_logiques": psutil.cpu_count(logical=True),
        "utilisation": psutil.cpu_percent(interval=1)
    }


def recuperer_memoire():
    """Retourne les infos mémoire."""
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "disponible": mem.available,
        "pourcentage": mem.percent
    }


def recuperer_disques():
    """Retourne les infos disques sous forme d'une liste."""
    partitions = psutil.disk_partitions()
    resultat = []

    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            resultat.append({
                "point_montage": p.mountpoint,
                "total": usage.total,
                "utilise": usage.used,
                "pourcentage": usage.percent
            })
        except PermissionError:
            continue

    return resultat


def recuperer_tout():
    """Collecte toutes les informations et les regroupe dans un dictionnaire."""
    return {
        "timestamp": datetime.now().isoformat(),
        "systeme": recuperer_info_systeme(),
        "cpu": recuperer_cpu(),
        "memoire": recuperer_memoire(),
        "disques": recuperer_disques()
    }
