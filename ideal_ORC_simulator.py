#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:43:53 2018

@author: wei
"""

from CoolProp.CoolProp import PropsSI
from thermo.node import Node


def main(tl, th, delta_subcool, delta_supheat, out, wan=False):
    '''


    Parameters
    ----------
    tl : TYPE
        DESCRIPTION.
    th : TYPE
        DESCRIPTION.
    delta_subcool : TYPE
        DESCRIPTION.
    delta_supheat : TYPE
        DESCRIPTION.
    out : TYPE
        DESCRIPTION.
    wan : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    '''
    if wan == True:
        print('小萬')
    tl = tl
    th = th
    delta_supheat = -delta_supheat
    delta_subcool = delta_subcool

    pl = PropsSI('P', 'T', (tl + delta_subcool) +
                 273.15, 'Q', 0, 'R245FA') / 1e5
    if wan == True:
        ph = pl + 7
    else:
        ph = PropsSI('P', 'T', (th + delta_supheat) +
                     273.15, 'Q', 0, 'R245FA') / 1e5

    point_name = ['pump_in', 'pump_out', 'exp_in', 'exp_out']
    points = []
    for index, point in enumerate(point_name, start=1):
        points.append(Node(point, index))

    # node 1 Isobaric process
    points[0].t = tl
    points[0].p = pl
    points[0].pt()

    # node 2 Isentropic process
    points[1].p = ph
    points[1].s = points[0].s
    points[1].ps()

    # node 3 Isobaric process
    points[2].t = th
    points[2].p = ph
    points[2].pt()

    # node 4 Isentropic process
    points[3].p = pl
    points[3].s = points[2].s
    points[3].ps()

    for i in range(4):
        print(points[i])

    expact_output = out  # 500w
    mdot = round(expact_output / (points[2].h-points[3].h), 5)  # kg/s
    mdot_lpm = round((mdot * 60000 / points[1].d), 4)
    eff = round(
        ((points[2].h-points[3].h) - (points[1].h-points[0].h)) * 100 /
        (points[2].h-points[1].h), 1)

    print('期望輸出: {}w,\t質量流率: {}kg/s,\t質量流率: {}LPM,\tEFF: {}%'.format(expact_output, mdot, mdot_lpm, eff))


if __name__ == '__main__':
    main(30, 100, 5, 5, 500, True)
    main(15, 100, 5, 5, 500, True)
    main(25, 100, 5, 5, 500)
    main(30, 100, 5, 5, 600)
    main(15, 100, 5, 5, 300)
