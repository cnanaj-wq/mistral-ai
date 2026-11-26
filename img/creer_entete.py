"""Compose le visuel d'en-tête du README. Sortie : img/entete.png (1280 x 640).

Usage : python img/creer_entete.py (demande Pillow et les polices Segoe UI de Windows)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).parent
L, H = 1280, 640
NUIT, AMBRE, BLANC, GRIS, ENCRE = "#1F3A5F", "#E0A458", "#FFFFFF", "#A7B1BD", "#16263D"
POLICES = Path("C:/Windows/Fonts")


def police(nom, taille):
    return ImageFont.truetype(str(POLICES / nom), taille)


def bloc(d, x, y, largeur, titre, code, couleur):
    """Une carte sombre : un titre court et une expression en police à chasse fixe."""
    d.rounded_rectangle((x, y, x + largeur, y + 150), 18, fill=ENCRE, outline=couleur, width=3)
    d.text((x + 28, y + 24), titre, font=police("seguisb.ttf", 24), fill=couleur)
    d.text((x + 28, y + 78), code, font=police("consola.ttf", 25), fill=BLANC)


fond = Image.new("RGB", (L, H), NUIT)
d = ImageDraw.Draw(fond)
d.text((70, 62), "Mistral AI", font=police("seguisb.ttf", 72), fill=AMBRE)
d.text(
    (70, 160),
    "Convertir des expressions Spotfire en Qlik Sense",
    font=police("seguisb.ttf", 44),
    fill=BLANC,
)
bloc(d, 70, 270, 500, "Spotfire", "Sum([Réel])  where [Ordre] <= 7", GRIS)
d.text((606, 322), ">>", font=police("seguisb.ttf", 54), fill=AMBRE)
bloc(d, 700, 270, 510, "Qlik Sense", "Sum({<...>} [CR Réel])", AMBRE)
d.text(
    (70, 480),
    "5 expressions converties par l'API, puis exécutées et contrôlées dans Qlik Sense",
    font=police("segoeui.ttf", 28),
    fill=BLANC,
)
d.text(
    (70, 550),
    "Cédric NANA — Expert BI & Data | Analytics & AI Automation",
    font=police("segoeui.ttf", 26),
    fill=GRIS,
)
fond.save(ICI / "entete.png", optimize=True)
print("En-tête écrit :", ICI / "entete.png")
