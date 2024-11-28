import pandas as pd

# Define the labeling rules
def label_entry(row):
    """
    Assign a label based on predefined rules.
    - Typing Speed: Low, Medium, High
    - Behavior: Distracted, Focused
    """
    # Example rules
    if row['event_type'] == 'keystroke':
        # Typing speed based on interval (arbitrary thresholds for example)
        if row['interval'] < 0.1:
            typing_label = 'High Speed'
        elif row['interval'] < 0.5:
            typing_label = 'Medium Speed'
        else:
            typing_label = 'Low Speed'
    else:
        typing_label = None  # Not applicable for non-keystrokes
    
    if row['event_type'] == 'mouse_move':
        # Mouse behavior based on movement speed (x, y coordinates and interval)
        if row['interval'] < 0.1:  # Frequent movements
            behavior_label = 'Active'
        elif row['interval'] < 1.0:
            behavior_label = 'Moderately Active'
        else:
            behavior_label = 'Inactive'
    elif row['event_type'] == 'mouse_click':
        behavior_label = 'Clicked'
    else:
        behavior_label = None  # Not applicable for other events
    
    # Return combined labels
    return typing_label, behavior_label

# Load the raw data
file_path = "raw_data.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Apply labeling rules
data[['Typing_Label', 'Behavior_Label']] = data.apply(label_entry, axis=1, result_type='expand')

# Save the labeled data
output_file = "labeled_data.csv"
data.to_csv(output_file, index=False)

print(f"Labeled data saved to {output_file}")