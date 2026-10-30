#!/usr/bin/env python3
"""Met chaque <lastmod> du sitemap à la date de la dernière modification réelle de la page (historique git de main).

Sans cela, les changements du site ne sont pas signalés aux moteurs : l'envoi IndexNow quotidien
ne retient que les pages dont le lastmod a changé. Lancé par .github/workflows/sitemap-lastmod.yml.
"""
import re
import subprocess
import sys
from pathlib import Path

SITEMAP = Path("sitemap.xml")


def fichier_de(loc):
    chemin = re.sub(r"^https?://[^/]+/?", "", loc)
    return Path(chemin + "index.html" if chemin == "" or chemin.endswith("/") else chemin)


def derniere_modif(fichier):
    # Article : la date déclarée (dateModified) prime, pour qu'un changement de bouton ou de pied de page
    # ne fasse pas passer la page pour mise à jour.
    m = re.search(r'"dateModified":\s*"([^"]+)"', fichier.read_text(encoding="utf-8"))
    if m:
        return m.group(1)
    # --first-parent : date et heure (ISO 8601) de l'arrivée de la modification sur main (fusion de la PR) ;
    # l'heure permet de signaler deux modifications de la même page faites le même jour.
    sortie = subprocess.run(["git", "log", "-1", "--first-parent", "--format=%cI", "--", str(fichier)],
                            capture_output=True, text=True, check=True).stdout.strip()
    return sortie or None


def maj_bloc(m):
    bloc = m.group(0)
    loc = re.search(r"<loc>\s*([^<\s]+)\s*</loc>", bloc)
    if not loc:
        return bloc
    fichier = fichier_de(loc.group(1))
    date = derniere_modif(fichier) if fichier.exists() else None
    if not date:
        print(f"ignoré (fichier introuvable) : {loc.group(1)}", file=sys.stderr)
        return bloc
    if "<lastmod>" in bloc:
        return re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{date}</lastmod>", bloc)
    return re.sub(r"(</loc>)", rf"\1\n    <lastmod>{date}</lastmod>", bloc, count=1)


avant = SITEMAP.read_text(encoding="utf-8")
apres = re.sub(r"<url>.*?</url>", maj_bloc, avant, flags=re.S)
if apres != avant:
    SITEMAP.write_text(apres, encoding="utf-8")
    print("sitemap.xml mis à jour")
else:
    print("sitemap.xml déjà à jour")
