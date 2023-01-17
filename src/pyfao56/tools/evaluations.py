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
            edata = edata.merge(self.swd.rzdata[['SWDr', 'SWDrmax', 'ObsKs']],
                                right_index=True,
                                left_index=True,
                                how='outer')
        self.edata = edata

    def plot_Dr(self, drmax=False, raw=False, water_events=False,
                obs=False, ks=False, dp=False, title=None,
                save=None, show=True):
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
        dp : boolean, optional
            If False, then deep percolation is not plotted; if True,
            figure includes a DP scatter plot below main plot.
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
        ks_l      = 'Ks'
        dp_l      = 'Deep Percolation'
        f_size    = 'medium'
        frame     = False
        # Colors
        bg_c      = 'whitesmoke'
        dr_c      = 'darkcyan'
        drmax_c   = 'darkturquoise'
        raw_c     = 'mediumorchid'
        water_c   = 'navy'
        ks_c      = 'lightsalmon'
        dp_c      = 'crimson'

        # Creating inner functions for making specific axes / figures
        def main_plot(ax):
            # Setting axis labels:
            ax.set(ylabel=y_l)
            plt.xlabel(x_l)
            # Setting axis ticks:
            # x axis:
            mykey = self.mdl.startDate.strftime('%Y-%j')
            start_doy = int(self.edata['DOY'].loc[mykey])
            x_tick_start = -(start_doy % 5)
            ax.set_xticks(range(x_tick_start, 365, 5))
            # y axis:
            swd_max = round(self.edata['Dr'].max())
            swd_max += (-(swd_max % 10) + 10) + 6
            ax.set_ylim(1.05, swd_max)
            ax.set_yticks(range(5, swd_max, 5))
            return ax

        def ks_plot(ax):
            # Setting y-axis ticks
            ax.set_ylim(0, 1.1)
            ax.set_yticks([x * 0.5 for x in range(1, 3)])
            # Adding Ks lineplot
            edata.plot(x=x, y='Ks', color=ks_c, label='pyfao56 ' + ks_l, ax=ax2)
            # Creating Grid
            ax.grid(ls=":")
            # Changing the background color of the plot
            ax.set_facecolor(bg_c)
            if obs:
                if self.swd.rzdata is None:
                    print('To plot observed data, please provide a '
                          'SoilWaterDeficit class rzdata attribute.')
                else:
                    ax.scatter(x, 'ObsKs', data=edata,
                                color=ks_c, marker='s', s=40,
                                edgecolor='salmon',
                                label='Observed ' + ks_l)
            # Adding legend
            ax.legend(fontsize=f_size, loc='lower left',
                       frameon=frame)

        def dp_plot(ax, dp_max):
            # Specifying DP parameters
            if dp_max > 0.0:
                ax.set_ylim(0, dp_max + 10)
            else:
                ax.set_ylim(1, dp_max + 10)
            ax.invert_yaxis()

            # DP plot
            # Creating Grid
            ax.grid(ls=":")
            # Changing the background color of the plot
            ax.set_facecolor(bg_c)
            ax.scatter(x, 'DP', data=edata, c=dp_c, marker='_', s=150, label=dp_l, linewidth=2)
            # Adding Legend
            ax.legend(fontsize=f_size, loc='upper left',
                       frameon=frame)
            return ax

        # Checking for DeepPerc before making axes
        if dp:
            # Checking for Ks before making axes
            if ks:
                # Check to see if DP is worth graphing
                dp_max = round(self.edata['DP'].max())
                if dp_max > 0.0:
                    # Creating Figure
                    fig, (ax2, ax, ax3) = plt.subplots(3, sharex=True,
                                                       gridspec_kw={'height_ratios': [4, 32, 6]})
                    ax3.yaxis.set_major_locator(plt.MaxNLocator(5))
                else:
                    # Creating Figure
                    fig, (ax2, ax, ax3) = plt.subplots(3, sharex=True,
                                                       gridspec_kw={'height_ratios': [2, 16, 1]})
                    ax3.yaxis.set_major_locator(plt.MaxNLocator(2))

                # # Ks Plot
                ks_plot(ax2)

            else:
                # Check to see if DP is worth graphing
                dp_max = round(self.edata['DP'].max())
                if dp_max > 0.0:
                    # Creating Figure
                    fig, (ax, ax3) = plt.subplots(2, sharex=True,
                                                     gridspec_kw={'height_ratios': [16, 3]})
                    ax3.yaxis.set_major_locator(plt.MaxNLocator(5))
                else:
                    # Creating Figure
                    fig, (ax, ax3) = plt.subplots(2, sharex=True,
                                                     gridspec_kw={'height_ratios': [16, 1]})
                    ax3.yaxis.set_major_locator(plt.MaxNLocator(2))

            # Removing space between the plots
            fig.subplots_adjust(hspace=0)

            # DP plot
            dp_plot(ax3, dp_max)

        else:
            # Checking for Ks before making axes
            if ks:
                # Creating Figure
                fig, (ax2, ax) = plt.subplots(2, sharex=True, gridspec_kw={'height_ratios': [1, 8]})

                # # Ks Plot
                ks_plot(ax2)

                # Removing space between the plots
                fig.subplots_adjust(hspace=0)

            else:
                # Creating Figure
                fig, ax = plt.subplots()

        # Changing the size of the figure
        fig.set_figheight(8)
        fig.set_figwidth(16)

        # Main plot:
        main_plot(ax)

        # Making Dr lineplot
        edata.plot(x=x, y='Dr', color=dr_c, label=dr_l, ax=ax)

        # Making Drmax lineplot if requested
        if drmax:
            edata.plot(x=x, y='Drmax', color=drmax_c, label=drmax_l, ax=ax)

        # Adding observed SWD if requested:
        if obs:
            if self.swd.rzdata is None:
                print('To plot observed data, please provide a '
                      'SoilWaterDeficit class rzdata attribute.')
            else:
                ax.scatter(x, 'SWDr', data=edata,
                           color=dr_c, marker='s', s=40,
                           edgecolor='darkslategray',
                           label='Observed '+dr_l)
                if drmax:
                    ax.scatter(x, 'SWDrmax', data=edata,
                               color=drmax_c, marker='s', s=40,
                               edgecolor='teal',
                               label='Observed '+drmax_l)

        # Adding RAW lineplot if requested
        if raw:
            edata.plot(x=x, y='RAW', color=raw_c, label=raw_l, ax=ax)

        # Adding water events if requested
        if water_events:
            ax.scatter(x, 'Rain', data=edata,
                       color=water_c, marker='+', s=55, linewidth=0.70,
                       label='Rain')
            ax.scatter(x, 'Irrig', data=edata,
                       color=water_c, marker='x', s=55, linewidth=0.70,
                       label='Irrigation')

        # Changing the background color of the plot
        ax.set_facecolor(bg_c)

        # Adding gridlines to the plot
        ax.grid(ls=":")
        # Making legend for the plot
        ax.legend(fontsize=f_size, loc='upper left', frameon=frame)

        # Adding plot title - either user-defined or default
        if title is None:
            plt.suptitle(plt_title)
        else:
            plt.suptitle(title)

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
        x_tick_start = -(start_doy % 5)
        ax.set_xticks(range(x_tick_start, 365, 5))
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
