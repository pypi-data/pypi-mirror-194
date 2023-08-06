import click
import pyautogui
import time
import math
import random

pyautogui.FAILSAFE = False

@click.command()
@click.option("--distance", default=10, help="Distance of mouse movement (in pixels)")
@click.option("--interval", default=0.5, help="Interval between mouse movements (in seconds)")
@click.option("--threshold", default=5, help="Threshold for mouse movement detection (in pixels)")
@click.option("--speedup-prob", default=0.1, help="Probability of increasing mouse movement speed")
def jiggle(distance, interval, threshold, speedup_prob):
    """
    Move the mouse cursor in a random pattern with the specified distance and interval indefinitely,
    but break the loop if the mouse cursor position changes by more than the threshold.
    """
    current_position = pyautogui.position()
    prev_pos = current_position
    speedup_factor = 1.0

    while True:
        x_offset = random.randint(-distance, distance)
        y_offset = random.randint(-distance, distance)
        if random.random() < speedup_prob:
            speedup_factor = random.uniform(1.0, 3.0)
        else:
            speedup_factor = 1.0
        pyautogui.moveRel(x_offset, y_offset, duration=0.25/speedup_factor)
        time.sleep(interval)
        
        # Check for mouse movement and exit the loop if the mouse has been moved by more than the threshold
        new_position = pyautogui.position()
        distance_moved = math.sqrt((new_position[0] - current_position[0])**2 + (new_position[1] - current_position[1])**2)
        print(f"Distance moved: {distance_moved:.2f} pixels")
        if distance_moved > threshold:
            print(f"Mouse cursor moved by {distance_moved:.2f} pixels. Exiting loop.")
            break
        current_position = new_position

if __name__ == "__main__":
    jiggle()