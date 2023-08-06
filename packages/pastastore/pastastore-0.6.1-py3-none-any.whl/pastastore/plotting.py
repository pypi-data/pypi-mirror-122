"""This module contains all the plotting methods for PastaStore.

Pastastore comes with a number helpful plotting methods to quickly
visualize timeseries or the locations of the timeseries contained in the
store. Plotting timeseries or data availability is available through the
`plots` attribute of the PastaStore object. Plotting locations of timeseries
or model statistics on maps is available through the `maps` attribute.
For example, if we have a :class:`pastastore.PastaStore` called `pstore`
linking to an existing database, the plot and map methods are available as
follows::

    pstore.plots.oseries()

    ax = pstore.maps.oseries()
    pstore.maps.add_background_map(ax)  # for adding a background map
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pastas as ps
from matplotlib import patheffects
from mpl_toolkits.axes_grid1 import make_axes_locatable


class Plots:
    """Plot class for Pastastore.

    Allows plotting of timeseries and data availability.
    """

    def __init__(self, pstore):
        """Initialize Plots class for Pastastore.

        Parameters
        ----------
        pstore : pastastore.Pastastore
            Pastastore object
        """
        self.pstore = pstore

    def _timeseries(self, libname, names=None, ax=None, split=False,
                    figsize=(10, 5), progressbar=True, **kwargs):
        """Internal method to plot timeseries from pastastore.

        Parameters
        ----------
        libname : str
            name of the library to obtain timeseries from (oseries
            or stresses)
        names : list of str, optional
            list of timeseries names to plot, by default None
        ax : matplotlib.Axes, optional
            pass axes object to plot on existing axes, by default None,
            which creates a new figure
        split : bool, optional
            create a separate subplot for each timeseries, by default False.
            A maximum of 20 timeseries is supported when split=True.
        figsize : tuple, optional
            figure size, by default (10, 5)
        progressbar : bool, optional
            show progressbar when loading timeseries from store,
            by default True

        Returns
        -------
        ax : matplotlib.Axes
            axes handle

        Raises
        ------
        ValueError
            split=True is only supported if there are less than 20 timeseries
            to plot.
        """
        names = self.pstore.conn._parse_names(names, libname)

        if len(names) > 20 and split:
            raise ValueError("More than 20 timeseries leads to too many "
                             "subplots, set split=False.")

        if ax is None:
            if split:
                fig, axes = plt.subplots(len(names), 1, sharex=True,
                                         figsize=figsize)
            else:
                fig, axes = plt.subplots(1, 1, figsize=figsize)
        else:
            axes = ax

        tsdict = self.pstore.conn._get_series(libname, names,
                                              progressbar=progressbar,
                                              squeeze=False)
        for i, (n, ts) in enumerate(tsdict.items()):
            if split and ax is None:
                iax = axes[i]
            elif ax is None:
                iax = axes
            else:
                iax = ax
            iax.plot(ts.index, ts, label=n, **kwargs)
            if split:
                iax.legend(loc='best', fontsize="x-small")

        if not split:
            axes.legend(loc=(0, 1), frameon=False, ncol=7, fontsize="x-small")

        fig.tight_layout()
        return axes

    def oseries(self, names=None, ax=None, split=False,
                figsize=(10, 5), **kwargs):
        """Plot oseries.

        Parameters
        ----------
        names : list of str, optional
            list of oseries names to plot, by default None, which loads
            all oseries from store
        ax : matplotlib.Axes, optional
            pass axes object to plot oseries on existing figure,
            by default None, in which case a new figure is created
        split : bool, optional
            create a separate subplot for each timeseries, by default False.
            A maximum of 20 timeseries is supported when split=True.
        figsize : tuple, optional
            figure size, by default (10, 5)

        Returns
        -------
        ax : matplotlib.Axes
            axes handle
        """
        return self._timeseries("oseries", names=names, ax=ax,
                                split=split, figsize=figsize, **kwargs)

    def stresses(self, names=None, kind=None, ax=None, split=False,
                 figsize=(10, 5), **kwargs):
        """Plot stresses.

        Parameters
        ----------
        names : list of str, optional
            list of oseries names to plot, by default None, which loads
            all oseries from store
        kind : str, optional
            only plot stresses of a certain kind, by default None, which
            includes all stresses
        ax : matplotlib.Axes, optional
            pass axes object to plot oseries on existing figure,
            by default None, in which case a new figure is created
        split : bool, optional
            create a separate subplot for each timeseries, by default False.
            A maximum of 20 timeseries is supported when split=True.
        figsize : tuple, optional
            figure size, by default (10, 5)

        Returns
        -------
        ax : matplotlib.Axes
            axes handle
        """
        names = self.pstore.conn._parse_names(names, "stresses")
        masknames = self.pstore.stresses.index.isin(names)
        stresses = self.pstore.stresses.loc[masknames]

        if kind:
            mask = stresses["kind"] == kind
            names = stresses.loc[mask].index.to_list()

        return self._timeseries("stresses", names=names, ax=ax,
                                split=split, figsize=figsize, **kwargs)

    def data_availability(self, libname, names=None, kind=None,
                          intervals=None,
                          ignore=('second', 'minute', '14 days'),
                          normtype='log', cmap='viridis_r',
                          set_yticks=False, figsize=(10, 8),
                          progressbar=True, **kwargs):
        """Plot the data-availability for multiple timeseries in pastastore.

        Parameters
        ----------
        libname : str
            name of library to get timeseries from (oseries or stresses)
        names : list, optional
            specify names in a list to plot data availability for certain
            timeseries
        kind : str, optional
            if library is stresses, kind can be specified to obtain only
            stresses of a specific kind
        intervals: dict, optional
            A dict with frequencies as keys and number of seconds as values
        ignore : list, optional
            A list with frequencies in intervals to ignore
        normtype : str, optional
            Determines the type of color normalisations, default is 'log'
        cmap : str, optional
            A reference to a matplotlib colormap
        set_yticks : bool, optional
            Set the names of the series as yticks
        figsize : tuple, optional
            The size of the new figure in inches (h,v)
        progressbar : bool
            show progressbar
        kwargs : dict, optional
            Extra arguments are passed to matplotlib.pyplot.subplots()

        Returns
        -------
        ax : matplotlib Axes
            The axes in which the data-availability is plotted
        """
        names = self.pstore.conn._parse_names(names, libname)

        if libname == "stresses":
            masknames = self.pstore.stresses.index.isin(names)
            stresses = self.pstore.stresses.loc[masknames]
            if kind:
                mask = stresses["kind"] == kind
                names = stresses.loc[mask].index.to_list()

        series = self.pstore.conn._get_series(
            libname, names, progressbar=progressbar, squeeze=False).values()

        ax = self._data_availability(series, names=names, intervals=intervals,
                                     ignore=ignore, normtype=normtype,
                                     cmap=cmap, set_yticks=set_yticks,
                                     figsize=figsize, **kwargs)
        return ax

    @staticmethod
    def _data_availability(series, names=None, intervals=None,
                           ignore=('second', 'minute', '14 days'),
                           normtype='log', cmap='viridis_r',
                           set_yticks=False, figsize=(10, 8), **kwargs):
        """Plot the data-availability for a list of timeseries.

        Parameters
        ----------
        libname : list of pandas.Series
            list of series to plot data availability for
        names : list, optional
            specify names of series, default is None in which case names
            will be taken from series themselves.
        kind : str, optional
            if library is stresses, kind can be specified to obtain only
            stresses of a specific kind
        intervals: dict, optional
            A dict with frequencies as keys and number of seconds as values
        ignore : list, optional
            A list with frequencies in intervals to ignore
        normtype : str, optional
            Determines the type of color normalisations, default is 'log'
        cmap : str, optional
            A reference to a matplotlib colormap
        set_yticks : bool, optional
            Set the names of the series as yticks
        figsize : tuple, optional
            The size of the new figure in inches (h,v)
        progressbar : bool
            show progressbar
        kwargs : dict, optional
            Extra arguments are passed to matplotlib.pyplot.subplots()

        Returns
        -------
        ax : matplotlib Axes
            The axes in which the data-availability is plotted
        """
        # a good colormap is cmap='RdYlGn_r' or 'cubehelix'
        f, ax = plt.subplots(figsize=figsize, **kwargs)
        ax.invert_yaxis()
        if intervals is None:
            intervals = {'second': 1,
                         'minute': 60,
                         'hour': 60 * 60,
                         'day': 60 * 60 * 24,
                         'week': 60 * 60 * 24 * 7,
                         '14 days': 60 * 60 * 24 * 14,
                         'month': 60 * 60 * 24 * 31,
                         'quarter': 60 * 60 * 24 * 31 * 4,
                         'year': 60 * 60 * 24 * 366}
            for i in ignore:
                if i in intervals:
                    intervals.pop(i)

        bounds = np.array([intervals[i] for i in intervals])
        bounds = bounds.astype(float) * (10**9)
        labels = intervals.keys()
        if normtype == 'log':
            norm = mpl.colors.LogNorm(vmin=bounds[0], vmax=bounds[-1])
        else:
            norm = mpl.colors.BoundaryNorm(
                boundaries=bounds, ncolors=256)
        cmap = plt.cm.get_cmap(cmap, 256)
        cmap.set_over((1., 1., 1.))

        for i, s in enumerate(series):
            if not s.empty:
                pc = ax.pcolormesh(s.index, [i, i + 1],
                                   [np.diff(s.index).astype(float)],
                                   norm=norm, cmap=cmap,
                                   linewidth=0, rasterized=True)
        # make a colorbar in an ax on the
        # right side, then set the current axes to ax again
        cb = f.colorbar(pc, ax=ax, extend='both')
        cb.set_ticks(bounds)
        cb.ax.set_yticklabels(labels)
        cb.ax.minorticks_off()
        if set_yticks:
            ax.set_yticks(np.arange(0.5, len(series) + 0.5))
            if names is None:
                names = [s.name for s in series]
            ax.set_yticklabels(names)
        else:
            ax.set_ylabel('Timeseries (-)')
        ax.grid()
        f.tight_layout(pad=0.0)
        return ax


class Maps:
    """Map Class for PastaStore.

    Allows plotting locations and model statistics on maps.

    Usage
    -----
    Example usage of the maps methods: :

    >> > ax = pstore.maps.oseries()  # plot oseries locations
    >> > pstore.maps.add_background_map(ax)  # add background map
    """

    def __init__(self, pstore):
        """Initialize Plots class for Pastastore.

        Parameters
        ----------
        pstore: pastastore.Pastastore
            Pastastore object
        """
        self.pstore = pstore

    def stresses(self, kind=None, labels=True, figsize=(10, 8), **kwargs):
        """Plot stresses locations on map.

        Parameters
        ----------
        kind: str, optional
            if passed, only plot stresses of a specific kind, default is None
            which plots all stresses.
        labels: bool, optional
            label models, by default True
        figsize: tuple, optional
            figure size, by default(10, 8)

        Returns
        -------
        ax: matplotlib.Axes
            axes object

        See also
        --------
        self.add_background_map
        """

        if kind is not None:
            mask = self.pstore.stresses["kind"] == kind
            stresses = self.pstore.stresses.loc[mask]
        else:
            stresses = self.pstore.stresses

        mask0 = (stresses["x"] != 0.0) | (stresses["y"] != 0.0)

        ax = self._plotmap_dataframe(stresses.loc[mask0], figsize=figsize,
                                     **kwargs)
        if labels:
            self.add_labels(stresses, ax)

        return ax

    def oseries(self, labels=True, figsize=(10, 8), **kwargs):
        """Plot oseries locations on map.

        Parameters
        ----------
        labels: bool, optional
            label models, by default True
        figsize: tuple, optional
            figure size, by default(10, 8)

        Returns
        -------
        ax: matplotlib.Axes
            axes object

        See also
        --------
        self.add_background_map
        """
        oseries = self.pstore.oseries
        mask0 = (oseries["x"] != 0.0) | (oseries["y"] != 0.0)
        ax = self._plotmap_dataframe(oseries.loc[mask0], figsize=figsize,
                                     **kwargs)
        if labels:
            self.add_labels(oseries, ax)

        return ax

    def models(self, labels=True, figsize=(10, 8), **kwargs):
        """Plot model locations on map.

        Parameters
        ----------
        labels: bool, optional
            label models, by default True
        figsize: tuple, optional
            figure size, by default(10, 8)

        Returns
        -------
        ax: matplotlib.Axes
            axes object

        See also
        --------
        self.add_background_map
        """

        model_oseries = [self.pstore.get_models(m, return_dict=True)[
            "oseries"]["name"] for m in self.pstore.model_names]

        models = self.pstore.oseries.loc[model_oseries]
        models.index = self.pstore.model_names

        # mask out 0.0 coordinates
        mask0 = (models["x"] != 0.0) | (models["y"] != 0.0)
        ax = self._plotmap_dataframe(models.loc[mask0], figsize=figsize,
                                     **kwargs)
        if labels:
            self.add_labels(models, ax)

        return ax

    def modelstat(self, statistic, label=True, cmap="viridis", norm=None,
                  vmin=None, vmax=None, figsize=(10, 8), **kwargs):
        """Plot model statistic on map.

        Parameters
        ----------
        statistic: str
            name of the statistic, e.g. "evp" or "aic"
        label: bool, optional
            label points, by default True
        cmap: str or colormap, optional
            (name of) the colormap, by default "viridis"
        norm: norm, optional
            normalization for colorbar, by default None
        vmin: float, optional
            vmin for colorbar, by default None
        vmax: float, optional
            vmax for colorbar, by default None
        figsize: tuple, optional
            figuresize, by default(10, 8)

        Returns
        -------
        ax: matplotlib.Axes
            axes object

        See also
        --------
        self.add_background_map
        """
        statsdf = self.pstore.get_statistics([statistic],
                                             progressbar=False).to_frame()

        statsdf["oseries"] = [self.pstore.get_models(m, return_dict=True)[
            "oseries"]["name"] for m in statsdf.index]
        statsdf = statsdf.reset_index().set_index("oseries")
        df = statsdf.join(self.pstore.oseries, how="left")

        scatter_kwargs = {
            "cmap": cmap,
            "norm": norm,
            "vmin": vmin,
            "vmax": vmax,
            "edgecolors": "w",
            "linewidths": 0.7
        }

        scatter_kwargs.update(kwargs)

        ax = self._plotmap_dataframe(df,
                                     column=statistic,
                                     figsize=figsize,
                                     **scatter_kwargs)
        if label:
            df.set_index("index", inplace=True)
            self.add_labels(df, ax)
        return ax

    @staticmethod
    def _plotmap_dataframe(df, x="x", y="y", column=None, ax=None,
                           figsize=(10, 8), **kwargs):
        """Internal method for plotting dataframe with point locations.

        Can be called directly for more control over plot characteristics.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing coordinates and data to plot, with
            index providing names for each location
        x : str, optional
            name of the column with x - coordinate data, by default "x"
        y : str, optional
            name of the column with y - coordinate data, by default "y"
        column : str, optional
            name of the column containing data used for determining the
            color of each point, by default None (all one color)
        ax : matplotlib Axes
            axes handle to plot dataframe, optional, default is None
            which creates a new figure
        figsize : tuple, optional
            figure size, by default(10, 8)
        **kwargs :
            dictionary containing keyword arguments for ax.scatter,
            by default None

        Returns
        -------
        ax : matplotlib.Axes
            axes object
        """

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        # set default size and marker if not passed
        if kwargs:
            s = kwargs.pop("s", 70)
            marker = kwargs.pop("marker", "o")
        else:
            s = 70
            marker = "o"
            kwargs = {}

        # if column is passed for coloring pts
        if column:
            c = df[column]
            if "cmap" not in kwargs:
                kwargs["cmap"] = "viridis"
        else:
            c = None

        sc = ax.scatter(df[x], df[y], marker=marker, s=s, c=c, **kwargs)
        # add colorbar
        if column:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.05)
            cbar = fig.colorbar(sc, ax=ax, cax=cax)
            cbar.set_label(column)

        # set axes properties
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        for label in ax.get_yticklabels():
            label.set_rotation(90)
            label.set_verticalalignment("center")

        fig.tight_layout()

        return ax

    def model(self, ml, label=True,
              metadata_source="model", offset=0.0):
        """Plot oseries and stresses from one model on a map.

        Parameters
        ----------
        ml: str or pastas.Model
            pastas model or name of pastas model to plot on map
        label: bool, optional, default is True
            add labels to points on map
        metadata_source: str, optional
            whether to obtain metadata from model Timeseries or from
            metadata in pastastore("store"), default is "model"
        offset : float, optional
            add offset to current extent of model timeseries, useful
            for zooming out around models

        Returns
        -------
        ax: axes object
            axis handle of the resulting figure

        See also
        --------
        self.add_background_map
        """
        if isinstance(ml, str):
            ml = self.pstore.get_models(ml)
        elif not isinstance(ml, ps.Model):
            raise TypeError("Pass model name as string or pastas.Model!")

        stresses = pd.DataFrame(columns=["x", "y", "stressmodel", "color"])
        count = 0
        for name, sm in ml.stressmodels.items():
            for istress in sm.stress:

                if metadata_source == "model":
                    xi = istress.metadata["x"]
                    yi = istress.metadata["y"]
                elif metadata_source == "store":
                    imeta = self.pstore.get_metadata(
                        "stresses", istress.name, as_frame=False)
                    xi = imeta.pop("x", np.nan)
                    yi = imeta.pop("y", np.nan)
                else:
                    raise ValueError("metadata_source must be either "
                                     "'model' or 'store'!")
                if np.isnan(xi) or np.isnan(yi):
                    print(f"No x,y-data for {istress.name}!")
                    continue
                if xi == 0.0 or yi == 0.0:
                    print(f"x,y-data is 0.0 for {istress.name}, not plotting!")
                    continue

                stresses.loc[istress.name, :] = (
                    xi, yi, name, f"C{count%10}")
            count += 1

        # create figure
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

        # add oseries
        osize = 50
        oserieslabel = ml.oseries.name

        if metadata_source == "model":
            xm = float(ml.oseries.metadata["x"])
            ym = float(ml.oseries.metadata["y"])
        elif metadata_source == "store":
            ometa = self.pstore.get_metadata(
                "oseries", ml.oseries.name, as_frame=False)
            xm = float(ometa.pop("x", np.nan))
            ym = float(ometa.pop("y", np.nan))
        else:
            raise ValueError("metadata_source must be either "
                             "'model' or 'store'!")

        po = ax.scatter(xm, ym, s=osize, marker="o",
                        label=oserieslabel, color="k")
        legend_list = [po]

        # add stresses
        ax.scatter(stresses["x"], stresses["y"], s=50, c=stresses.color,
                   marker="o", edgecolors="k", linewidths=0.75)

        # label oseries
        if label:
            stroke = [patheffects.withStroke(linewidth=3, foreground="w")]
            txt = ax.annotate(text=oserieslabel, xy=(xm, ym), fontsize=8,
                              textcoords="offset points", xytext=(10, 10))
            txt.set_path_effects(stroke)

        # get legend entries for stressmodels
        uniques = stresses.loc[:, ["stressmodel", "color"]
                               ].drop_duplicates(keep="first")
        for name, row in uniques.iterrows():
            h, = ax.plot([], [], marker="o", label=row.stressmodel, ls="",
                         mec="k", ms=10, color=row.color)
            legend_list.append(h)

        # add legend
        ax.legend(legend_list, [i.get_label()
                                for i in legend_list], loc="best")

        # set axes properties
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        for label in ax.get_yticklabels():
            label.set_rotation(90)
            label.set_verticalalignment("center")

        if offset > 0.0:
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            ax.set_xlim(xmin - offset, xmax + offset)
            ax.set_ylim(ymin - offset, ymax + offset)

        # label stresses
        if label:
            for name, row in stresses.iterrows():
                namestr = str(name)
                namestr += f"\n({row.stressmodel})"
                txt = ax.annotate(text=namestr, xy=(row.x, row.y), fontsize=8,
                                  textcoords="offset points", xytext=(10, 10))
                txt.set_path_effects(stroke)

        fig.tight_layout()

        return ax

    @staticmethod
    def _list_contextily_providers():
        """List contextily providers.

        Taken from contextily notebooks.

        Returns
        -------
        providers : dict
            dictionary containing all providers. See keys for names
            that can be passed as map_provider arguments.
        """
        import contextily as ctx
        providers = {}

        def get_providers(provider):
            if "url" in provider:
                providers[provider['name']] = provider
            else:
                for prov in provider.values():
                    get_providers(prov)
        get_providers(ctx.providers)
        return providers

    @staticmethod
    def add_background_map(ax, proj="epsg:28992",
                           map_provider="OpenStreetMap.Mapnik",
                           **kwargs):
        """Add background map to axes using contextily.

        Parameters
        ----------
        ax: matplotlib.Axes
            axes to add background map to
        map_provider: str, optional
            name of map provider, see `contextily.providers` for options.
            Default is 'OpenStreetMap.Mapnik'
        proj: pyproj.Proj or str, optional
            projection for background map, default is 'epsg:28992'
            (RD Amersfoort, a projection for the Netherlands)
        """
        import contextily as ctx

        if isinstance(proj, str):
            import pyproj
            proj = pyproj.Proj(proj)

        providers = Maps._list_contextily_providers()
        ctx.add_basemap(ax, source=providers[map_provider], crs=proj.srs,
                        **kwargs)

    @staticmethod
    def add_labels(df, ax, **kwargs):
        """Add labels to points on plot.

        Uses dataframe index to label points.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame containing x, y - data. Index is used as label
        ax: matplotlib.Axes
            axes object to label points on
        **kwargs:
            keyword arguments to ax.annotate
        """

        stroke = [patheffects.withStroke(linewidth=3, foreground="w")]

        fontsize = kwargs.pop("fontsize", 10)
        textcoords = kwargs.pop("textcoords", "offset points")
        xytext = kwargs.pop("xytext", (10, 10))

        for name, row in df.iterrows():
            namestr = str(name)
            txt = ax.annotate(text=namestr,
                              xy=(row["x"], row["y"]),
                              fontsize=fontsize,
                              textcoords=textcoords,
                              xytext=xytext)
            txt.set_path_effects(stroke)
