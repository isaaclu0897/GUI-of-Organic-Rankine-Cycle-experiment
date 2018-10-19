import visa
import time
import node
from tabulate_text import ORC_status

# =============================================================================
# load the data
# =============================================================================
probe_type_TEMP, type_TEMP, ch_TEMP = 'TCouple', 'T', '@201:210'
range_PRESS,resolution_PRESS, ch_PRESS  = 10, 5.5, '@301:306'
gain_PRESS, offset_PRESS, label_PRESS, state_PRESS = 2.1, 0, 'BAR', 1
pumpi = {'name' : 'pump_inlet',         'nid' : 1}
pumpo = {'name' : 'pump_ioutlet',       'nid' : 2}
EXPi  = {'name' : 'expander_inlet',     'nid' : 3}
EXPo  = {'name' : 'expander_outlet',    'nid' : 4}
#CDSi  = {'name' : 'condenser_inlet',    'nid' : 5}
#CDSo  = {'name' : 'condenser_outlet',   'nid' : 6}


rm = visa.ResourceManager()
with rm.open_resource('USB0::0x0957::0x2007::MY49017447::0::INSTR') as v34972A:
    idn_string = v34972A.query('*IDN?')

    while 1:
        # scan temperature
        scans_TEMP = v34972A.query(':MEASure:TEMPerature? %s,%s,(%s)' % (probe_type_TEMP, type_TEMP, ch_TEMP))
        
        # scan pressure
        v34972A.write(':CONFigure:VOLTage:DC %G,%G,(%s)' % (range_PRESS,resolution_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:GAIN %G,(%s)' % (gain_PRESS, ch_PRESS))
        v34972A.write(':CALCulate:SCALe:STATe %d,(%s)' % (state_PRESS, ch_PRESS))
        scans_PRESS = v34972A.query(':READ?')
        
        # convert str to float
        readings_TEMP = [float(x) for x in scans_TEMP.split(',')]
        readings_PRESS = [float(x) for x in scans_PRESS.split(',')]
        
# =========================================================
# define the  of all point & init all node====================
# =============================================================================
        dev_list = [pumpi, pumpo, EXPi, EXPo]
        for i in range(4):
            dev_list[i]['P'] = readings_PRESS[i]
            dev_list[i]['T'] = readings_TEMP[i]
        nodes = []
        for i in dev_list:
            nodes.append(node.Node(i['name'], i['nid']))
            
        for i, obj in enumerate(dev_list):
            nodes[i].set_tp(obj['T'], obj['P'])
            nodes[i].pt()
        ORC_status([nodes[i] for i in range(len(nodes))])

        time.sleep(3)
rm.close()






