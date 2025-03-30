import cv2
import numpy as np

# Initialiser la caméra
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

# Vérification si la caméra est ouverte
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir камеру.")
    exit()

# Variables pour compter les passages
left_hits = 0
right_hits = 0
last_position = None

while True:
    # Capturer une image de la caméra
    ret, frame = cap.read()
    
    if not ret:
        print("Erreur lors de la capture de l'image.")
        break

    # Obtenir les dimensions du cadre
    height, width, _ = frame.shape
    
    # Division de l'image en 2 parties
    middle_x = width // 2  # Ligne médiane

    # Conversion en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Appliquer un flou pour mieux détecter les contours
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Détecter les contours
    edges = cv2.Canny(blurred, 50, 150)

    # Trouver les contours dans l'image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dessiner les contours détectés
    for contour in contours:
        # Si l'aire du contour est suffisante, on considère que c'est l'étiquette
        if cv2.contourArea(contour) > 1000:  # Ajuster cette valeur selon la taille du marqueur
            # Dessiner un rectangle autour du contour détecté
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculer la position horizontale du centre du rectangle
            center_x = x + w // 2

            # Vérifier si l'étiquette traverse la ligne médiane
            if last_position is None:
                last_position = center_x  # Initialiser la position

            # Si le marqueur a traversé la ligne médiane, augmenter le compteur
            if last_position < middle_x and center_x >= middle_x:
                right_hits += 1  # Le marqueur est passé dans la partie droite
            elif last_position >= middle_x and center_x < middle_x:
                left_hits += 1  # Le marqueur est passé dans la partie gauche

            # Mettre à jour la position
            last_position = center_x

    # Afficher les résultats
    cv2.putText(frame, f"Left Hits: {left_hits}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Right Hits: {right_hits}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Dessiner une ligne médiane pour séparer les zones gauche et droite
    cv2.line(frame, (middle_x, 0), (middle_x, height), (255, 0, 0), 2)

    # Afficher l'image avec les contours et les compteurs
    cv2.imshow('Tracking with Hits', frame)

    # Quitter la boucle en appuyant sur la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la caméra et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
