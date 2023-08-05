from hardwareMaster import client
from scheduler import Routine

cli = client()
rout = Routine()

def bfnc(*args):
    msg = cli.send_qry('input_pump_status')
    print(f'{rout.ext_timer()}: {msg}')
    if msg[0] == '0':
        return True

cli.send_cmd('en_input_pump')
rout.add_break_functions(bfnc, None)
rout.run()