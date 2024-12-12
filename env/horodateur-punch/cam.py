import cv2
from quickHand import HandDetector
import subprocess
import numpy as np
import os

SAVE_PATH = "mediapipe"

os.makedirs(SAVE_PATH, exist_ok=True)

def capture_image_and_save():
    # Essayer d'ouvrir la caméra
    cap = cv2.VideoCapture(-1, cv2.CAP_V4L)

    # Vérifier si la caméra est ouverte
    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return None

    # Capture une seule image
    
    success, image = cap.read()

    print(success, image)
    # Vérification si l'image a bien été capturée
    if not success or image is None:
        print("Erreur : Impossible de capturer une image.")
        print(f"success: {success}, image: {image}")
        cap.release()
        return None

    # Sauvegarder l'image capturée dans un fichier
    filename = "captured_image.jpg"
    cv2.imwrite(filename, image)
    print(f"Image capturée et sauvegardée dans : {filename}")

    cap.release()  # Libérer la caméra

    return image
    
def capture_frame():
    try:
        # Run libcamera-jpeg and capture a single frame as JPEG output
        cmd = ["libcamera-jpeg", "-o", "-", "--width", "640", "--height", "480", "--nopreview"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode != 0:
            print(f"Error capturing frame: {error.decode('utf-8')}")
            return None

        # Decode JPEG output to OpenCV image
        img_array = np.frombuffer(output, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Exception while capturing frame: {e}")
        return None
        
def mediapipe_image(frame, data):
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data}_{timestamp}.jpg"
        filepath = os.path.join(SAVE_PATH, filename)
        cv2.imwrite(filepath, frame)
        print(f"QR code image saved: {filepath}")
    except Exception as e:
        print(f"Failed to save image: {e}")
        
        
def main():
    image = capture_frame()

    # Si une image a été capturée, détecter les mains
    if image is not None:
        detector = HandDetector(detectionCon=0.8, maxHands=2)

        hands = detector.findHands(image, draw=False)

        if len(hands) == 1:
            hand = hands[0]
            detector.infoOnHand(image, hand, [detector.fingersUp(hand)])
        elif len(hands) == 2:
            print("mettez une main seulement")
        
        # Afficher l'image capturée
        cv2.imshow("Captured Image", image)
        cv2.waitKey(0) & 0xFF == ord('q')
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
