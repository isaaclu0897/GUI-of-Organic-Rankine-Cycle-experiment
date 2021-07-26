#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 23:04:07 2021

@author: wei
"""

import sys
sys.path.append('../')

if __name__ == "__main__":
    from matplotlib.pyplot import figure
    from matplotlib.pyplot import show
    from matplotlib.lines import Line2D
    from thermo.node import Node
    from thermo.plot import calc_SaturationofCurve, calc_StatusofORC, ProcessPlot

    def set_windows():
        fig = figure()
        dia = fig.add_subplot(1, 1, 1)
        xAxis = "s"
        yAxis = "T"
        title = {"T": "T, °C", "s": "s, (kJ/kg)*K"}
        dia.set_title("%s-%s Diagram" % (yAxis, xAxis))
        dia.set_xlabel(title[xAxis])
        dia.set_ylabel(title[yAxis])
        dia.set_ylim(10, 135)
        dia.set_xlim(1.05, 1.88)
        dia.grid()
        return dia

    # set label
    dia = set_windows()
    # plot Saturation of Curve
    sat_line = calc_SaturationofCurve()
    dia.add_line(sat_line[0])
    dia.add_line(sat_line[1])

    # import data

    def data():
        pumpi = {'name': 'pump_inlet',         'nid': 1, 'P': 2.01, 'T': 21.86}
        pumpo = {'name': 'pump_ioutlet',       'nid': 2, 'P': 6.44, 'T': 22.55}
        EVPo = {'name': 'evaparator_outlet',  'nid': 3, 'P': 6.11, 'T': 88.31}
        EXPi = {'name': 'expander_inlet',     'nid': 4, 'P': 6.27, 'T': 88.28}
        EXPo = {'name': 'expander_outlet',    'nid': 5, 'P': 2.05, 'T': 64.03}
        CDSi = {'name': 'condenser_inlet',    'nid': 6, 'P': 1.99, 'T': 56.68}
        CDSo = {'name': 'condenser_outlet',   'nid': 7, 'P': 1.98, 'T': 22.12}

        return [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo]
    dev_list = [pumpi, pumpo, EVPo, EXPi, EXPo, CDSi, CDSo] = data()

    # init node
    nodes = [Node(i["name"], i["nid"]) for i in dev_list]
    for i, obj in enumerate(dev_list):
        nodes[i].set_tp(obj["T"], obj["P"])
        nodes[i].pt()

    # plot status of ORC
#    plot_StatusofORC(nodes)
    state_point = calc_StatusofORC(nodes, [1, 2, 3, 4])
    x, y = state_point
    state_point_line = Line2D(x, y, color='b', linestyle='None', marker='o')
    dia.add_line(state_point_line)
    """ example
    ProcessPlot(0, 1, 'isos').plot_process
    a=ProcessPlot(3, 4, 'isos')
    a.iso_line(nodes)
    a.calc_iso()
    a.calc_stateline()
    plot process of ORC
    """
    process = [ProcessPlot(0, 1, 'isos'),
               ProcessPlot(1, 2, 'isop'),
               ProcessPlot(2, 3, 'isop'),
               ProcessPlot(3, 4, 'isos'),
               ProcessPlot(4, 5, 'isop'),
               ProcessPlot(5, 6, 'isop'),
               ProcessPlot(6, 0, 'isop')]
#    good = [plot.plot_process(nodes) for plot in process]
#    for i in good:
#        act_line =
#        dia.add_line(i[0])
#        dia.add_line(i[1])
    good = [plot.plot_process_data(nodes) for plot in process]

    for i in good:
        iso = Line2D(i[0][0], i[0][1], color="grey", lw=2.0)
        dia.add_line(iso)
#        dia.add_line(i[1])

    show()
