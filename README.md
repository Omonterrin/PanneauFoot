# PanneauFoot
Panneau d'affichage du score 0 à 19 buts + chronomètre. Affichage via bandeaux LED WS2812B

Segments:
 -- A --
|       |
F       B
|       |
 -- G --
|       |
E       C
|       |
 -- D --


# Mapping des LEDs aux segments
segments = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6
}

# Segments allumés pour chaque chiffre
digit_segments = {
    0: ['A', 'B', 'C', 'D', 'E', 'F'],
    1: ['B', 'C'],
    2: ['A', 'B', 'G', 'E', 'D'],
    3: ['A', 'B', 'C', 'D', 'G'],
    4: ['F', 'G', 'B', 'C'],
    5: ['A', 'F', 'G', 'C', 'D'],
    6: ['A', 'F', 'E', 'D', 'C', 'G'],
    7: ['A', 'B', 'C'],
    8: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    9: ['A', 'B', 'C', 'D', 'F', 'G']
}
