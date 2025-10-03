import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class StudentPerformanceModel:
    def __init__(self, csv_file='student_performance_deploy.csv'):
        self.csv_file = csv_file
        self.model = LinearRegression()
        self.is_trained = False
        self._train_model()
    
    def _load_csv_data(self):
        """Load CSV data using built-in csv module instead of pandas"""
        data = []
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append([
                        float(row['weekly_self_study_hours']),
                        float(row['attendance_percentage']),
                        int(row['class_participation']),
                        float(row['total_score'])
                    ])
            return np.array(data)
        except FileNotFoundError:
            # Generate sample data if CSV not found
            print("CSV file not found, generating sample data...")
            return self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample data for deployment"""
        np.random.seed(42)
        n_samples = 10000
        
        study_hours = np.random.uniform(0, 40, n_samples)
        attendance = np.random.uniform(50, 100, n_samples)
        participation = np.random.randint(0, 11, n_samples)
        
        # Create realistic score based on features
        scores = (
            study_hours * 1.2 + 
            attendance * 0.8 + 
            participation * 3 + 
            np.random.normal(0, 5, n_samples)
        )
        scores = np.clip(scores, 30, 100)  # Keep scores realistic
        
        return np.column_stack([study_hours, attendance, participation, scores])
    
    def _train_model(self):
        """Train the model with available data"""
        try:
            print("🔄 Loading student performance data...")
            data = self._load_csv_data()
            
            print(f"✅ Successfully loaded {len(data):,} student records!")
            
            # Features and target
            X = data[:, :3]  # study_hours, attendance, participation
            y = data[:, 3]   # total_score
            
            print(f"🔄 Splitting dataset (80% train, 20% test)...")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            print(f"🟣 Training Linear Regression model...")
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            mae = np.mean(np.abs(y_test - y_pred))
            
            print(f"🎯 Model Performance:")
            print(f"   • R² Score: {r2:.4f}")
            print(f"   • MAE: {mae:.2f}")
            print(f"   • RMSE: {np.sqrt(mse):.2f}")
            
            self.is_trained = True
            print(f"✅ Model successfully trained!")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            self.is_trained = False
    
    def predict_grade(self, study_hours, attendance, participation):
        """Predict student performance and grade"""
        if not self.is_trained:
            raise Exception("Model training failed.")
        
        # Make prediction
        features = np.array([[study_hours, attendance, participation]])
        score = self.model.predict(features)[0]
        
        # Ensure score is within valid range
        score = max(0, min(100, score))
        
        # Convert score to grade
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'predicted_score': round(score, 2),
            'predicted_grade': grade
        }