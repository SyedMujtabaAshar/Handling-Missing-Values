import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variable to store the data
data = None

def handle_missing_values():
    global data
    # Open file dialog to select CSV file
    file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if not file_path:
        return

    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {e}")
        return
    
    # Show missing values summary
    missing_values = data.isnull().sum()
    missing_values_str = missing_values.to_string()

    # Display the missing values in the text box
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, f"Missing Values Summary:\n{missing_values_str}\n\n")

    # Ask user for method to handle missing values (via buttons)
    def handle_fillna():
        global data
        fill_value = entry_fill_value.get().strip()
        try:
            if fill_value.isdigit():
                fill_value = int(fill_value)
            elif fill_value.replace('.', '', 1).isdigit():
                fill_value = float(fill_value)
            data = data.fillna(fill_value)
            messagebox.showinfo("Success", "Missing values filled successfully!")
            show_updated_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"Error filling missing values: {e}")

    def handle_interpolate():
        global data
        # Ask user whether to use mean or median for interpolation
        interpolate_method = interpolate_method_var.get()
        
        if interpolate_method == "Mean":
            data = data.fillna(data.mean())
            messagebox.showinfo("Success", "Missing values interpolated with mean.")
        elif interpolate_method == "Median":
            data = data.fillna(data.median())
            messagebox.showinfo("Success", "Missing values interpolated with median.")
        else:
            messagebox.showerror("Error", "Invalid interpolation method selected.")
            return
        
        show_updated_data(data)
    
    def show_updated_data(data):
        # Display updated data in the text box
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Updated Data (with missing values handled):\n")
        text_box.insert(tk.END, data.head())

        # Save updated data to a new CSV file
        def save_file():
            output_path = filedialog.asksaveasfilename(title="Save CSV file", defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            if output_path:
                try:
                    data.to_csv(output_path, index=False)
                    messagebox.showinfo("Success", f"Updated CSV file saved to: {output_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving updated file: {e}")

        # Add a button to save the file
        save_button = tk.Button(root, text="Save Updated CSV", command=save_file)
        save_button.pack(pady=10)

    # Create UI for user to choose method to handle missing values
    method_frame = tk.Frame(root)
    method_frame.pack(pady=10)

    # Fill with a specific value option
    fillna_button = tk.Button(method_frame, text="Fill with Specific Value", command=lambda: handle_fillna())
    fillna_button.pack(side=tk.LEFT, padx=10)

    # Interpolate missing values option
    interpolate_button = tk.Button(method_frame, text="Interpolate", command=lambda: handle_interpolate())
    interpolate_button.pack(side=tk.LEFT, padx=10)

    # Entry field for fill value (for the 'Fill with Specific Value' option)
    entry_fill_value_label = tk.Label(root, text="Enter the value to fill missing values with:")
    entry_fill_value_label.pack(pady=5)
    entry_fill_value = tk.Entry(root)
    entry_fill_value.pack(pady=5)

    # Radio buttons for interpolation method (Mean or Median)
    interpolate_method_var.set("Mean")  # Default to "Mean"
    mean_radio = tk.Radiobutton(root, text="Mean", variable=interpolate_method_var, value="Mean")
    mean_radio.pack(pady=5)
    median_radio = tk.Radiobutton(root, text="Median", variable=interpolate_method_var, value="Median")
    median_radio.pack(pady=5)


# Set up the main window
root = tk.Tk()
root.title("Missing Values Handler")
root.geometry("600x500")

# Global variable for interpolation method
interpolate_method_var = tk.StringVar()

# Add a text box to display information and results
text_box = tk.Text(root, height=15, width=70)
text_box.pack(pady=10)

# Add a button to load the CSV file
load_button = tk.Button(root, text="Load CSV File", command=handle_missing_values)
load_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
