# imports
from kandinsky import *
from ion import *
from random import *
from math import *
from time import sleep

# constante(s)
liste_couleurs = [(255, 0, 0), (248, 4, 0), (248, 12, 0), (248, 16, 0), (248, 24, 0), (248, 28, 0), 
   (248, 36, 0), (248, 44, 0), (248, 48, 0), (248, 56, 0), (248, 60, 0), (248, 68, 0), 
   (248, 76, 0), (248, 80, 0), (248, 88, 0), (248, 92, 0), (248, 100, 0), (248, 104, 0), 
   (248, 112, 0), (248, 120, 0), (248, 124, 0), (248, 132, 0), (248, 136, 0), (248, 144, 0), 
   (248, 152, 0), (248, 156, 0), (248, 164, 0), (248, 168, 0), (248, 176, 0), (248, 180, 0), 
   (248, 188, 0), (248, 196, 0), (248, 200, 0), (248, 208, 0), (248, 216, 0), (248, 220, 0), 
   (248, 228, 0), (248, 232, 0), (248, 240, 0), (248, 248, 0), (248, 252, 0), (248, 252, 0), 
   (240, 252, 0), (232, 252, 0), (224, 252, 0), (216, 252, 0), (216, 252, 0), (208, 252, 0), 
   (200, 252, 0), (192, 252, 0), (184, 252, 0), (184, 252, 0), (176, 252, 0), (168, 252, 0), 
   (160, 252, 0), (160, 252, 0), (152, 252, 0), (144, 252, 0), (136, 252, 0), (128, 252, 0), 
   (128, 252, 0), (120, 252, 0), (112, 252, 0), (104, 252, 0), (96, 252, 0), (96, 252, 0), 
   (88, 252, 0), (80, 252, 0), (72, 252, 0), (64, 252, 0), (64, 252, 0), (56, 252, 0), 
   (48, 252, 0), (40, 252, 0), (32, 252, 0), (32, 252, 0), (24, 252, 0), (16, 252, 0), 
   (8, 252, 0), (0, 252, 0)]

liste_niveaux = ('execrable', 'nul', 'mauvais', 'risible', 'correct', 
      'convenable', 'satisfaisant', 'bon', 'excellent', 'légendaire', 'irreel')

# fonctions
def dessiner_panier(xg, yg): # dessine le panier de coordonnees du coin haut gauche (xg, yg) 
    fill_rect(xg, yg, 30, 5, 'orange')
    p1 = 1.5*xg-(yg+35)
    for i in range(10):
        p = i*7.5+p1
        for x in range(xg, xg+30):
            y = round(1.5*x-p)
            if yg+4 < y <yg+35:
                set_pixel(x, y, 'black')

def cercle(x0,y0,r,c,e=1): # dessine un cercle de centre (x0, y0), de rayon r, de couleur c, d'epaisseur e
  for i in range(2*e):
    xd=x0-round((r-i*0.5)/sqrt(2))
    xf=x0+round((r-i*0.5)/sqrt(2))
    for x in range(xd,xf+1):
      x1=x
      y1=y0+int(sqrt((r-i*0.5)**2-(x-x0)**2))
      set_pixel(x,y1,c)
      for _ in range(3):
        x2=x0+y1-y0
        y2=y0+x0-x1
        set_pixel(x2,y2,c)
        x1,y1=x2,y2

def cercle_plein(x0,y0,r,c1,c2,e=1): # dessine un cercle rempli de couleur exterieure c1, et interieure c2
  cercle(x0,y0,r,c1,e)
  cercle(x0,y0,r-e,c2,r-e)

def roots(a,b,c): # retourne les racines du polynome passe en argument
  delta = b*b-4*a*c
  x_1 = (-b-sqrt(delta))/(2*a)
  x_2 = (-b+sqrt(delta))/(2*a)
  return (x_1, x_2)

def parab(a,b,c): # dessine la balle, dans sa trajectoire
    y = 175 
    for x in range(0, 320, 2):
        if x==140:
          draw_string('<'+' '+str(valeur_actuelle+1)+'%', 37, ancienne_valeur, liste_couleurs[valeur_actuelle])
        effacer_balle(x-2, y)
        if not 290<x<320 or not 95<y<130:
          y = round((a*(x**2))+(b*x)+c)
          dessiner_balle(x, y)
          sleep(0.02)
    if not 95<y<130:
      effacer_balle(318,y)

def dessiner_balle(xc, yc): # dessine la balle
  cercle_plein(xc, yc, 4, 'black', 'orange')

def effacer_balle(xc, yc): # efface la balle
  fill_rect(xc-4, yc-4, 9, 9, 'white')

def get_rand(n, percent): 
    np = n*((400/percent)/100)
    return round(random()*np*2 + (n-np))      

def is_in(a,b,c): # gere le tir (dessins, texte), renvoie True si le ballon 'rentre' dans le panier
    draw_string('       ',125, 170)
    parab(a,b,c)
    reponses = roots(a,b,c-95)
    dessiner_panier(290, 95)
    for i in reponses:
        if 290<=i<=320:
          draw_string('Bravo !', 125, 170, 'black', (15,240,30))
          return True
    draw_string('Nul !', 135, 170, 'white', (255,0,0))
    return False
    
def tir(sc, d, at): # gere le tir (score, calculs)
    global l
    l.append(round(d, 2))
    draw_string(str(at), 300, 10)
    if is_in(1/get_rand(200, d), -1.8, 175):
      sc+=1
    return sc

def curseur_bis(phase): # affiche le curseur (phase : 1 ou -1)
  global valeur_actuelle, ancienne_valeur
  couleur, limite = (248, 255, 248), 0
  if phase > 0:
    couleur, limite = liste_couleurs[valeur_actuelle], 79
  while not keydown(KEY_TWO):
    if valeur_actuelle == limite:
      curseur_bis(-phase)
    if couleur != (248, 255, 248):
      couleur = liste_couleurs[valeur_actuelle]
    fill_rect(10, 89-valeur_actuelle, 25, 1, couleur)
    valeur_actuelle += phase
    sleep(0.00125)
  draw_string('      ', 37, ancienne_valeur, (248, 255, 248))
  ancienne_valeur = 82-valeur_actuelle
  draw_string('<'+' '+str(valeur_actuelle+1)+'%', 37, ancienne_valeur, liste_couleurs[valeur_actuelle])
  return valeur_actuelle
    
# variables de départ
score, attempts, valeur_actuelle, ancienne_valeur, l = 0, 0, 0, 0, []

def start():
  global score, attempts, valeur_actuelle, ancienne_valeur, l
  # ecran de depart
  fill_rect(0, 0, 320, 222, 'black')
  fill_rect(10, 10, 300, 202, 'orange')
  cercle(160, 50, 20, 'black')
  draw_string('Appuyez sur la touche <OK>', 30, 91, 'black', 'orange')
  draw_string('pour tenter votre chance.', 35, 111, 'black', 'orange')
  fill_rect(140, 145, 40, 45, 'white')
  dessiner_panier(145, 150)
  for s in range(3):
    draw_string(str(-s+3), 155, 41, 'black', 'orange')
    sleep(1)

  # jeu
  fill_rect(0, 0, 320, 222, 'white')
  fill_rect(9, 9, 27, 82, color(0, 0, 0))
  fill_rect(10, 10, 25, 80, color(255, 255, 255))
  dessiner_panier(290, 95)
  # game loop
  while attempts!=10 and not keydown(KEY_ONE):
    attempts += 1
    score = tir(score, curseur_bis(1)+1, attempts)
    sleep(3)

  # écran final
  couleur = liste_couleurs[round(score*7.9)]
  fill_rect(0, 0, 320, 222, couleur)
  texte_score = 'Votre score : '+str(score)+'/'+str(attempts)+" ("+str(round(score/attempts*100))+"%)"
  draw_string(texte_score, int((320-(len(texte_score)*10))/2), 50, 'black', couleur)
  texte_sc_theorique = 'Score theorique : ' + str(round(sum(l)/len(l))) + '%'
  draw_string(texte_sc_theorique, int((320-(len(texte_sc_theorique)*10))/2), 70, 'black', couleur)
  texte_niveau = 'Votre niveau est ' + liste_niveaux[score] + '.'
  draw_string(texte_niveau, int((320-(len(texte_niveau)*10))/2), 160)
  cercle_plein(160, 120, 17, 'black', 'orange')