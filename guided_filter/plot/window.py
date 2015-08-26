
# -*- coding: utf-8 -*-
## @package som_cm.plot.window
#
#  Matplot window functions.
#  @author      tody
#  @date        2015/07/29

from matplotlib import pyplot as plt


## Maximize the matplot window.
def showMaximize():
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()
