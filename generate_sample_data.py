import pandas as pd
import numpy as np

# Generate smaller sample dataset for Vercel deployment
np.random.seed(42)

# Create 10,000 sample records instead of 1M
n_samples = 10000

data = {
    'weekly_self_study_hours': np.random.uniform(0, 40, n_samples),
    'attendance_percentage': np.random.uniform(50, 100, n_samples),
    'class_participation': np.random.randint(0, 11, n_samples),
    'total_score': np.random.uniform(30, 100, n_samples)
}

df = pd.DataFrame(data)
df.to_csv('student_performance_small.csv', index=False)
print(f"Generated {len(df)} sample records for deployment")