import serial


BAUD_RATE = 115200
PORT = "COM8"

device = None

def connect():
    global device
    device = serial.Serial(PORT, BAUD_RATE, timeout=5)

def read_data():
    global device
    if device == None:
        return None
    
    if device.in_waiting > 0:
        raw_data = device.readline()
        clean_data = raw_data.decode('utf-8').strip()

        return clean_data
    else:
        return None

def close_port():
    global device
    device.close()
