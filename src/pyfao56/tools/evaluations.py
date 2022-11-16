"""
########################################################################
The evaluations.py module contains the Evaluations class,
which provide tools for visualizing pyfao56 Model output.

The evaluations.py module contains the following:
    Evaluations - A class for evaluating pyfao56 Model output

11/9/2022 Initial Python functions developed by Josh Brekel, USDA-ARS
########################################################################
"""

import matplotlib.pyplot as plt
import seaborn as sns

class Evaluations:
    """A class for evaluating pyfao56 Model output.

    Attributes
    ----------
    mdl : pyfao56 Model class
        Provides data to evaluate.
    edata : Dataframe
        All of the data to be evaluated.
    swd : pyfao56-Tools SoilWaterDeficit class, optional
        Provides observed soil water deficit data to evaluate
        (default = None)

    Methods
    -------
    plot_Dr(drmax=False, raw=False, water_events=False, obs=False,
            ks=False, title=None, save=None, show=True)
        Create a plot of Modeled soil water depletion
    plot_ET(rET=True, etc=True, etcadj=True, water_events=False,
            title=None, save=None, show=True)
        Create a plot of Modeled evapotranspiration
    """

    def __init__(self, mdl, swd=None):
        """Initialize the Evaluations class attributes.

        Parameters
        ----------
        mdl : pyfao56 Model object
            Provides the modeled data to be evaluated
        swd : pyfao56-Tools SoilWaterDeficit object, optional
            Provides observed soil water deficit data to evaluate
            (default = None)
        """

        self.mdl = mdl
        self.swd = swd
        # Getting rid of duplicate columns from mdl.odata
        edata = mdl.odata.loc[:, ~mdl.odata.columns.duplicated()].copy()
        if self.swd is not None:
            edata = edata.merge(self.swd.rzdata[['SWDr', 'SWDrmax']],
                                right_index=True,
                                left_index=True,
                                how='outer')
        self.edata = edata

    def plot_Dr(self, drmax=False, raw=False, water_events=False,
                obs=False, ks=False, title=None, save=None, show=True):
        """Plot soil water depletion (Dr), with water amount (mm/day) on
           the y-axis, and day of year (DOY) on the x-axis.

        Parameters
        ----------
        drmax : boolean, optional
            If False, max root depth depletion (Drmax) is not plotted;
            if True, figure includes a line plot of Drmax
            (default = False)
        raw : boolean, optional
            If False, Readily Available Water (RAW) is not plotted; if
            True, figure includes a line plot of RAW
            (default = False)
        water_events : boolean, optional
            If False, irrigation and rainfall are not plotted; if True,
            figure includes a scatter plot of irrigation and rainfall
            (default = False)
        obs : boolean, optional
            If False, observed soil water depletion values are not
            plotted; if True, figure includes a scatter plot of observed
            soil water depletion.
            (default = False)
        ks : boolean, optional
            If False, the stress coefficient (Ks) is not plotted; if
            True, figure includes a Ks line plot at the top.
            (default = False)
        title : str, optional
            If None, the figure title is "pyfao56 Soil Water Depletion".
            Change the title by providing a string here.
            (default = None)
        save : str, optional
            If None, the figure is not saved. To save, provide a string
            of the filepath where the figure should be saved.
            (default = None)
        show : boolean, optional
            If True, the plot is displayed before the method moves on;
            if False, the plot is not displayed.
            (default = True)
        """

        # Creating variables for info that is used or changed often
        edata     = self.edata
        x         = 'DOY'
        # Labels
        plt_title = 'pyfao56 Soil Water Depletion'
        x_l       = 'Day of Year (DOY)'
        y_l       = 'Water Amount (mm/day)'
        dr_l      = 'Root Zone Depletion'
        drmax_l   = 'Max Root Depth Depletion'
        raw_l     = 'Readily Available Water (RAW)'
        ks_l      = 'pyfao56 Ks'
        f_size    = 'medium'
        frame     = False
        # Colors
        bg_c      = 'whitesmoke'
        dr_c      = 'darkcyan'
        drmax_c   = 'darkturquoise'
        raw_c     = 'mediumorchid'
        water_c   = 'navy'
        ks_c      = 'lightsalmon'
        
        # Checking for Ks before making axes
        if ks:
            # Creating Figure
            fig, (ax2, ax) = plt.subplots(2, sharex=True, gridspec_kw=
                                            {'height_ratios': [1, 8]})
            fig.set_figheight(8)
            fig.set_figwidth(16)

            # Main plot:
            # Setting axis labels:
            ax.set(ylabel=y_l)
            plt.xlabel(x_l)
            # Setting axis ticks:
            # x axis:
            mykey = self.mdl.startDate.strftime('%Y-%j')
            start_doy = int(self.edata['DOY'].loc[mykey])
            x_tick_start = -1 * (start_doy % 5)
            ax.set_xticks(range(x_tick_start, start_doy, 5))
            # y axis:
            swd_max = round(self.edata['Dr'].max())
            swd_max += (-(swd_max % 10) + 10) + 6
            ax.set_ylim(1, swd_max)
            ax.set_yticks(range(5, swd_max, 5))
            # Changing the background color of the plot
            ax.set_facecolor(bg_c)
            # Adding gridlines to the plot
            ax.grid(ls=":")

            # Ks Plot
            # Setting y-axis ticks
            ax2.set_ylim(0, 1.1)
            ax2.set_yticks([x * 0.5 for x in range(1, 3)])
            # Creating Grid
            ax2.grid(ls=":")
            # Changing the background color of the plot
            ax2.set_facecolor(bg_c)
            # Adding Ks lineplot
            sns.lineplot(data=edata, x=x, y='Ks',
                         color=ks_c, label=ks_l, ax=ax2)
            # Adding legend
            ax2.legend(fontsize=f_size, loc='lower left',
                       frameon=frame)
            # Removing space between the plots
            fig.subplots_adjust(hspace=0)
        else:
            # Creating Figure
            fig, ax = plt.subplots()
            fig.set_figheight(8)
            fig.set_figwidth(16)

            # Main plot:
            # Setting axis labels:
            ax.set(ylabel=y_l)
            plt.xlabel(x_l)
            # Setting axis ticks:
            # x axis:
            mykey = self.mdl.startDate.strftime('%Y-%j')
            start_doy = int(self.edata['DOY'].loc[mykey])
            x_tick_start = -1 * (start_doy % 5)
            ax.set_xticks(range(x_tick_start, start_doy, 5))
            # y axis:
            swd_max = round(self.edata['Dr'].max())
            swd_max += (-(swd_max % 10) + 10) + 6
            ax.set_ylim(1, swd_max)
            ax.set_yticks(range(5, swd_max, 5))
            # Changing the background color of the plot
            ax.set_facecolor(bg_c)
            # Adding gridlines to the plot
            ax.grid(ls=":")

        # Making Dr lineplot
        sns.lineplot(data=edata, x=x, y='Dr',
                     color=dr_c, label=dr_l, ax=ax)

        # Making Drmax lineplot if requested
        if drmax:
            sns.lineplot(data=edata, x=x, y='Drmax',
                         color=drmax_c, label=drmax_l, ax=ax)

        # Adding observed SWD if requested:
        if obs:
            if self.swd.rzdata is None:
                print('To plot observed data, please provide a '
                      'SoilWaterDeficit class rzdata attribute.')
            else:
                sns.scatterplot(data=edata, x=x, y='SWDr',
                                color=dr_c, marker='s', s=40,
                                edgecolor='darkslategray',
                                label='Observed '+dr_l, ax=ax)
                if drmax:
                    sns.scatterplot(data=edata, x=x, y='SWDrmax',
                                    color=drmax_c, marker='s', s=40,
                                    edgecolor='teal',
                                    label='Observed '+drmax_l, ax=ax)

        # Adding RAW lineplot if requested
        if raw:
            sns.lineplot(data=edata, x=x, y='RAW',
                         color=raw_c, label=raw_l, ax=ax)

        # Adding water events if requested
        if water_events:
            sns.scatterplot(data=edata, x=x, y='Rain',
                            color=water_c, marker='+', s=60,
                            label='Rain', ax=ax)
            sns.scatterplot(data=edata, x=x, y='Irrig',
                            color=water_c, marker='x', s=60,
                            label='Irrigation', ax=ax)

        # Adding plot title - either user-defined or default
        if title is None:
            plt.suptitle(plt_title)
        else:
            plt.suptitle(title)

        # Making legend for the plot
        ax.legend(fontsize=f_size, loc='upper left', frameon=frame)
        # Saving and Showing the plot (if desired)
        if save is not None:
            plt.savefig(save)
        if show:
            plt.show()
        else:
            plt.close(fig)

    def plot_ET(self, rET=True, etc=True, etcadj=True,
                water_events=False, title=None, save=None, show=True):
        """Plot evapotranspiration (ET), with water amount (mm/day) on
           the y-axis, and day of year (DOY) on the x-axis.

        Parameters
        ----------
        rET : boolean, optional
            If True, the figure includes a lineplot for reference ET; if
            False, the figure does not include reference ET
            (default = True)
        etc : boolean, optional
            If True, the figure includes a lineplot for crop ET; if
            False, the figure does not include crop ET
            (default = True)
        etcadj : boolean, optional
            If True, the figure includes a lineplot for adjusted crop
            ET; if False, the figure does not include adjusted crop ET
            (default = True)
        water_events : boolean, optional
            If False, irrigation and rainfall are not plotted; if True,
            figure includes a scatter plot of irrigation and rainfall
            (default = False)
        title : str, optional
            If None, the figure title is "pyfao56 Soil Water Depletion".
            Change the title by providing a string here.
            (default = None)
        save : str, optional
            If None, the figure is not saved. To save, provide a string
            of the filepath where the figure should be saved.
            (default = None)
        show : boolean, optional
            If True, the plot is displayed before the method moves on;
            if False, the plot is not displayed.
            (default = True)
            """

        # Creating variables for info that is used or changed often
        edata     = self.edata
        x         = 'DOY'
        # Labels
        plt_title = 'pyfao56 Evapotranspiration (ET)'
        x_l       = 'Day of Year (DOY)'
        y_l       = 'Water Amount (mm/day)'
        if self.mdl.wth.rfcrp == 'S':
            rET_l = 'ETo'
        elif self.mdl.wth.rfcrp == 'T':
            rET_l = 'ETr'
        etc_l     = 'ETc'
        etcadj_l  = 'ETc_adj'
        f_size    = 'medium'
        frame     = False
        # Colors
        bg_c      = 'whitesmoke'
        rET_c     = 'darkred'
        etc_c     = 'deepskyblue'
        etcadj_c  = 'navy'
        water_c   = 'navy'

        # Creating figure:
        fig, ax = plt.subplots()
        fig.set_figheight(8)
        fig.set_figwidth(16)

        # Setting axis labels:
        ax.set(xlabel=x_l, ylabel=y_l)

        # Setting axis ticks:
        # x axis:
        mykey = self.mdl.startDate.strftime('%Y-%j')
        start_doy = int(self.edata['DOY'].loc[mykey])
        x_tick_start = -1 * (start_doy % 5)
        ax.set_xticks(range(x_tick_start, start_doy, 5))
        # y axis:
        rET_max = round(self.edata['ETref'].max())
        rET_max += -(rET_max % 2) + 3
        ax.set_ylim(0, rET_max)
        ax.set_yticks(range(0, rET_max, 2))

        # Changing the background color of the plot
        ax.set_facecolor(bg_c)

        # Adding gridlines to the plot
        ax.grid(ls=":")

        # Making ETr lineplot if requested
        if rET:
            sns.lineplot(data=edata, x=x, y='ETref',
                         color=rET_c, label=rET_l)

        # Making ETc lineplot if requested
        if etc:
            sns.lineplot(data=edata, x=x, y='ETc',
                         color=etc_c, label=etc_l)

        # Making ETcadj lineplot if requested
        if etcadj:
            sns.lineplot(data=edata, x=x, y='ETcadj', linestyle='-.',
                         color=etcadj_c, label=etcadj_l)

        # Adding water events if requested
        if water_events:
            water_max = max([round(self.edata['Rain'].max()),
                             round(self.edata['Irrig'].max())])
            water_max += water_max % 5
            ax.set_ylim(1, water_max)
            ax.set_yticks(range(1, water_max, 2))
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
        ax.legend(loc='upper left', fontsize=f_size, frameon=frame)

        # Saving and Showing the plot (if desired)
        if save is not None:
            plt.savefig(save)
        if show:
            plt.show()
        else:
            plt.close(fig)
