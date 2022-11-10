"""
########################################################################
The evaluations.py module contains the Visualize and Analyze classes,
which provide tools for evaluating pyfao56 Model output.

The evaluations.py module contains the following:
    Visualize - A class for visualizing pyfao56 Model output
    Analyze   - A class for numerically analyzing pyfao56 Model output

11/9/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import matplotlib.pyplot as plt
import seaborn as sns


class Visualize:
    """A class for visualizing pyfao56 Model output

    Attributes
    ----------
    mdl : pyfao56 Model class
        Provides data to evaluate.
    edata : Dataframe
        All of the data to be evaluated.
    swd : pyfao56 Tools SoilWaterDeficit class, optional
        Provides observed soil water deficit data to evaluate
        (default = None)

    Methods
    -------
    """

    def __init__(self, mdl, swd=None):
        """super informative docstring"""

        self.mdl = mdl
        self.swd = swd
        self.edata = mdl.odata.loc[:, ~mdl.odata.columns.duplicated()].copy()

    def plot_Dr(self, raw=False, water_events=False, ks=False,
                title=None, save=None, show=True):
        """informative docstring"""

        # Creating variables for info that is used or changed often
        edata     = self.edata
        if self.swd is not None:
            swddata   = self.swd.rzdata
        x         = 'DOY'
        # Labels
        plt_title = 'pyfao56 Soil Water Depletion'
        x_l       = 'Day of Year (DOY)'
        y_l       = 'Water Amount (mm/day)'
        y2_l      = 'Ks (FAO-56 stress coefficient)'
        dr_l      = 'Root Zone Depletion'
        drmax_l   = 'Max Root Depth Depletion'
        raw_l     = 'Modeled Readily Available Water (RAW)'
        ks_l      = 'pyfao56 Ks'
        # Colors
        bg_c      = 'whitesmoke'
        dr_c      = 'darkcyan'
        drmax_c   = 'darkturquoise'
        raw_c     = 'mediumorchid'
        water_c   = 'navy'
        ks_c      = 'lightsalmon'

        # Creating figure:
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(20)

        # Setting axis labels:
        ax.set(xlabel=x_l, ylabel=y_l)

        # Setting axis ticks:
        # x axis:
        mykey = self.mdl.startDate.strftime('%Y-%j')
        start_doy = int(self.edata['DOY'].loc[mykey])
        x_tick_start = -1 * (start_doy % 5)
        ax.set_xticks(range(x_tick_start, start_doy, 5))
        # y axis:
        swd_max = round(self.edata['Dr'].max())
        swd_max += (swd_max % 10) + 10
        ax.set_ylim(1, swd_max)
        ax.set_yticks(range(5, swd_max, 5))

        # Changing the background color of the plot
        ax.set_facecolor(bg_c)

        # Adding gridlines to the plot
        ax.grid(ls=":")

        # Making Dr lineplot
        sns.lineplot(data=edata, x=x, y='Dr',
                     color=dr_c, label='Modeled '+dr_l)

        # Making Drmax lineplot if available
        if self.mdl.sol is not None:
            sns.lineplot(data=edata, x=x, y='Drmax',
                         color=drmax_c, label='Modeled '+drmax_l)

        # Adding observed SWD if available:
        if self.swd is not None:
            sns.scatterplot(data=swddata, x=x, y='SWDr',
                            color=dr_c, marker='s', s=50,
                            label='Measured '+drmax_l)
            if self.mdl.sol is not None:
                sns.scatterplot(data=swddata, x=x, y='SWDrmax',
                                color=drmax_c, marker='s', s=50,
                                label='Measured '+drmax_l)

        # Adding RAW lineplot if requested
        if raw:
            sns.lineplot(data=edata, x=x, y='RAW',
                         color=raw_c, label=raw_l)

        # Adding water events if requested
        if water_events:
            sns.scatterplot(data=edata, x=x, y='Rain',
                            color=water_c, marker='+', s=75,
                            label='Rain')
            sns.scatterplot(data=edata, x=x, y='Irrig',
                            color=water_c, marker='x', s=75,
                            label='Irrigation')

        # Adding Ks lineplot if requested
        if ks:
            ax2 = ax.twinx()
            ax2.set_ylim(0, 1.7)
            ax2.set_yticks([x * 0.25 for x in range(0, 5)])
            ax2.set(ylabel=y2_l)
            sns.lineplot(data=edata, x=x, y='Ks',
                         color=ks_c, label=ks_l)

        # Adding plot title - either user-defined or default
        if title is None:
            plt.title(plt_title)
        else:
            plt.title(title)

        # Making legend for the plot
        ax.legend(loc='upper left')

        # Saving and Showing the plot (if desired)
        if save is not None:
            plt.savefig(save)
        if show:
            plt.show()
        else:
            plt.close(fig)

    def plot_ET(self, water_events=False,
                title=None, save=None, show=True):
        """informative docstring"""

        # Creating variables for info that is used or changed often
        edata     = self.edata
        x         = 'DOY'
        # Labels
        plt_title = 'pyfao56 Evapotranspiration (ET)'
        x_l       = 'Day of Year (DOY)'
        y_l       = 'Water Amount (mm/day)'
        # y2_l      = 'Ks (FAO-56 stress coefficient)'
        etr_l     = 'Reference ET'
        etc_l     = 'Crop ET'
        etcadj_l  = 'Adjusted Crop ET'
        # Colors
        bg_c      = 'whitesmoke'
        etr_c     = 'darkmagenta'
        etc_c     = 'firebrick'
        etcadj_c  = 'plum'
        water_c   = 'navy'

        # Creating figure:
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(20)

        # Setting axis labels:
        ax.set(xlabel=x_l, ylabel=y_l)

        # Setting axis ticks:
        # x axis:
        mykey = self.mdl.startDate.strftime('%Y-%j')
        start_doy = int(self.edata['DOY'].loc[mykey])
        x_tick_start = -1 * (start_doy % 5)
        ax.set_xticks(range(x_tick_start, start_doy, 5))
        # y axis:
        etr_max = round(self.edata['ETref'].max())
        etr_max += (etr_max % 5)
        ax.set_ylim(0, etr_max)
        ax.set_yticks(range(0, etr_max, 2))
        # ax.set_yticks([x * 2.5 for x in range(0, (int(etr_max/2)))])

        # Changing the background color of the plot
        ax.set_facecolor(bg_c)

        # Adding gridlines to the plot
        ax.grid(ls=":")

        # Making ETr lineplot
        sns.lineplot(data=edata, x=x, y='ETref',
                     color=etr_c, label='Modeled '+etr_l)

        # Making ETc lineplot
        sns.lineplot(data=edata, x=x, y='ETc',
                     color=etc_c, label='Modeled '+etc_l)

        # Making ETcadj lineplot
        sns.lineplot(data=edata, x=x, y='ETcadj',
                     color=etcadj_c, label='Modeled '+etcadj_l)

        # Adding water events if requested
        if water_events:
            sns.scatterplot(data=edata, x=x, y='Rain',
                            color=water_c, marker='+', s=75,
                            label='Rain')
            sns.scatterplot(data=edata, x=x, y='Irrig',
                            color=water_c, marker='x', s=75,
                            label='Irrigation')

        # Adding plot title - either user-defined or default
        if title is None:
            plt.title(plt_title)
        else:
            plt.title(title)

        # Making legend for the plot
        ax.legend(loc='upper left')

        # Saving and Showing the plot (if desired)
        if save is not None:
            plt.savefig(save)
        if show:
            plt.show()
        else:
            plt.close(fig)


class Analyze:
    """A class for numerically analyzing pyfao56 Model output."""
    pass
