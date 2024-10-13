import picar_4wd as fc
import json
import time

class Picar_Tracker:

    def __init__(self):
        self.speed_val = 0
        self.current_direction = "North"
        self.battery_life = self._get_battery_life()
        self.temperature = self._get_cpu_temperature()
        self.distance = 0.0

    def _update_state(self):
        self.battery_life = self._get_battery_life()
        self.speed_val = self._get_speed_val()

    def _parse_byte_message(message: bytes):
        """
        Helper function to process incoming byte messages
        received by the server

        Parameters
        ==========
            message: bytes
            Incoming message to the server, in bytes
        """
        return (message.decode("utf-8").strip())

    def _get_battery_life(self):
        """
        Wrapper function to retrieve and parse the power-read
        from the PiCar-4WD
        """
        return f"{float(fc.power_read())}V"
    
    def _get_speed_val(self):
        """
        Wrapper function to retrieve and parse the speed-val
        from the PiCar-4WD
        """
        return f"{float(fc.speed_val())} units"

    def _get_cpu_temperature(self):
        """
        Wrapper function to retrieve and parse the CPU temperature
        from the PiCar-4WD
        """
        return f"{float(fc.cpu_temperature())} degrees"
    
    def generate_payload(self):
        """
        Generates a Byte payload of dictionary attributes to update
        the HTML page.
        """
        self._update_state()
        payload = {
            "distance": self.distance,
            "battery": self.battery_life,
            "temperature": self.temperature
        }
        return (json.dumps(payload).encode("utf-8"))

    def parse_movement(self, command: str):
        """
        Helper function to process movement messages

        Parameters
        ==========
        command : str
            String command representing the movement command
        """

        if command == "forward":
            fc.forward(10)
            self.distance += 1.0
        elif command == "left":
            fc.turn_left(45)
            self.distance += 0.25
            self.current_direction = "west"
        elif command == "right":
            fc.turn_right(45)
            self.distance += 0.25
            self.current_direction = "east"
        elif command == "backward":
            fc.backward(10)
            self.distance += 1.0
        elif command == "stop":
            fc.stop()
    