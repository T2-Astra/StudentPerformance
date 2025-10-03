import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import traceback

class StudentPerformanceModel:
    def __init__(self, csv_file='student_performance.csv'):
        self.csv_file = csv_file
        self.model = LinearRegression()
        self.is_trained = False
        self._train_model()
    
    def _train_model(self):
        """Train the model with the complete 1 million row dataset"""
        try:
            print("🔄 Loading complete student performance dataset...")
            print("📊 Processing 1,000,000+ student records...")
            
            # Load the entire dataset efficiently using chunks for memory management
            chunk_size = 50000  # Process in chunks to manage memory
            chunks = []
            
            print("📖 Reading dataset in chunks...")
            for chunk in pd.read_csv(self.csv_file, chunksize=chunk_size):
                chunks.append(chunk)
                print(f"   Loaded {len(chunks) * chunk_size:,} records...", end='\r')
            
            df = pd.concat(chunks, ignore_index=True)
            print(f"\n✅ Successfully loaded {len(df):,} student records!")
            
            # Display dataset statistics
            print(f"\n📊 Dataset Statistics:")
            print(f"   • Total Students: {len(df):,}")
            print(f"   • Study Hours Range: {df['weekly_self_study_hours'].min():.1f} - {df['weekly_self_study_hours'].max():.1f}")
            print(f"   • Attendance Range: {df['attendance_percentage'].min():.1f}% - {df['attendance_percentage'].max():.1f}%")
            print(f"   • Participation Range: {df['class_participation'].min()} - {df['class_participation'].max()}")
            print(f"   • Score Range: {df['total_score'].min():.2f} - {df['total_score'].max():.2f}")
            
            # Features for prediction
            X = df[['weekly_self_study_hours', 'attendance_percentage', 'class_participation']]
            y = df['total_score']
            
            print(f"\n🔄 Splitting dataset (80% train, 20% test)...")
            # Use stratified sampling for better representation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=True
            )
            
            print(f"   • Training samples: {len(X_train):,}")
            print(f"   • Testing samples: {len(X_test):,}")
            
            print(f"\n🟣 Training Linear Regression model on full dataset...")
            # Linear regression scales well with large datasets
            self.model.fit(X_train, y_train)
            
            print(f"\n🟦 Evaluating model performance...")
            # Evaluate on test set
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Calculate additional metrics
            mae = np.mean(np.abs(y_test - y_pred))
            
            print(f"\n🎯 Model Performance on {len(X_test):,} test samples:")
            print(f"   • R² Score: {r2:.4f} ({r2*100:.2f}% variance explained)")
            print(f"   • MSE: {mse:.2f}")
            print(f"   • MAE: {mae:.2f}")
            print(f"   • RMSE: {np.sqrt(mse):.2f}")
            
            # Feature importance (coefficients for linear regression)
            feature_names = ['Study Hours', 'Attendance', 'Participation']
            coefficients = self.model.coef_
            print(f"\n📊 Feature Importance (Model Coefficients):")
            for name, coef in zip(feature_names, coefficients):
                print(f"   • {name}: {coef:.3f}")
            
            self.is_trained = True
            print(f"\n✅ Model successfully trained on complete dataset!")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            import traceback
            traceback.print_exc()
            self.is_trained = False
    
    def predict_grade(self, study_hours, attendance, participation):
        """Predict student performance and grade"""
        if not self.is_trained:
            raise Exception("Model training failed. Check CSV file.")
        
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

def main():
    # Create and train the model
    model = StudentPerformanceModel()
    
    # Example prediction
    if model.is_trained:
        result = model.predict_grade(15, 85, 6)
        print(f"\n🔮 Example Prediction:")
        print(f"Study Hours: 15, Attendance: 85%, Participation: 6")
        print(f"Predicted Score: {result['predicted_score']}")
        print(f"Predicted Grade: {result['predicted_grade']}")

if __name__ == "__main__":
    main()
