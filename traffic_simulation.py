import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

def simulate_advanced_traffic_data(num_intersections, time_steps, mean_flow=400, std_dev=100, min_flow=50, max_flow=1000, rush_hours=((7, 9), (17, 19))):
    """
    Simulates traffic data for a given number of intersections over specified time steps.
    
    Parameters:
    - num_intersections: Number of intersections to simulate.
    - time_steps: Total time steps for simulation (e.g., 1440 for 24 hours).
    - mean_flow: Mean traffic flow for Gaussian distribution.
    - std_dev: Standard deviation for Gaussian distribution.
    - min_flow: Minimum traffic flow cap.
    - max_flow: Maximum traffic flow cap.
    - rush_hours: Tuple of tuples defining rush hour ranges.
    
    Returns:
    - A pandas DataFrame containing the simulated traffic data.
    """
    data = []
    for t in range(time_steps):
        for i in range(num_intersections):
            weather_factor = random.uniform(0.8, 1.2)  # Impact of weather
            time_of_day = 1 if any(start <= t % 24 <= end for start, end in rush_hours) else 0.5  # Rush hours
            
            # Introduce random incidents
            if random.random() < 0.05:  # 5% chance of an incident
                incident_factor = 0.7  # Reduce traffic flow by 30%
            else:
                incident_factor = 1
            
            traffic_flow = int(random.gauss(mean_flow, std_dev) * weather_factor * time_of_day * incident_factor)
            traffic_flow = max(min_flow, min(traffic_flow, max_flow))  # Cap at reasonable values
            data.append([t, i, traffic_flow])
    
    df = pd.DataFrame(data, columns=['Time', 'Intersection', 'TrafficFlow'])
    return df

def plot_traffic_data(df):
    """
    Plots the traffic flow over time for each intersection.
    
    Parameters:
    - df: DataFrame containing traffic data.
    """
    plt.figure(figsize=(15, 8))
    for i in df['Intersection'].unique():
        intersection_data = df[df['Intersection'] == i]
        plt.plot(intersection_data['Time'], intersection_data['TrafficFlow'], label=f'Intersection {i}')
    
    plt.title('Traffic Flow Over Time')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Traffic Flow')
    plt.legend()
    plt.grid()
    plt.show()

def export_to_csv(df, filename='traffic_data.csv'):
    """
    Exports the traffic data to a CSV file.
    
    Parameters:
    - df: DataFrame containing traffic data.
    - filename: Name of the file to save the data.
    """
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

def compute_statistics(df):
    """
    Computes and prints basic statistics of the traffic data.
    
    Parameters:
    - df: DataFrame containing traffic data.
    """
    stats = df.groupby('Intersection')['TrafficFlow'].agg(['mean', 'median', 'max', 'min'])
    print("Traffic Flow Statistics by Intersection:")
    print(stats)

# Simulate for 10 intersections over 24 hours
traffic_data = simulate_advanced_traffic_data(10, 1440)

# Display the first few rows
print(traffic_data.head())

# Plot the traffic data
plot_traffic_data(traffic_data)

# Export the traffic data to a CSV file
export_to_csv(traffic_data)

# Compute and display statistics
compute_statistics(traffic_data)