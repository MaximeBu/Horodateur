import cv2
import subprocess
import numpy as np
import os
from datetime import datetime
from my_lcd import lcd, show_error, show_message
from user import validate_user, getNom, resetNom
from time import sleep

SAVE_PATH = "scanned_qrcodes"

os.makedirs(SAVE_PATH, exist_ok=True)

def capture_frame():
    """
    Capture une image unique depuis la caméra Raspberry Pi en utilisant libcamera-jpeg.
    Retourne l'image sous forme de tableau numpy pour un traitement avec OpenCV.
    """
    try:
        # Run libcamera-jpeg and capture a single frame as JPEG output
        cmd = ["libcamera-jpeg", "-o", "-", "--width", "640", "--height", "480", "--nopreview"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            print(f"Error capturing frame: {error.decode('utf-8')}")
            return None

        # Décode la sortie JPEG en image OpenCV
        img_array = np.frombuffer(output, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Exception while capturing frame: {e}")
        return None
        
def save_qr_code_image(frame, data):
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_PATH, filename)
        cv2.imwrite(filepath, frame)
        print(f"QR code image saved: {filepath}")
    except Exception as e:
        print(f"Failed to save QR code image: {e}")

def verify(data, frame, bbox):
    """
    Vérifie si les données du QR code scanné correspondent à un utilisateur du système.
    Affiche le nom de l'utilisateur s'il existe, ou un message d'erreur sinon.
    """
    resetNom()
    print(f"Scanning QR Code: {data}")
    validate_user(data)
    user_name = getNom()
    
    if user_name:
        print(f"User verified: {user_name}")
        drawBox(frame, bbox, data, True)
        
    else:
        print("User not recognized!")
        drawBox(frame, bbox, data, False)
    
    save_qr_code_image(frame,data)
    
    if user_name:
        print(f"User verified: {user_name}")
        lcd.clear()
        lcd.write_string(f"Bonjour, {user_name}!")
        openGate()
        sleep(5)
        closeGate()
    else:
        print("User not recognized!")
        lcd.clear()
        lcd.write_string("Utilisateur inconnu")
        show_error()
        sleep(3)
        
def drawBox(img, bbox, data, is_valid):
    
    color = (0, 255, 0) if is_valid else (0, 0, 255) # Definit la couleur en fonction de la validite
    
    points = [(int(bbox[0][i][0]), int(bbox[0][i][1])) for i in range(len(bbox[0]))]
    
    for i in range(len(points)):
        cv2.line(img, points[i - 1], points[i], color, 2)
    cv2.putText(img, data, (points[0][0], points[0][1] - 5),  cv2.FONT_HERSHEY_SIMPLEX, (points[1][0] - points [0][0]) * 0.004, (0,0, 255), 1, cv2.LINE_AA)
    

def openGate():
    """
    Opens the gate. Add GPIO or relay control logic here.
    """
    print("Gate Opened!")  # Placeholder for GPIO control

def closeGate():
    """
    Closes the gate. Add GPIO or relay control logic here.
    """
    print("Gate Closed!")  # Placeholder for GPIO control

def main():
    """
    Boucle principale pour capturer des images, détecter des QR codes et vérifier les utilisateurs.
    """
    detector = cv2.QRCodeDetector()

    try:
        closeGate()
        print("Starting QR code detection loop...")
        while True:
            frame = capture_frame()
            if frame is None:
                print("Failed to capture frame, retrying...")
                continue

            # Détecte et décode les QR codes dans l'image
            data, bbox, _ = detector.detectAndDecode(frame)
            if bbox is not None and data:
                print(f"QR code detected: {data}")
            
                
                verify(data, frame, bbox)
                

            # Affiche l'image capturée
            cv2.imshow("QR Code Scanner", frame)


            # Quitte la boucle si la touche 'q' est pressée
            if cv2.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:
        lcd.clear()
        print("Terminating...")
    finally:
        cv2.destroyAllWindows()
        lcd.clear()

if __name__ == "__main__":
    main()
