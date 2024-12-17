from flask import Flask, render_template, Response, jsonify, request
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO models
models = {
    "YOLO8n": "models/yolo8n.pt",
    "YOLO11s": "models/yolo11s.pt"
}
current_model_name = "YOLO8n"
model = YOLO(models[current_model_name])

# Initialize camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame)  # Без предсказаний, чистое изображение
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_prediction')
def video_prediction():
    def generate_prediction_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            # Run prediction
            results = model(frame)
            annotated_frame = results[0].plot()
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate_prediction_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/switch_model', methods=['POST'])
def switch_model():
    global model, current_model_name
    new_model_name = request.json.get('model')
    if new_model_name in models:
        current_model_name = new_model_name
        model = YOLO(models[new_model_name])
        return jsonify({"message": f"Switched to {new_model_name}"})
    return jsonify({"error": "Model not found"}), 400

if __name__ == '__main__':
    app.run(debug=True)