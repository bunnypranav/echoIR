import board
import digitalio
import pwmio
import time
import json
import microcontroller
import wifi
import socketpool
import adafruit_httpserver
from adafruit_httpserver import Server, Request, Response
from adafruit_httpserver.mime_type import MIMEType
from secrets import secrets

# Pins
IRTXPIN = board.GP5
IRRXPIN = board.GP18
BUTTONPIN = board.GP4

# IR transmitter
ir_pwm = pwmio.PWMOut(IRTXPIN, frequency=38000, duty_cycle=0)


def carrier_on():
    ir_pwm.duty_cycle = 32768


def carrier_off():
    ir_pwm.duty_cycle = 0


# IR receiver
ir_rx = digitalio.DigitalInOut(IRRXPIN)
ir_rx.direction = digitalio.Direction.INPUT

# Button
button = digitalio.DigitalInOut(BUTTONPIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Signal Storage
ir_signals = {}
next_signal_id = 1


def sleep_us_precise(duration_us):
    if duration_us <= 0:
        return

    if duration_us > 2500:
        time.sleep((duration_us - 500) / 1_000_000)

    target = time.monotonic_ns() + (duration_us * 1000)
    while time.monotonic_ns() < target:
        pass


# Recording
def record_ir(duration=3):
    global next_signal_id

    print("Recording IR")
    start_time = time.monotonic()
    last_state = ir_rx.value
    segments = []
    last_change = time.monotonic_ns()

    while time.monotonic() - start_time < duration:
        current_state = ir_rx.value
        if current_state != last_state:
            now = time.monotonic_ns()
            delta = (now - last_change) // 1000
            segments.append((last_state, delta))
            last_change = now
            last_state = current_state

    now = time.monotonic_ns()
    delta = (now - last_change) // 1000
    if delta > 0:
        segments.append((last_state, delta))

    signal_id = next_signal_id
    ir_signals[signal_id] = segments
    next_signal_id += 1

    print("Saved as ID:", signal_id)
    return signal_id


# Replay
def replay_ir(signal_id):
    if signal_id not in ir_signals:
        print("Invalid ID")
        return

    print("Replaying ID:", signal_id)
    segments = ir_signals[signal_id]

    for level, duration_us in segments:
        if not level:
            carrier_on()
        else:
            carrier_off()
        sleep_us_precise(duration_us)

    carrier_off()
    print("Done")


# WiFi setup
print("Connecting to WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static")


# Webhook Endpoint
@server.route("/play", methods=["POST"])
def play_handler(request: Request):
    try:
        data = request.json()
        signal_id = int(data["id"])
        replay_ir(signal_id)
        return Response(request, "Played", MIMEType.TEXT)
    except Exception as e:
        return Response(request, "Error: " + str(e), MIMEType.TEXT)


server.start(str(wifi.radio.ipv4_address))

print("Webhook ready at:")
print("http://" + str(wifi.radio.ipv4_address) + "/play")

# Main Loop
last_button_state = True

while True:
    server.poll()

    current_button_state = button.value

    if not current_button_state and last_button_state:
        time.sleep(0.2)
        if not button.value:
            record_ir()

    last_button_state = current_button_state
