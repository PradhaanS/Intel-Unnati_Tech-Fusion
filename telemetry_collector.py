import psutil
import time
import tkinter as tk
from tkinter import ttk

# Function to collect system metrics
def collect_metrics(duration, update_label):
    start_time = time.time()
    end_time = start_time + duration
    metrics = {
        'cpu_percent': [],
        'disk_io': [],
        'memory_percent': []
    }

    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        update_label(f"Collecting telemetry... {remaining_time} seconds remaining")

        cpu_percent = psutil.cpu_percent(interval=1)
        disk_io = psutil.disk_io_counters().write_bytes
        memory_percent = psutil.virtual_memory().percent

        metrics['cpu_percent'].append(cpu_percent)
        metrics['disk_io'].append(disk_io)
        metrics['memory_percent'].append(memory_percent)

    return metrics

# Function to compute averages
def compute_averages(metrics):
    avg_cpu = sum(metrics['cpu_percent']) / len(metrics['cpu_percent'])
    avg_disk_io = sum(metrics['disk_io']) / len(metrics['disk_io'])
    avg_memory = sum(metrics['memory_percent']) / len(metrics['memory_percent'])
    return avg_cpu, avg_disk_io, avg_memory

# Function to estimate power based on averages
def estimate_power(avg_cpu, avg_disk_io, avg_memory):
    # Assuming average CPU power consumption per 1% usage (0.3 watts per %)
    avg_power_cpu = avg_cpu * 0.3
    
    # Assuming average disk power consumption (2 watts for SSD)
    avg_power_disk = avg_disk_io * 2e-12  # (Converting bytes to appropriate scale)
    
    # Assuming average memory power consumption (3 watts per 8GB module)
    avg_power_memory = avg_memory * 3 / 8

    avg_power = avg_power_cpu + avg_power_disk + avg_power_memory

    return avg_power, avg_power_cpu, avg_power_disk, avg_power_memory

# Function to suggest optimizations based on component metrics
def suggest_optimizations(avg_power_cpu, avg_power_disk, avg_power_memory):
    suggestions = []

    # CPU Optimization
    if avg_power_cpu > 45:
        suggestions.append("\nOptimization Suggestion (High CPU Power): Reduce CPU Frequency")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Determine the Current CPU Governor Setting:")
        suggestions.append("   - Check the current CPU governor setting using the following command:")
        suggestions.append("     $ cpupower frequency-info --policy")
        suggestions.append("2. Set CPU Governor to 'powersave' Mode:")
        suggestions.append("   - Open a terminal and run the following command with sudo privileges:")
        suggestions.append("     $ sudo cpupower frequency-set -g powersave")
        suggestions.append("3. Verify the CPU Governor Setting:")
        suggestions.append("   - Confirm that the CPU governor is set to 'powersave' mode by executing:")
        suggestions.append("     $ cpupower frequency-info --policy")
        suggestions.append("4. Monitor Power Consumption:")
        suggestions.append("   - Monitor the power consumption to observe the impact of the frequency reduction.")
    elif avg_power_cpu < 15:
        suggestions.append("\nOptimization Suggestion (Low CPU Power): Increase CPU Frequency")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Determine the Current CPU Governor Setting:")
        suggestions.append("   - Check the current CPU governor setting using the following command:")
        suggestions.append("     $ cpupower frequency-info --policy")
        suggestions.append("2. Set CPU Governor to 'performance' Mode:")
        suggestions.append("   - Open a terminal and run the following command with sudo privileges:")
        suggestions.append("     $ sudo cpupower frequency-set -g performance")
        suggestions.append("3. Verify the CPU Governor Setting:")
        suggestions.append("   - Confirm that the CPU governor is set to 'performance' mode by executing:")
        suggestions.append("     $ cpupower frequency-info --policy")
        suggestions.append("4. Monitor Power Consumption:")
        suggestions.append("   - Monitor the power consumption to observe the impact of the frequency increase.")
    
    # Memory Optimization
    if avg_power_memory > 4:
        suggestions.append("\nOptimization Suggestion (High Memory Power): Reduce Memory Usage")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Identify Memory-Intensive Applications:")
        suggestions.append("   - Use task manager or system monitor to identify memory-intensive applications.")
        suggestions.append("2. Close Unnecessary Applications:")
        suggestions.append("   - Close applications that are not in use to free up memory.")
        suggestions.append("3. Optimize Running Applications:")
        suggestions.append("   - Optimize applications to use less memory where possible.")
        suggestions.append("4. Upgrade Hardware:")
        suggestions.append("   - Consider upgrading to more efficient memory modules if the hardware is outdated.")
    elif avg_power_memory < 2:
        suggestions.append("\nOptimization Suggestion (Low Memory Power): Increase Memory Efficiency")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Upgrade to Faster Memory Modules:")
        suggestions.append("   - Upgrade to memory modules with higher speed and lower power consumption.")
        suggestions.append("2. Enable Memory Compression:")
        suggestions.append("   - Enable memory compression in the operating system to make more efficient use of available memory.")
        suggestions.append("3. Monitor Memory Usage:")
        suggestions.append("   - Regularly monitor memory usage to ensure efficient utilization.")

    # Disk Optimization
    if avg_power_disk > 55:
        suggestions.append("\nOptimization Suggestion (High Disk Power): Reduce Disk Usage")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Identify Disk-Intensive Processes:")
        suggestions.append("   - Use disk usage tools to identify processes that are heavily using the disk.")
        suggestions.append("2. Optimize Disk Usage:")
        suggestions.append("   - Optimize applications and processes to reduce disk usage.")
        suggestions.append("3. Upgrade to SSD:")
        suggestions.append("   - Consider upgrading from HDD to SSD for lower power consumption and better performance.")
    elif avg_power_disk < 20:
        suggestions.append("\nOptimization Suggestion (Low Disk Power): Increase Disk Efficiency")
        suggestions.append("\nExplanation:")
        suggestions.append("1. Defragment Disk (HDD only):")
        suggestions.append("   - Regularly defragment the disk to improve efficiency.")
        suggestions.append("2. Enable TRIM (SSD only):")
        suggestions.append("   - Ensure TRIM is enabled on SSDs for better performance and longevity.")
        suggestions.append("3. Monitor Disk Usage:")
        suggestions.append("   - Regularly monitor disk usage to ensure efficient utilization.")

    return suggestions

# Function to display the results in a GUI
def display_results(metrics, avg_cpu, avg_disk_io, avg_memory, avg_power, optimizations):
    result_window = tk.Toplevel()
    result_window.title("Telemetry Results")
    result_window.geometry("600x400")

    canvas = tk.Canvas(result_window)
    scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Display the results with grid layout
    row = 0
    ttk.Label(scrollable_frame, text=f"Average CPU Percent:").grid(row=row, column=0, sticky='w', padx=10, pady=2)
    ttk.Label(scrollable_frame, text=f"{avg_cpu:.2f}").grid(row=row, column=1, sticky='w', padx=10, pady=2)
    row += 1

    ttk.Label(scrollable_frame, text=f"Average Disk IO (GB):").grid(row=row, column=0, sticky='w', padx=10, pady=2)
    ttk.Label(scrollable_frame, text=f"{avg_disk_io / 1e9:.2f}").grid(row=row, column=1, sticky='w', padx=10, pady=2)
    row += 1

    ttk.Label(scrollable_frame, text=f"Average Memory Percent:").grid(row=row, column=0, sticky='w', padx=10, pady=2)
    ttk.Label(scrollable_frame, text=f"{avg_memory:.2f}").grid(row=row, column=1, sticky='w', padx=10, pady=2)
    row += 1

    ttk.Label(scrollable_frame, text=f"Average Power Consumption Estimate:").grid(row=row, column=0, sticky='w', padx=10, pady=2)
    ttk.Label(scrollable_frame, text=f"{avg_power:.2f} Watts").grid(row=row, column=1, sticky='w', padx=10, pady=2)
    row += 1

    ttk.Label(scrollable_frame, text="Optimization Suggestions:").grid(row=row, column=0, sticky='w', padx=10, pady=2, columnspan=2)
    row += 1
    for opt in optimizations:
        ttk.Label(scrollable_frame, text=f"- {opt}").grid(row=row, column=0, sticky='w', padx=10, pady=2, columnspan=2)
        row += 1

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Function to run the telemetry collection and display results in GUI
def run_telemetry():
    duration = 60
    wait_label.pack(pady=20)
    
    def update_label(text):
        wait_label.config(text=text)
        root.update_idletasks()

    metrics = collect_metrics(duration, update_label)
    avg_cpu, avg_disk_io, avg_memory = compute_averages(metrics)
    avg_power, avg_power_cpu, avg_power_disk, avg_power_memory = estimate_power(avg_cpu, avg_disk_io, avg_memory)
    optimizations = suggest_optimizations(avg_power_cpu, avg_power_disk, avg_power_memory)

    wait_label.pack_forget()
    display_results(metrics, avg_cpu, avg_disk_io, avg_memory, avg_power, optimizations)

# Setting up the main GUI
root = tk.Tk()
root.title("Telemetry Collector")
root.geometry("300x200")

ttk.Label(root, text="Telemetry Collector", font=("Helvetica", 16)).pack(pady=10)

wait_label = ttk.Label(root, text="")

ttk.Button(root, text="Run Telemetry", command=run_telemetry).pack(pady=20)

root.mainloop()
