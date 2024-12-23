import serial
import time
import sys

# Initialize the serial connection (make sure the device is connected to the correct port)
ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1) # Replace with COM1-10 for windows and /dev/ttyUSB1,2,3,4,5 whatever serial port the camera is connected to

# Initialize sleep time variable (starting at 0.3 seconds)
sleep_time = 0.3

# Function to send VISCA command to move the camera up
def move_camera_up():
    command = b'\x88\x01\x06\x01\x01\x14\x03\x01\xFF'  # Command for "UP" change x14 value down to 1 or up to 14 to change speed
    ser.write(command)
    time.sleep(sleep_time)  # Sleep for the current sleep_time
    stop_camera()  # Stop the camera after moving
    print("Camera moved up.")

# Function to send VISCA command to move the camera down
def move_camera_down():
    command = b'\x88\x01\x06\x01\x01\x14\x03\x02\xFF'  # Command for "DOWN" change x14 value down to 1 or up to 14 to change speed
    ser.write(command)
    print("Camera moved down.")
    time.sleep(sleep_time)
    stop_camera()
# Function to send VISCA command to move the camera left
def move_camera_left():
    command = b'\x88\x01\x06\x01\x18\x14\x01\x03\xFF'  # Command for "LEFT" change x18 value down to 1 or up to 18 to change speed
    ser.write(command)
    time.sleep(sleep_time)
    stop_camera()
    print("Camera moved left.")

# Function to send VISCA command to move the camera right
def move_camera_right():
    command = b'\x88\x01\x06\x01\x18\x14\x02\x03\xFF'  # Command for "RIGHT" change x18 value down to 1 or up to 18 to change speed
    ser.write(command)
    time.sleep(sleep_time)
    stop_camera()
    print("Camera moved right.")

# Function to send VISCA command to stop the camera movement
def stop_camera():
    command = b'\x88\x01\x06\x01\x01\x14\x03\x03\xFF'  # Command for "STOP"
    ser.write(command)
    print("Camera stopped.")

# Function to send VISCA command to home the camera
def home_camera():
    command = b'\x88\x01\x06\x04\xFF\x14\x03\x01\xFF'  # Command for "HOME"
    ser.write(command)
    print("Camera is homing.")

# Function to zoom in
def zoom_in():
    zoom_in_command = b'\x88\x01\x04\x07\x27\xFF\x90\x41\xFF\x90\x51\xFF'
    ser.write(zoom_in_command)
    time.sleep(sleep_time)
    stop_camera()
    print("Zooming in.")

# Function to zoom out
def zoom_out():
    zoom_out_command = b'\x88\x01\x04\x07\x37\xFF\x90\x41\xFF\x90\x51\xFF'
    ser.write(zoom_out_command)
    time.sleep(sleep_time)
    stop_camera()
    print("Zooming out.")

# Function to adjust the sleep time
def adjust_sleep_time(increase, step):
    global sleep_time
    if increase:
        sleep_time += step
    else:
        if sleep_time > step:
            sleep_time -= step
        else:
            sleep_time = step
    print(f"Sleep time adjusted to {sleep_time} seconds.")

# Main control based on the command line argument
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Please provide a command.")
            sys.exit(1)

        command = sys.argv[1]

        if command == "move_camera_up":
            move_camera_up()
        elif command == "move_camera_down":
            move_camera_down()
        elif command == "move_camera_left":
            move_camera_left()
        elif command == "move_camera_right":
            move_camera_right()
        elif command == "home_camera":
            home_camera()
        elif command == "zoom_in":
            zoom_in()
        elif command == "zoom_out":
            zoom_out()
        elif command == "sbcp":
            adjust_sleep_time(True, 0.1)  # Increase by 0.1
        elif command == "sbcn":
            adjust_sleep_time(False, 0.1)  # Decrease by 0.1
        elif command == "sscp":                                            # sleep time changes does not work, check if chat gpt can fix it, im too lazy :)
            adjust_sleep_time(True, 0.05)  # Increase by 0.05
        elif command == "sscn":
            adjust_sleep_time(False, 0.05)  # Decrease by 0.05
        else:
            print("Invalid command. Available commands are:")
            print("move_camera_up, move_camera_down, move_camera_left, move_camera_right, home_camera, zoom_in, zoom_out, sbcp, sbcn, sscp, sscn")

    except KeyboardInterrupt:
        print("Control interrupted.")
    finally:
        ser.close()  # Close the serial connection