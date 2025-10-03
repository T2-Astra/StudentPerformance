import csv
import numpy as np

# Generate smaller sample dataset for deployment
np.random.seed(42)
n_samples = 5000  # Smaller dataset for faster deployment

print("Generating sample data for deployment...")

# Generate realistic data
study_hours = np.random.uniform(0, 40, n_samples)
attendance = np.random.uniform(50, 100, n_samples)
participation = np.random.randint(0, 11, n_samples)

# Create realistic scores based on features
scores = (
    study_hours * 1.2 + 
    attendance * 0.8 + 
    participation * 3 + 
    np.random.normal(0, 5, n_samples)
)
scores = np.clip(scores, 30, 100)

# Write to CSV
with open('student_performance_deploy.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['weekly_self_study_hours', 'attendance_percentage', 'class_participation', 'total_score'])
    
    for i in range(n_samples):
        writer.writerow([
            round(study_hours[i], 2),
            round(attendance[i], 2),
            int(participation[i]),
            round(scores[i], 2)
        ])

print(f"Generated {n_samples} sample records for deployment")
print("File saved as: student_performance_deploy.csv")