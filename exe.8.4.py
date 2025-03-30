import cv2
import numpy as np

cap = cv2.VideoCapture(0) 

if not cap.isOpened():
    print("Ошибка: Не удается открыть камеру.")
    exit()

fly_image = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)

left_hits = 0
right_hits = 0
last_position = None

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Ошибка при захвате изображения.")
        break

    height, width, _ = frame.shape
    middle_x = width // 2  

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:  
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            center_x = x + w // 2
            center_y = y + h // 2

            if last_position is None:
                last_position = center_x 

            
            if last_position < middle_x and center_x >= middle_x:
                right_hits += 1  
            elif last_position >= middle_x and center_x < middle_x:
                left_hits += 1  

            last_position = center_x

            
            fly_resized = cv2.resize(fly_image, (w, h))  
            for i in range(h):
                for j in range(w):
                    if fly_resized[i, j][3] != 0:  
                        frame[y + i, x + j] = fly_resized[i, j][:3]  

    
    cv2.putText(frame, f"Left Hits: {left_hits}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Right Hits: {right_hits}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    
    cv2.line(frame, (middle_x, 0), (middle_x, height), (255, 0, 0), 2)

    
    cv2.imshow('Tracking with Fly Overlay', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
