import numpy as np
import os
import SimpleHTTPServer
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler, test
#
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()

class DynamixelMotor:
    # Control table address
    ADDR_PRO_TORQUE_ENABLE = 64  # Control table address is different in Dynamixel model
    ADDR_PRO_GOAL_POSITION = 116
    ADDR_PRO_PRESENT_POSITION = 132
    ADDR_PRO_PROFILE_VELOCITY = 112
    ADDR_PRO_OPERATING_MODE = 11
    ADDR_PRO_GOAL_VELOCITY = 104

    # Protocol version
    PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

    # Default setting
    DXL_ID = 1  # Dynamixel ID : 1
    DXL_ID2 = 2
    BAUDRATE = 57600  # Dynamixel default baudrate : 57600
    DEVICENAME = '/dev/tty.usbserial-FT2H2MO1'  # Check which port is being used on your controller
    # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

    TORQUE_ENABLE = 1  # Value for enabling the torque
    TORQUE_DISABLE = 0  # Value for disabling the torque
    DXL_MINIMUM_POSITION_VALUE = 10  # Dynamixel will rotate between this value
    DXL_MAXIMUM_POSITION_VALUE = 4000  # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
    DXL_MOVING_STATUS_THRESHOLD = 20  # Dynamixel moving status threshold

    def __init__(self):
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(self.DEVICENAME)

        # Initialize PacketHandler instance
        # Set the protocol version
        # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

    def torque_enable(self, motor_id):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, motor_id, self.ADDR_PRO_TORQUE_ENABLE,
                                                                  self.TORQUE_ENABLE)

    def read_position(self, motor_id):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, motor_id,
                                                                                       self.ADDR_PRO_PRESENT_POSITION)
        return dxl_present_position

    def write_position(self, motor_id, goal_position):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, self.ADDR_PRO_GOAL_POSITION, goal_position)


class CORSRequestHandler(SimpleHTTPRequestHandler):

    motor_actuation = DynamixelMotor()
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # prepare for response
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_str = self.rfile.read(content_length)
        print(post_str)

        if post_str == "lamp_up":
            self.motor_actuation.torque_enable(5)
            self.motor_actuation.write_position(5, 3700)
        elif post_str == "lamp_down":
            self.motor_actuation.torque_enable(5)
            self.motor_actuation.write_position(5, 0)
        elif post_str == "trash_open":
            self.motor_actuation.torque_enable(2)
            self.motor_actuation.write_position(2, 700)
        elif post_str == "trash_close":
            self.motor_actuation.torque_enable(2)
            self.motor_actuation.write_position(2, 1200)

# class CORSHTTPRequestHandler(BaseHTTPRequestHandler):
#     def __init__(self, request, client_address, server):
#         BaseHTTPRequestHandler.__init__(self, request, client_address, server)
#
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     def do_POST(self):
#         # prepare for response
#         self._set_headers()
#
#     def end_headers(self):
#         self.send_header('Access-Control-Allow-Origin', '*')
#         super(CORSHTTPRequestHandler, self).end_headers(self)
#
# class S(BaseHTTPRequestHandler):
#
#     def send_head(self):
#         """Common code for GET and HEAD commands.
#         This sends the response code and MIME headers.
#         Return value is either a file object (which has to be copied
#         to the outputfile by the caller unless the command was HEAD,
#         and must be closed by the caller under all circumstances), or
#         None, in which case the caller has nothing further to do.
#         """
#         path = self.translate_path(self.path)
#         f = None
#         if os.path.isdir(path):
#             if not self.path.endswith('/'):
#                 # redirect browser - doing basically what apache does
#                 self.send_response(301)
#                 self.send_header("Location", self.path + "/")
#                 self.end_headers()
#                 return None
#             for index in "index.html", "index.htm":
#                 index = os.path.join(path, index)
#                 if os.path.exists(index):
#                     path = index
#                     break
#             else:
#                 return self.list_directory(path)
#         ctype = self.guess_type(path)
#         try:
#             # Always read in binary mode. Opening files in text mode may cause
#             # newline translations, making the actual size of the content
#             # transmitted *less* than the content-length!
#             f = open(path, 'rb')
#         except IOError:
#             self.send_error(404, "File not found")
#             return None
#         self.send_response(200)
#         self.send_header("Content-type", ctype)
#         fs = os.fstat(f.fileno())
#         self.send_header("Content-Length", str(fs[6]))
#         self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
#         self.send_header("Access-Control-Allow-Origin", "*")
#         self.end_headers()
#         return f
#
#     def __init__(self, request, client_address, server):
#         BaseHTTPRequestHandler.__init__(self, request, client_address, server)
#
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     def do_POST(self):
#         # prepare for response
#         self._set_headers()
#
def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()
    # BaseHTTPServer.test(handler_class, server_class)

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

# from SimpleHTTPServer import SimpleHTTPRequestHandler
# import BaseHTTPServer
#
# class CORSRequestHandler (SimpleHTTPRequestHandler):
#     def end_headers (self):
#         self.send_header('Access-Control-Allow-Origin', '*')
#         SimpleHTTPRequestHandler.end_headers(self)
#
# if __name__ == '__main__':
#     BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)