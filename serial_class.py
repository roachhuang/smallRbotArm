import serial.tools.list_ports
import serial
import platform
from threading import Thread, Event

class SerialPort():
    def __init__(self):                
        port = self._get_serial_port()
        if port:
            self.ser = serial.Serial(port, baudrate=115200, timeout=1)
            print(f"Connected to serial port {self.ser.name}")
            self._event_ok2send = Event()
            self._event_ok2send.set()

            self._event_run = Event()
            self._event_run.set()

            self.t = Thread(target=self._ReceiveThread, args=[])
            self.t.start()
            # do something with the serial connection
        else:
            print("Could not find a suitable serial port.")

    @property
    def event_run(self):
        return self._event_run.is_set()    

    @event_run.setter
    def event_run(self, state):
        if state == True:
            self._event_run.set()
        else:
            self._event_run.clear()

    def _get_serial_port(self):
        """Automatically detects and returns the serial port."""
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if 'USB' in port.description:
                return port.device
        return None

    def send2Arduino(self, header: str, j, bWaitAck: bool):
        """send robot cmd to arduino

        Args:
            ser (_type_): _description_
            header (str): cmd type
            j (float): theta in deg for 6 axes
            bWaitAck (bool): wait for ack from arduino or not
        """
        # msg = f'{header}{j[0]:.2f},{j[1]:.2f},{j[2]:.2f},{j[3]:.2f},{j[4]:.2f},{j[5]:.2f}\n'
        msg = '{}{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n'.format(header, *j,)
        self.ser.write(msg.encode('utf-8'))
        self._event_ok2send.clear()
        print(msg)
        if bWaitAck is True:
            # wait till the event is set in rcvThread.
            self._event_ok2send.wait()            
        # while event_ack.is_set() and bWaitAck is True:
        #    pass

    def _ReceiveThread(self):
        """
        input string is retrieved as a byte string, which works
        differently than a standard string. The decode() method is to convert
        the string from a byte string to a standard string.
        """
        while self.event_run == True:            
            line = self.ser.readline().decode('utf-8')
            if len(line) > 0:
                # get rid of the end of characters /n/r
                string = line.rstrip()
                # logging.warning(string)
                # print(string)
                if string == 'ack':
                    # receive ack frm arduion meaning it is free now
                    self._event_ok2send.set()
