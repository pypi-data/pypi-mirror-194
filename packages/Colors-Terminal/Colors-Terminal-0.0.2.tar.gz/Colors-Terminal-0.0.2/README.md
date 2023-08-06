# colors_terminal

## Installation

`pip install Colors-Terminal`
## Usage

	from colors_terminal.colors import colors
	
	color = Colors()
	
	color.print(f"{color.red}Hello world!", colored=True)
	# Print text without color
	color.print("Hello world!", colored=False)
	# If colored is active the color will be seen if it is off it will not be seen
### Colors
black
white
blue
red
yellow
green
orange
purple