Created By Kacper Paraniuk 07-09-26 


This markdown file discusses the structure of the payload interface shell (command line interface) and how to set it up 

uv — project + dependency management (replaces pip/venv juggling)

UV 

cmd module || read more here: https://docs.python.org/3/library/cmd.html

pyserial — external dependency for the serial side
cmd (Python stdlib, no install needed) — gives nice terminal commanding functionality  


HOW TO SET UP DEPENDENCIES:

*If you do not have UV installed: 

1. UV INSTALLATION (https://docs.astral.sh/uv/getting-started/installation/)

- type in terminal inside of project directory and run >

WINDOWS - 

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

MAC - 

curl -LsSf https://astral.sh/uv/install.sh | sh


RESTART TERMINAL TO ADD UV TO PATH 

2. PYTHON

If you do not have python no worries UV can manage your python type (https://docs.astral.sh/uv/guides/install-python/) If you have python skip this step. 

uv python install

3. RUNNING THE CODE


cd pib-cli # make sure you are in the pib-cli folder

uv run python main.py (port default = 12 | baud rate default = 115200) 

OR

uv run python main.py --port {Input COMX} --baud {Input Baud Rate}

Allows the user to specify the serial port and baud rate for the Arduino connection.


4. Commanding the PIB!

If you sucessfully executed the program then you should see the following message:
    "Welcome to the PIB shell. Use with an arduino to command the payload interface board of MonARCH. Type help or ? to list commands."

Now you can start running various commands.

See the command .md [Commanding the PIB](INSERT THE LINK)

// make this a git repo that is more friendly to look at 

Common Errors: 

 >   raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))

This is due to the python script failing a handshake with the arduino board. Please check the connection between computer and arduino board. Also check if you are specifiying the correct port the device is identified at. 

