import serial
import math

# formats the line as: numpoints-x,y,x,y,x,y,x,y...
def formatMessage(message):
    points = ""
    for i in message:
        points += str(i).strip("(").replace(")", ",").replace(" ", "")

    msg = f"{len(message)}-{points}"[:-1]
    return msg


# chops up big messages for the arduino
class Comms:
    def __init__(self, port: str, baud: int = 115200):
        self._serial = serial.Serial(port, baud, timeout=10)
        self.chunkSize = 128

    def _short(self, message):
        self._serial.write(message.encode())
        return self._serial.readline()[:-2]

    def _long(self, message):
        res = self._short("RCV " + str(len(message)) + "\n")
        if res.decode() != "RDY":
            return None

        for i in range(int(math.ceil(len(message) / self.cmdChunkSize))):
            c = message[128 * i : 128 * (i + 1)]
            response = self._shortCmd(c)
        return self._serial.readline().strip()

    def send(self, message):
        msg = formatMessage(message)
        print(msg)
        if len(msg) < 128:
            res = self._short(msg + "\n")
        else:
            res = self._long(msg)
        print(res)
