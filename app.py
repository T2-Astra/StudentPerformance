from flask import Flask, request, jsonify, render_template
from model_lightweight import StudentPerformanceModel

app = Flask(__name__)

# Initialize and train model on startup
print("Initializing Student Performance Model...")
model = StudentPerformanceModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        study_hours = float(data['study_hours'])
        attendance = float(data['attendance'])
        participation = int(data['participation'])
        
        # Validate inputs
        if not (0 <= study_hours <= 168):
            return jsonify({'error': 'Study hours must be between 0 and 168'}), 400
        if not (50 <= attendance <= 100):
            return jsonify({'error': 'Attendance must be between 50 and 100'}), 400
        if not (0 <= participation <= 10):
            return jsonify({'error': 'Participation must be between 0 and 10'}), 400
        
        result = model.predict_grade(study_hours, attendance, participation)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
