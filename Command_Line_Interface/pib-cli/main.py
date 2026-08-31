import cmd 
import serial 
import argparse
import struct


''' INTERNAL COMMANDS '''
CMD_READ_PT1  =  1
CMD_READ_PT2    =  2
CMD_READ_PT3    =  3
CMD_READ_PT4    =  4
CMD_READ_PT5    =  5
CMD_READ_PT6    =  6
CMD_READ_PT7    =  7
CMD_READ_PT8    =  8


# UART Commands for MAX31856 TC Readings

CMD_READ_TC1    =  9
CMD_READ_TC2	= 10
CMD_READ_TC3	= 11
CMD_READ_TC4	= 12
CMD_READ_TC5	= 13

CMD_READ_TC1_CJ = 84
CMD_READ_TC2_CJ = 85
CMD_READ_TC3_CJ = 86
CMD_READ_TC4_CJ = 87
CMD_READ_TC5_CJ = 88


# UART Commands for Solenoid Valves

CMD_OPEN_SOL1  = 14
CMD_OPEN_SOL2  =  15
CMD_OPEN_SOL3  =  17
CMD_OPEN_SOL4  =  18
CMD_OPEN_SOL5  =  19
CMD_OPEN_SOL6  = 20
CMD_OPEN_SOL7  = 21
CMD_OPEN_SOL8  = 22
CMD_OPEN_SOL9  = 23
CMD_OPEN_SOL10  = 24
CMD_OPEN_SOL11  = 25
CMD_OPEN_SOL12  = 26
CMD_OPEN_SOL13  = 27
CMD_OPEN_SOL14  = 28
CMD_OPEN_SOL15  = 29
CMD_OPEN_SOL16  = 30
CMD_OPEN_SOL17  = 31
CMD_OPEN_SOL18  = 32

CMD_CLOSE_SOL1  = 33
CMD_CLOSE_SOL2  = 34
CMD_CLOSE_SOL3   = 35
CMD_CLOSE_SOL4  = 36
CMD_CLOSE_SOL5  = 37
CMD_CLOSE_SOL6  = 38
CMD_CLOSE_SOL7  = 39
CMD_CLOSE_SOL8  = 40
CMD_CLOSE_SOL9  = 41
CMD_CLOSE_SOL10  = 42
CMD_CLOSE_SOL11  = 43
CMD_CLOSE_SOL12  = 44
CMD_CLOSE_SOL13  = 45
CMD_CLOSE_SOL14  = 46
CMD_CLOSE_SOL15  = 47
CMD_CLOSE_SOL16  = 48
CMD_CLOSE_SOL17  = 49
CMD_CLOSE_SOL18  = 50

CMD_READ_VALVE_STATE_1 = 91
CMD_READ_VALVE_STATE_2 = 92
CMD_READ_VALVE_STATE_3 = 93
CMD_READ_VALVE_STATE_4 = 94
CMD_READ_VALVE_STATE_5 = 95
CMD_READ_VALVE_STATE_6 = 96
CMD_READ_VALVE_STATE_7 = 97
CMD_READ_VALVE_STATE_8 = 98
CMD_READ_VALVE_STATE_9 = 99
CMD_READ_VALVE_STATE_10 = 100
CMD_READ_VALVE_STATE_11 = 101
CMD_READ_VALVE_STATE_12 = 102
CMD_READ_VALVE_STATE_13 = 103
CMD_READ_VALVE_STATE_14 = 104
CMD_READ_VALVE_STATE_15 = 105
CMD_READ_VALVE_STATE_16 = 106
CMD_READ_VALVE_STATE_17 = 107 
CMD_READ_VALVE_STATE_18 = 108


# UART Commands for ADC7124 PC104 Stack Readings

CMD_READ_12VA_VB  = 51
CMD_READ_12VA_VA  = 52 # powers all Valves except for 4,6 (which are pwm)
CMD_READ_3V3_VB  = 53
CMD_READ_3V3_VA  = 54
CMD_READ_VBAT_VA  = 66
CMD_READ_VBAT_VB  = 67
CMD_READ_12VB_VA  = 68
CMD_READ_12VB_VB  = 69

CMD_READ_12VA_VB_CURRENT  = 70
CMD_READ_12VA_VA_CURRENT  = 71 
CMD_READ_3V3_VB_CURRENT  = 72
CMD_READ_3V3_VA_CURRENT  = 73
CMD_READ_VBAT_VA_CURRENT  = 74
CMD_READ_VBAT_VB_CURRENT  = 75
CMD_READ_12VB_VA_CURRENT  = 76
CMD_READ_12VB_VB_CURRENT  = 77

# UART Commands for FDC2214

CMD_READ_CAPACITANCE_A1  = 55
CMD_READ_CAPACITANCE_A2  = 56
CMD_READ_CATALYST_LEVEL_A1  = 57
CMD_READ_CATALYST_LEVEL_A2  = 58


# UART Command for heater

CMD_HEAT_CATALYST  = 59

CMD_MANUAL_HEATER_TURN_ON = 89
CMD_MANUAL_HEATER_TURN_OFF = 90


# UART Commands for Pressure Regulation (PWM / PID)

CMD_REGULATE_PRESSURE_INPUT_VALUE  = 60
CMD_REGULATE_PRESSURE_2_INPUT_VALUE  = 61


# UART Commands for PPU Control (OBC -> PIB)

CMD_PPU_CURRENT_READ_1  = 62
CMD_PPU_CURRENT_READ_2  = 63
CMD_PPU_ON  = 64
CMD_PPU_OFF  = 65

CMD_TOGGLE_RED_LED = 78
CMD_TOGGLE_GREEN_LED = 79
CMD_TOGGLE_AMBER_LED = 80


# Read Device IDs 

CMD_READ_ID_PT = 81
CMD_READ_ID_V = 82
CMD_READ_ID_FDC = 83 







class SerialLink:
    """Computer to Arduino Link """
 
    def __init__(self, port: str, baud: int = 115200, timeout: float = 1.0):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.conn: serial.Serial | None = None
 
    def open(self):
        self.conn = serial.Serial(self.port, self.baud, timeout=self.timeout)
        # TODO: any handshake/reset-wait logic your Arduino sketch needs
        # (e.g. Arduinos often reset on serial connect - you may need a
        # short sleep or a "ready" byte handshake here)
 
    def close(self):
        if self.conn:
            self.conn.close()
 
    def send_command(self, code: int):
        if not 0 <= code <= 255:
            raise ValueError(f"Command code out of range for 1 byte: {code}")
        payload = struct.pack("B", code)
        self.conn.write(payload) # sends the bit value'

    def read_response(self, terminator: bytes = b'\n') -> str:
        """Read a line of text response from the device."""
        if not self.conn:
            return ""
        line = self.conn.readline()  # blocks until terminator or timeout
        return line.decode('utf-8', errors='replace').strip()

 

class PIBShell(cmd.Cmd):
    intro = "Welcome to the PIB shell. Use with an arduino to command the payload interface board of MonARCH. Type help or ? to list commands.\n"
    prompt = "(pib) "

    def __init__(self, pib: SerialLink):
        super().__init__()
        self.pib = pib

    def do_greet(self, arg):
        """Greet the user."""
        print(f"Hello, {arg}!")

    def do_exit(self, arg):
        """Exit the shell."""
        print("Exiting the PIB shell.")
        return True

    def do_toggle_red_led(self, arg):
        """Toggling the RED LED on the payload interface board."""
        print("Toggling LED...")
        self.pib.send_command(CMD_TOGGLE_RED_LED)  

    def do_toggle_green_led(self, arg):
        """Toggling the GREEN LED on the payload interface board."""
        print("Toggling LED...")
        self.pib.send_command(CMD_TOGGLE_GREEN_LED)

    def do_toggle_amber_led(self, arg):
        """Toggling the GREEN LED on the payload interface board."""
        print("Toggling LED...")
        self.pib.send_command(CMD_TOGGLE_AMBER_LED)

    def do_open_valve(self, arg):
        """Open the valve on the payload interface board."""
        try: 
            valve = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 18.")
            return

        if(valve < 1 or valve > 18):
            print("Invalid valve number. Please enter a number between 1 and 18.")
            return
        else:
            print("Opening valve " + arg + "...")
            self.pib.send_command(CMD_OPEN_SOL1 + (valve-1)) # takes valve 1 and adds the valve number to obtain the correct command.
            
      
    def do_close_valve(self, arg):
        """Close the valve on the payload interface board."""
        try: 
            valve = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 18.")
            return

        if(valve < 1 or valve > 18):
            print("Invalid valve number. Please enter a number between 1 and 18.")
            return
        else:
            print("Closing valve " + arg + "...")
            self.pib.send_command(CMD_CLOSE_SOL1 + (valve-1)) # takes valve 1 and adds the valve number to obtain the correct command.
    def do_read_cj_temp(self,arg):
        """Read the cold junction temperature from the payload interface board."""
        try: 
            sensor = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            return

        if(sensor < 1 or sensor > 5):
            print("Invalid sensor number. Please enter a number between 1 and 5.")
            return
        else:
            print("Reading cold junction temperature from sensor " + arg + "...")
            self.pib.send_command(CMD_READ_TC1_CJ + (sensor - 1)) # takes sensor 1 and adds the sensor number - 1 to obtain the correct command.
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Celcius degrees")

    def do_read_temp(self, arg):
        """Read the temperature from the payload interface board."""
        try: 
            sensor = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            return

        if(sensor < 1 or sensor > 5):
            print("Invalid sensor number. Please enter a number between 1 and 5.")
            return
        else:
            print("Reading temperature from sensor " + arg + "...")
            self.pib.send_command(CMD_READ_TC1 + (sensor - 1)) # takes sensor 1 and adds the sensor number - 1 to obtain the correct command.
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Celcius degrees")

    def do_read_pressure(self, arg):
        """Read the pressure from the payload interface board."""
        try: 
            sensor = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            return

        if(sensor < 1 or sensor > 8):
            print("Invalid sensor number. Please enter a number between 1 and 8.")
            return
        else:
            print("Reading pressure from sensor " + arg + "...")
            self.pib.send_command(CMD_READ_PT1 + (sensor - 1)) # takes sensor 1 and adds the sensor number - 1 to obtain the correct command.
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Pa") 

    def do_read_capacitancez(self, arg):
        """Read the capacitance chip from the payload interface board."""
        print("Reading pressure from sensor " + arg + "...")

        try: 
            sensor = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return 
        
        self.pib.send_command(CMD_READ_PT1 + (sensor - 1)) # takes sensor 1 and adds the sensor number - 1 to obtain the correct command.
        response = self.pib.read_response()
        if response:
            print(f"PIB says: {response}" + " Pa") 

    def do_read_level(self, arg):
        """Read the level of the FAM142 propellant from the payload interface board."""
        print("Reading propellant level from sensor " + arg + "...")





         
    def do_read_valve_state(self, arg):
        """Read the valve state on the payload interface board."""
        try: 
            valve = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 18.")
            return

        if(valve < 1 or valve > 18):
            print("Invalid valve number. Please enter a number between 1 and 18.")
            return
        else:
            print("Reading valve " + arg + "...")
            self.pib.send_command(CMD_READ_VALVE_STATE_1 + (valve - 1)) # takes valve 1 and adds the valve number - 1 to obtain the correct command.
            response = self.pib.read_response()
            if response:
                state = int(response)
                if(state):
                    print("Valve ON")
                else:
                    print("Valve OFF")
            

    def do_read_3v3(self, arg):
        """Read 3v3 Bus of the PIB"""
        try: 
            value = int(arg)

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return

        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider " + arg + "...")
            self.pib.send_command(CMD_READ_3V3_VB + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Volts") 

    def do_read_VBAT(self,arg):
        """Read VBAT Bus of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider " + arg + "...")
            self.pib.send_command(CMD_READ_VBAT_VA + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Volts") 

    def do_read_12VB(self, arg):
        """Read 12V Bus of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider " + arg + "...")
            self.pib.send_command(CMD_READ_12VB_VA + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Volts") 
    def do_read_12VA(self, arg):
        """Read 12V Bus of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider " + arg + "...")
            self.pib.send_command(CMD_READ_12VA_VB + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Volts") 


    def do_read_3v3_current(self, arg):
        """Read 3v3 current of the PIB"""
        try: 
            value = int(arg)

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return

        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider current" + arg + "...")
            self.pib.send_command(CMD_READ_3V3_VB_CURRENT + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Milli-Amps") 

    def do_read_VBAT_current(self,arg):
        """Read VBAT Currnet of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider current " + arg + "...")
            self.pib.send_command(CMD_READ_VBAT_VA_CURRENT + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Milli-Amps") 

    def do_read_12VB(self, arg):
        """Read 12V Current of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider current" + arg + "...")
            self.pib.send_command(CMD_READ_12VB_VA_CURRENT + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Milli-Amps") 
    def do_read_12VA(self, arg):
        """Read 12V Current of the PIB"""
        try: 
            value = int(arg)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 2.")
            return
        if(value <1 or value > 2):
            print("Invalid voltage divider number. Please enter either 1 or 2.")
            return
        else:
            print("Reading voltage divider current" + arg + "...")
            self.pib.send_command(CMD_READ_12VA_VB_CURRENT + (value - 1)) 
            response = self.pib.read_response()
            if response:
                print(f"PIB says: {response}" + " Milli-Amps") 









      
    def do_run_sequence(self, arg):
        """Run a predefined sequence on the payload interface board."""
        
        print(arg)

        if(arg == "fill_accum1"):
            print("Running fill accumulator sequence 1...")
            # Here add the code to run sequence 1 on the PIB

        if(arg == "run_espray"):
            print("Running e-spray sequence...")

        # Here add the code to open the valve on the PIB

    def do_help(self, arg):
        """List available commands with "help" or detailed help with "help cmd"."""
        super().do_help(arg) 


def parse_args(): # Parse command-line arguments when running the script directly. This allows the user to specify the serial port and baud rate for the Arduino connection.
    parser = argparse.ArgumentParser(description="PIB command-line interface")
    parser.add_argument(
        "--port",
        default="COM12",
        help="Serial port the Arduino is connected to (default: %(default)s)",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="Baud rate for the serial link (default: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    link = SerialLink(port=args.port, baud=args.baud)
    link.open()
    try:
        PIBShell(link).cmdloop()
    finally:
        link.close()