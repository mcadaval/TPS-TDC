# -*- coding: utf-8 -*-

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def graph_information(file_name, entropy):
    MAX_BARS = 30
    LEGEND = [u'Entropía']

    information = pd.read_csv(file_name)
    information.sort_index(ascending = True, inplace = True)
    information.reset_index(drop = True, inplace = True)

    plt.style.use('ggplot')
    fig, ax = plt.subplots()

    if len(information) > MAX_BARS:
        LEGEND = [u'Datos descartados', u'Entropía']
        number_of_rows_to_drop = len(information) - MAX_BARS
        middle_index = len(information) / 2
        dropped_indexes = range(middle_index - number_of_rows_to_drop / 2, middle_index)
        dropped_indexes = dropped_indexes + range(middle_index, middle_index + number_of_rows_to_drop / 2)
        information.drop(information.index[dropped_indexes], inplace = True)
        information.reset_index(drop = True, inplace = True)
        plt.axvline(x = MAX_BARS / 2 - 0.5, color = 'crimson', linestyle = '--', linewidth = 2)

    plt.axhline(y = entropy, color = 'coral', linestyle = '--', linewidth = 2)
    information.plot.bar(ax = ax, xticks = information.index, rot = 90, color = 'mediumseagreen')

    legend = ax.legend(LEGEND, loc = 'upper center', bbox_to_anchor = (0.5, -0.3), fancybox = True, shadow = True, ncol = 2)
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_linewidth(0)    

    ax.set_xticklabels(information.symbol)
    plt.xlabel(u'Símbolo')
    plt.ylabel(u'Información')
    plt.rcParams.update({'font.size': 8})
    plt.gcf().set_size_inches(7, 5)
    plt.savefig(file_name.replace('csv','pdf'), format='pdf', bbox_inches = 'tight', dpi = 100)

if __name__ == '__main__':
    try:
        graph_information(sys.argv[1], sys.argv[2])
    except IndexError as e:
        print('Usage: python graphInformation.py <information_file> <source_entropy>')