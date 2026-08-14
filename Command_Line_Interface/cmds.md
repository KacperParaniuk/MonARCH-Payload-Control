Created By Kacper Paraniuk 07-06-26 

This is a markdown file containing the commands for cli of the payload interface board 

[Command Structure](#command-structure)

[Commands Explanation](#commands-explanation)

[Commands](#commands)



# Command Structure

The command structure is:

 <verb> <target> 


# Commands Explanation: 

Sensors 
-----------------------------------------------------------------------------------------------------------

<verb> <target> <[num]>

ex: 

read_cj_temp 1 

read_pressure 2

read_temp 5


Actions 
-----------------------------------------------------------------------------------------------------------
<verb> <target> <[num]>

ex: 

open_valve 3

toggle_red_led

Events -----------------------------------------------------------------------------------------------------------

<verb> <event>

ex: 

run_sequence fill_accum1

run_sequence run_espray 


# PIB Shell Commands

| Command | Usage | Description |
|---|---|---|
| `greet` | `greet <text>` | Echoes back `Hello <text>` |
| `exit` | `exit` | Echoes `Exiting the PIB shell.` and exits the script |
| `help` | `help` | Returns a list of commands
| `toggle_red_led` | `toggle_red_led` | Toggles the red debug LED on the PIB |
| `open_valve` | `open_valve <valve #>` | Opens the specified valve |
| `close_valve` | `close_valve <valve #>` | Closes the specified valve |
| `read_cj_temp` | `read_cj_temp <sensor #>` | Returns the cold junction temperature |
| `