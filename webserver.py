from flask import Flask, send_file
import cv2

app = Flask(__name__)

def capture_image():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open camera.")
        return None

    ret, frame = camera.read()
    if not ret:
        print("Error: Could not read frame.")
        return None

    # Save the captured image to a file
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)
    camera.release()
    return image_path

@app.route('/capture')
def capture():
    image_path = capture_image()
    if image_path:
        return send_file(image_path, mimetype='image/jpeg')
    else:
        return "Failed to capture image", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
