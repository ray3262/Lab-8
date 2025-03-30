import cv2
import numpy as np


cap = cv2.VideoCapture(0)  


if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la caméra.")
    exit()

while True:
    
    ret, frame = cap.read()
    
    if not ret:
        print("Erreur lors de la capture de l'image.")
        break

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    
    edges = cv2.Canny(blurred, 50, 150)

    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    for contour in contours:
        
        if cv2.contourArea(contour) > 1000:  
            
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Marqueur detecte", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    
    cv2.imshow('Tracking', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
