from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
import time
import pandas as pd
import csv
from collections import defaultdict

# Local variables
duration_in_seconds = 3

# Data storage lists
keystrokes = []
mouse_moves = []
mouse_clicks = []
key_press_times = []  # To track time between consecutive key presses
key_count = defaultdict(int)  # To count key presses
last_keypress_time = time.time()

# Mouse metrics
mouse_click_times = []  # To track time between clicks
last_click_time = time.time()

# Special key mappings for control characters
special_key_map = {
    '\\x01': 'ctrl-A', '\\x02': 'ctrl-B', '\\x03': 'ctrl-C', '\\x04': 'ctrl-D',
    '\\x05': 'ctrl-E', '\\x06': 'ctrl-F', '\\x07': 'ctrl-G', '\\x08': 'ctrl-H',
    '\\x09': 'ctrl-I', '\\x0a': 'ctrl-J', '\\x0b': 'ctrl-K', '\\x0c': 'ctrl-L',
    '\\x0d': 'ctrl-M', '\\x0e': 'ctrl-N', '\\x0f': 'ctrl-O', '\\x10': 'ctrl-P',
    '\\x11': 'ctrl-Q', '\\x12': 'ctrl-R', '\\x13': 'ctrl-S', '\\x14': 'ctrl-T',
    '\\x15': 'ctrl-U', '\\x16': 'ctrl-V', '\\x17': 'ctrl-W', '\\x18': 'ctrl-X',
    '\\x19': 'ctrl-Y', '\\x1a': 'ctrl-Z', '\\x1b': 'ctrl-[', '\\x1c': 'ctrl-\\',
    '\\x1d': 'ctrl-]', '\\x1e': 'ctrl-^', '\\x1f': 'ctrl-_' ,

    'Key.space': 'SPACE',
    'Key.backspace': 'BACKSPACE',
    'Key.right': 'RIGHT_ARROW',
    'Key.left': 'LEFT_ARROW',
    'Key.up': 'UP_ARROW',
    'Key.down': 'DOWN_ARROW',
    'Key.esc': 'ESC',
    'Key.enter': 'ENTER'
}

# Helper function to map keys to human-readable format
def get_key_name(key):
    key = str(key)
    key = key.replace("'", '')
    if isinstance(key, Key):
        return special_key_map.get(str(key), str(key))  # Return mapped special key or its name
    else:
        return special_key_map.get(key, key)  # For regular keys like 'a', 'b', etc.

# Helper function to log events with timestamps
def log_event(event_type, data):
    timestamp = time.time()
    return {'timestamp': timestamp, 'event_type': event_type, **data}

# Keyboard event handlers
def on_press(key):
    global last_keypress_time
    try:
        # Get key name using the mapping function
        key_name = get_key_name(key)
        
        # Count the key press
        key_count[key_name] += 1
        
        # Track time between key presses
        current_time = time.time()
        inter_keystroke_interval = current_time - last_keypress_time
        keystrokes.append(log_event('keystroke', {'key': key_name, 'interval': inter_keystroke_interval}))
        key_press_times.append(current_time - last_keypress_time)  # Time between key presses
        last_keypress_time = current_time

    except Exception as e:
        print(f"Error in logging key press: {e}")

# Mouse event handlers
def on_move(x, y):
    mouse_moves.append(log_event('mouse_move', {'x': x, 'y': y}))

def on_click(x, y, button, pressed):
    global last_click_time
    if pressed:
        current_time = time.time()
        click_interval = current_time - last_click_time
        mouse_clicks.append(log_event('mouse_click', {'x': x, 'y': y, 'button': str(button), 'interval': click_interval}))
        mouse_click_times.append(click_interval)  # Time between clicks
        last_click_time = current_time

# Data storage function (save data to CSV with calculated metrics at the top)
def save_data_to_csv():
    # Calculate metrics
    total_keystrokes = len(keystrokes)
    typing_speed_kpm = (total_keystrokes / duration_in_seconds) * 60  # 20 seconds -> converted to KPM
    typing_speed_wpm = typing_speed_kpm / 5  # Assuming average word length is 5 characters
    avg_inter_key_interval = sum(key_press_times) / len(key_press_times) if key_press_times else 0
    avg_click_interval = sum(mouse_click_times) / len(mouse_click_times) if mouse_click_times else 0

    # Create a dictionary of metrics
    metrics = {
        'Total Keystrokes': total_keystrokes,
        'Typing Speed (KPM)': typing_speed_kpm,
        'Typing Speed (WPM)': typing_speed_wpm,
        'Avg. Keypress Interval': avg_inter_key_interval,
        'Avg. Mouse Click Interval': avg_click_interval,
        'Most Pressed Keys': dict(key_count)
    }

    # Create the CSV header with metrics
    header = ['Metric', 'Value']
    metric_rows = [[key, value] for key, value in metrics.items()]

    # All event data
    all_data = keystrokes + mouse_moves + mouse_clicks
    df_events = pd.DataFrame(all_data)

    # Save metrics and events to CSV
    with open('user_activity_log.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([header])  # Write header for metrics
        writer.writerows(metric_rows)  # Write metric values
        f.write('\n')  # Add a blank line between metrics and event data
        df_events.to_csv(f, index=False)  # Write event data

# Setup the listeners for mouse and keyboard
mouse_listener = MouseListener(on_move=on_move, on_click=on_click)
keyboard_listener = KeyboardListener(on_press=on_press)

# Start listening
mouse_listener.start()
keyboard_listener.start()

# Run for a set period of time (e.g., 20 seconds for testing purposes)
time.sleep(duration_in_seconds)  # 20 seconds for testing purposes

# Stop the listeners
mouse_listener.stop()
keyboard_listener.stop()

# Save collected data to CSV file with metrics at the top
save_data_to_csv()

print("Data collection completed and saved to 'user_activity_log.csv'")