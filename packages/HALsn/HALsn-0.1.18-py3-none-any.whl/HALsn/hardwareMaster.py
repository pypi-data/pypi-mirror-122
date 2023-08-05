#!/usr/bin/env python3

'''
MIT License

Copyright (c) 2021 Mikhail Hyde & Cole Crescas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from serialSupervisor import serialRoot
import socket

class socketRoot:

    def __init__(self, is_server=False):

        self.HEADER = 8
        self.PORT   = 5050
        self.SERVER = '10.0.0.110'
        self.ADDR   = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'

        self.DC_MSG = '!DC'

        self.node  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if is_server:
            self.node.bind(self.ADDR)
        else:
            self.node.connect(self.ADDR)

class server(socketRoot):
    def __init__(self, is_server=True):
        
        super().__init__(is_server)

        self.ard = serialRoot(device_path='/dev/ttyACM0',
                              baud=115200,
                              timeout=0.25)
        self.ard.open_port()

    def start(self):
        
        self.node.listen()
        print(f"[LISTENING] Server is listening on {self.node}")
        
        while True:
            
            conn, addr = self.node.accept()
            print(f"[NEW CONNECTION] {addr} connected.")
            
            while True:
                
                msg_len = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_len:
                    msg_len = int(msg_len)
                    msg = conn.recv(msg_len).decode(self.FORMAT)
                    
                    if msg == self.DC_MSG:
                        conn.close()
                        break

                    print(f'[{addr}] {msg}')
                    msg_tag = msg[0]
                    msg     = msg[1:]
                    self.ard._send_msg(msg)                
                    if msg_tag == '?':
                        conn.send(self.ard._read_msg().encode(self.FORMAT))

class client(socketRoot):

    def __init__(self):
    
        super().__init__()

        self.node_id = input('Enter ID: ')#socket.gethostname()[4:]

        self.commands = {
            # Enable Input Pump for Bay N
            'en_input_pump':       '*0x01!',
            # Disable Input Pump for Bay N
            'dis_input_pump':      '*0x00!',
            # Enable Output Pump for Bay N
            'en_output_pump':      '*1x01!',
            # Disable Output Pump for Bay N
            'dis_output_pump':     '*1x00!',
            # Set Output Pump Timer - 10 Seconds
            'output_time_10':      '*3x10!',
            # Set Output Pump Timer - 20 Seconds
            'output_time_20':      '*3x20!',
            # Set Output Pump Timer - 30 Seconds
            'output_time_30':      '*3x30!',
            # Set Output Pump Timer - 40 Seconds
            'output_time_40':      '*3x40!',
            # Set Output Pump Timer - 50 Seconds
            'output_time_50':      '*3x50!',
            # Set Output Pump Timer - 60 Seconds
            'output_time_60':      '*3x60!',
        }

        self.queries  = {
            # Request Bay N Input Pump State
            'input_pump_status':   '*0x02!',
            # Request Bay N Output Pump State
            'output_pump_status':  '*1x02!',
            # Request Bay N Res Float State
            'res_float_status':    '*2x00!'
        }

    def disconnect(self):
        msg = self.DC_MSG.encode(self.FORMAT)
        self.formatted_send(msg)

    def send_cmd(self, cmd_id):
        msg     = '*' + self.node_id + self.commands[cmd_id]
        msg = msg.encode(self.FORMAT)
        msg_len = len(msg)
        header = str(msg_len).encode(self.FORMAT)
        header += b' ' * (self.HEADER - len(header))
        self.node.send(header)
        self.node.send(msg)

    def send_qry(self, qry_id):
        msg     = '?' + self.node_id + self.queries[qry_id]
        msg = msg.encode(self.FORMAT)
        msg_len = len(msg)
        header = str(msg_len).encode(self.FORMAT)
        header += b' ' * (self.HEADER - len(header))
        self.node.send(header)
        self.node.send(msg)
        return self.node.recv(2048).decode(self.FORMAT)
