# ------------------------------------------------- -----
# -------------------- mplwidget.py --------------------
# -------------------------------------------------- ----
from  PyQt5.QtWidgets  import *
from PyQt5 import QtCore
import matplotlib

from  matplotlib.backends.backend_qt5agg  import   FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from  matplotlib.figure  import  Figure
from matplotlib import rcParams




#sets the matplotlib backend that renders the plots. Agg is the default backend.
# Without this line there are issues when closing 3d plots, don't know why
matplotlib.use('Agg')

# this class is used to display matplotlib plots on QWidgets when there is only one plot to be shown. MplWidget
#is a subclass of QWidget. This means that it can be implemented in the GUI like any other widget
class  MplWidget ( QWidget ):


    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )

        self.figure = Figure()
        self . canvas  =  FigureCanvasQTAgg ( self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        vertical_layout  =  QVBoxLayout ()

        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)

        

        self . setLayout ( vertical_layout )



#same as above but without toolbar. Used for experimental plots in general tab
class  MplWidget1 ( QWidget ):

    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )

        self.figure = Figure(tight_layout=True)
        self . canvas  =  FigureCanvasQTAgg ( self.figure)
        vertical_layout  =  QVBoxLayout ()
        vertical_layout.addWidget(self.canvas)


        self . setLayout ( vertical_layout )
# this class is used to display matplotlib plots on QWidgets when two plots should be shown (spc_vs_theta).
# MplWidget_for_two_plots is a subclass of QWidget. This means that it can be implemented in the GUI like any other widget
class  MplWidget_for_two_plots ( QWidget ):

    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        vertical_layout  =  QVBoxLayout ()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)

        # add_subplot(121) means 2*1 grid (two columns one row), first subplot
        self . ax1  =  self . figure . add_subplot ( 121 )
        self.ax2 = self.figure.add_subplot(122)
        self . setLayout ( vertical_layout )

#same as above but toolbar is on top of plot
class  MplWidget_for_two_plots_1 ( QWidget ):

    def  __init__ ( self ,  parent  =  None ):

        QWidget . __init__ ( self ,  parent )

        self.figure = Figure()
        self.figure.subplots_adjust(wspace = 0.5, hspace=0.5, bottom = 0.17, top = 0.9)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


        vertical_layout  =  QVBoxLayout ()
        vertical_layout.addWidget(self.toolbar)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Ignored)
        vertical_layout.addSpacerItem(spacerItem)
        vertical_layout.addWidget(self.canvas)


        # add_subplot(121) means 2*1 grid (two colums one row), first subplot
        self . ax1  =  self . figure . add_subplot ( 121 )
        self.ax2 = self.figure.add_subplot(122)
        self . setLayout ( vertical_layout )


class MplWidget_for_plot_grid (QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.figure = Figure(tight_layout=False)
        #self.figure.subplots_adjust(wspace=0.2, hspace=0.5, left =0.1, right = 1.05, bottom = 0.2 ,top = 0.8)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.toolbar)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Ignored)
        vertical_layout.addSpacerItem(spacerItem)
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)

        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4 = None
        self.ax5 = None
        self.ax6 = None
        self.ax7 = None
        self.ax8 = None
        self.ax9 = None
        self.ax10 = None
        self.ax11 = None
        self.ax12 = None
        self.ax13 = None
        self.ax14 = None
        self.ax15 = None
        self.ax16 = None

        self.subplot_list = [self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6, self. ax7, self. ax8,
                            self.ax9, self.ax10, self. ax11, self.ax12, self.ax13, self.ax14, self.ax15, self.ax16]

        self.subplot_list_2 = [[self.ax1, self.ax2], [self.ax3, self.ax4], [self.ax5, self.ax6], [self.ax7, self.ax8],
                             [self.ax9, self.ax10], [self.ax11, self.ax12],[ self.ax13, self.ax14], [self.ax15, self.ax16]]

        self.colorbar = None





