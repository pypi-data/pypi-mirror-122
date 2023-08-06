from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio
from digitalio import Direction

i2c = busio.I2C(board.SCL, board.SDA)

mcp_out1 = MCP23017(i2c, 0x26)
mcp_out2 = MCP23017(i2c, 0x27)
mcp_in1 = MCP23017(i2c, 0x20)
mcp_in2 = MCP23017(i2c, 0x21)

ListOut = []


def SetupIO(mcp):
    i = 0
    while i < 16:
        pin = mcp.get_pin(i)
        pin.direction = Direction.OUTPUT()
        ListOut.append(pin)
        pin.value = False
        pass
    pass

