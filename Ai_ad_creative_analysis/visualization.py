import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from database import SessionLocal, PerformanceData

def generate_visualization():
    db = SessionLocal()
    data_entries = db.query(PerformanceData).all()
    db.close()

    data = []
    for entry in data_entries:
        data.append([entry.ctr, entry.conversion_rate])
    
    df = pd.DataFrame(data, columns=["CTR", "Conversion Rate"])
    correlation_matrix = df.corr()

    # Generate heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("CTR vs Conversion Rate Correlation")
    plt.savefig("uploads/correlation.png")

    return {"message": "Visualization generated", "image": "uploads/correlation.png"}
