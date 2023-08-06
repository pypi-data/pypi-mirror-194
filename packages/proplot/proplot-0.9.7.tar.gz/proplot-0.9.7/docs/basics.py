# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_basics:
#
# The basics
# ==========


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_intro:
#
# Creating figures
# ----------------
#
# Proplot works by subclassing three fundamental matplotlib objects:
# `proplot.figure.Figure` replaces `matplotlib.figure.Figure`, `proplot.axes.Axes`
# and `proplot.axes.PlotAxes` replace `matplotlib.axes.Axes`, and
# `proplot.gridspec.GridSpec` replaces `matplotlib.gridspec.GridSpec`
# (for more on gridspecs, see this `matplotlib tutorial
# <https://matplotlib.org/stable/tutorials/intermediate/gridspec.html>`__).
#
# To make plots with these classes, you must start with the `~proplot.ui.figure` or
# `~proplot.ui.subplots` commands. These are modeled after the `~matplotlib.pyplot`
# commands of the same name. As in `~matplotlib.pyplot`, `~proplot.ui.subplots`
# creates a figure and a grid of subplots all at once, while `~proplot.ui.figure`
# creates an empty figure that can be subsequently filled with subplots.
# A minimal example with just one subplot is shown below.
#
# %% [raw] raw_mimetype="text/restructuredtext"
# .. note::
#
#    Proplot changes the default :rcraw:`figure.facecolor` so that the figure
#    backgrounds shown by the `matplotlib backend
#    <https://matplotlib.org/faq/usage_faq#what-is-a-backend>`__ are light gray (the
#    :rcraw:`savefig.facecolor` applied to saved figures is still white). This can be
#    helpful when designing figures. Proplot also controls the appearence of figures
#    in Jupyter notebooks using the new :rcraw:`inlinefmt` setting, which is passed
#    to `~proplot.config.config_inline_backend` on import. This imposes a
#    higher-quality default `"inline" format
#    <https://ipython.readthedocs.io/en/stable/interactive/plotting.html>`__
#    and disables the backend-specific settings ``InlineBackend.rc`` and
#    ``InlineBackend.print_figure_kwargs``, ensuring that the figures you save
#    look like the figures displayed by the backend.
#
#    Proplot also changes the default :rcraw:`savefig.format`
#    from PNG to PDF for the following reasons:
#
#        #. Vector graphic formats are infinitely scalable.
#        #. Vector graphic formats are preferred by academic journals.
#        #. Nearly all academic journals accept figures in the PDF format alongside
#           the `EPS <https://en.wikipedia.org/wiki/Encapsulated_PostScript>`__ format.
#        #. The EPS format is outdated and does not support transparent graphic
#           elements.
#
#    In case you *do* need a raster format like PNG, proplot increases the
#    default :rcraw:`savefig.dpi` to 1000 dots per inch, which is
#    `recommended <https://www.pnas.org/page/authors/format>`__ by most journals
#    as the minimum resolution for rasterized figures containing lines and text.
#    See the :ref:`configuration section <ug_proplotrc>` for how to change
#    these settings.
#

# %%
# Single subplot
import numpy as np
import proplot as pplt
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)
fig = pplt.figure(suptitle='Single subplot')
ax = fig.subplot(xlabel='x axis', ylabel='y axis')
ax.plot(data, lw=2)


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_subplot:
#
# Creating subplots
# -----------------
#
# Similar to matplotlib, subplots can be added to figures one-by-one
# or all at once. Each subplot will be an instance of
# `proplot.axes.Axes`. To add subplots all at once, use
# `proplot.figure.Figure.add_subplots` (or its shorthand,
# `proplot.figure.Figure.subplots`). Note that under the hood, `~proplot.ui.subplots`
# simply calls `~proplot.ui.figure` followed by `proplot.figure.Figure.add_subplots`.
#
# * With no arguments, `~proplot.figure.Figure.add_subplots` returns a subplot
#   generated from a 1-row, 1-column `~proplot.gridspec.GridSpec`.
# * With `ncols` or `nrows`, `~proplot.figure.Figure.add_subplots` returns a
#   simple grid of subplots from a `~proplot.gridspec.GridSpec` with
#   matching geometry in either row-major or column-major `order`.
# * With `array`, `~proplot.figure.Figure.add_subplots` returns an arbitrarily
#   complex grid of subplots from a `~proplot.gridspec.GridSpec` with matching
#   geometry. Here `array` is a 2D array representing a "picture" of the subplot
#   layout, where each unique integer indicates a `~matplotlib.gridspec.GridSpec` slot
#   that is occupied by the corresponding subplot and ``0`` indicates an empty space.
#
# To add subplots one-by-one, use the `proplot.figure.Figure.add_subplot`
# command (or its shorthand `proplot.figure.Figure.subplot`).
#
# * With no arguments, `~proplot.figure.Figure.add_subplot` returns a subplot
#   generated from a 1-row, 1-column `~proplot.gridspec.GridSpec`.
# * With integer arguments, `~proplot.figure.Figure.add_subplot` returns
#   a subplot matching the corresponding `~proplot.gridspec.GridSpec` geometry,
#   as in matplotlib. Note that unlike matplotlib, the geometry must be compatible
#   with the geometry implied by previous `~proplot.figure.Figure.add_subplot` calls.
# * With a `~matplotlib.gridspec.SubplotSpec` generated by indexing a
#   `proplot.gridspec.GridSpec`, `~proplot.figure.Figure.add_subplot` returns a
#   subplot at the corresponding location. Note that unlike matplotlib, only
#   one `~proplot.figure.Figure.gridspec` instance can be used with each figure.
#
# As in matplotlib, to save figures, use `~matplotlib.figure.Figure.savefig` (or its
# shorthand `proplot.figure.Figure.save`). User paths in the filename are expanded
# with `os.path.expanduser`. In the following examples, we add subplots to figures
# with a variety of methods and then save the results to the home directory.
#
# .. warning::
#
#    Proplot employs :ref:`automatic axis sharing <ug_share>` by default. This lets
#    subplots in the same row or column share the same axis limits, scales, ticks,
#    and labels. This is often convenient, but may be annoying for some users. To
#    keep this feature turned off, simply :ref:`change the default settings <ug_rc>`
#    with e.g. ``pplt.rc.update(share=False, span=False)``. See the
#    :ref:`axis sharing section <ug_share>` for details.

# %%
# Simple subplot grid
import numpy as np
import proplot as pplt
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)
fig = pplt.figure()
ax = fig.subplot(121)
ax.plot(data, lw=2)
ax = fig.subplot(122)
fig.format(
    suptitle='Simple subplot grid', title='Title',
    xlabel='x axis', ylabel='y axis'
)
fig.save('~/example1.png')


# %%
# Complex grid
import numpy as np
import proplot as pplt
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)
array = [  # the "picture" (0 == nothing, 1 == subplot A, 2 == subplot B, etc.)
    [1, 1, 2, 2],
    [0, 3, 3, 0],
]
fig = pplt.figure(refwidth=1.8)
axs = fig.subplots(array)
axs.format(
    abc=True, abcloc='ul', suptitle='Complex subplot grid',
    xlabel='xlabel', ylabel='ylabel'
)
axs[2].plot(data, lw=2)
fig.save('~/example2.png')


# %%
# Really complex grid
import numpy as np
import proplot as pplt
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)
array = [  # the "picture" (1 == subplot A, 2 == subplot B, etc.)
    [1, 1, 2],
    [1, 1, 6],
    [3, 4, 4],
    [3, 5, 5],
]
fig, axs = pplt.subplots(array, figwidth=5, span=False)
axs.format(
    suptitle='Really complex subplot grid',
    xlabel='xlabel', ylabel='ylabel', abc=True
)
axs[0].plot(data, lw=2)
fig.save('~/example3.png')


# %%
# Using a GridSpec
import numpy as np
import proplot as pplt
state = np.random.RandomState(51423)
data = 2 * (state.rand(100, 5) - 0.5).cumsum(axis=0)
gs = pplt.GridSpec(nrows=2, ncols=2, pad=1)
fig = pplt.figure(span=False, refwidth=2)
ax = fig.subplot(gs[:, 0])
ax.plot(data, lw=2)
ax = fig.subplot(gs[0, 1])
ax = fig.subplot(gs[1, 1])
fig.format(
    suptitle='Subplot grid with a GridSpec',
    xlabel='xlabel', ylabel='ylabel', abc=True
)
fig.save('~/example4.png')


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_plots:
#
# Plotting stuff
# --------------
#
# Matplotlib has
# `two different interfaces <https://matplotlib.org/stable/api/index.html>`__:
# an object-oriented interface and a MATLAB-style `~matplotlib.pyplot` interface
# (which uses the object-oriented interface internally). Plotting with proplot is just
# like plotting with matplotlib's *object-oriented* interface. The added plotting
# features are implemented with an intermediate `proplot.axes.PlotAxes` subclass.
# This subclass adds several new plotting commands and adds new features to existing
# commands. These additions do not change the usage or syntax of existing commands,
# which means a shallow learning curve for the average matplotlib user.
#
# In the below example, we create a 4-panel figure with the familiar "1D" and "2D"
# plot commands `~proplot.axes.PlotAxes.plot`, `~proplot.axes.PlotAxes.scatter`,
# `~proplot.axes.PlotAxes.pcolormesh`, and `~proplot.axes.PlotAxes.contourf`.
# See the :ref:`1D plotting <ug_1dplots>` and :ref:`2D plotting <ug_2dplots>`
# sections for details on the features added by proplot.


# %%
import proplot as pplt
import numpy as np

# Sample data
N = 20
state = np.random.RandomState(51423)
data = N + (state.rand(N, N) - 0.55).cumsum(axis=0).cumsum(axis=1)

# Example plots
cycle = pplt.Cycle('greys', left=0.2, N=5)
fig, axs = pplt.subplots(ncols=2, nrows=2, figwidth=5, share=False)
axs[0].plot(data[:, :5], linewidth=2, linestyle='--', cycle=cycle)
axs[1].scatter(data[:, :5], marker='x', cycle=cycle)
axs[2].pcolormesh(data, cmap='greys')
m = axs[3].contourf(data, cmap='greys')
axs.format(
    abc='a.', titleloc='l', title='Title',
    xlabel='xlabel', ylabel='ylabel', suptitle='Quick plotting demo'
)
fig.colorbar(m, loc='b', label='label')


# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_format:
#
# Formatting stuff
# ----------------
#
# Proplot's ``format`` command is your one-stop-shop for changing figure and axes
# settings. While one-liner matplotlib setters like ``set_xlabel`` and ``set_title``
# still work, ``format`` is usually more succinct -- it only needs to be called once.
# You can also pass arbitrary ``format`` arguments to axes-creation commands
# like `~proplot.figure.Figure.subplots`, `~proplot.figure.Figure.add_subplot`,
# `~proplot.axes.Axes.inset_axes`, `~proplot.axes.Axes.panel_axes`, and
# `~proplot.axes.CartesianAxes.altx` or `~proplot.axes..Axes.alty`. The keyword
# arguments accepted by ``format`` fall into the following groups:
#
# * Figure settings. These are related to row labels, column labels, and
#   figure "super" titles -- for example, ``fig.format(suptitle='Super title')``.
#   See `proplot.figure.Figure.format` for details.
#
# * General axes settings. These are related to background patches,
#   a-b-c labels, and axes titles -- for example, ``ax.format(title='Title')``
#   See `proplot.axes.Axes.format` for details.
#
# * Cartesian axes settings (valid only for `~proplot.axes.CartesianAxes`).
#   These are related to *x* and *y* axis ticks, spines, bounds, and labels --
#   for example, ``ax.format(xlim=(0, 5))`` changes the x axis bounds.
#   See `proplot.axes.CartesianAxes.format`
#   and :ref:`this section <ug_cartesian>` for details.
#
# * Polar axes settings (valid only for `~proplot.axes.PolarAxes`).
#   These are related to azimuthal and radial grid lines, bounds, and labels --
#   for example, ``ax.format(rlim=(0, 10))`` changes the radial bounds.
#   See `proplot.axes.PolarAxes.format`
#   and :ref:`this section <ug_polar>` for details.
#
# * Geographic axes settings (valid only for `~proplot.axes.GeoAxes`).
#   These are related to map bounds, meridian and parallel lines and labels,
#   and geographic features -- for example, ``ax.format(latlim=(0, 90))``
#   changes the meridional bounds. See `proplot.axes.GeoAxes.format`
#   and :ref:`this section <ug_geoformat>` for details.
#
# * `~proplot.config.rc` settings. Any keyword matching the name
#   of an rc setting is locally applied to the figure and axes.
#   If the name has "dots", you can pass it as a keyword argument with
#   the "dots" omitted or pass it to `rc_kw` in a dictionary. For example, the
#   default a-b-c label location is controlled by :rcraw:`abc.loc`. To change
#   this for an entire figure, you can use ``fig.format(abcloc='right')``
#   or ``fig.format(rc_kw={'abc.loc': 'right'})``.
#   See :ref:`this section <ug_config>` for more on rc settings.
#
# A ``format`` command is available on every figure and axes.
# `proplot.figure.Figure.format` accepts both figure and axes
# settings (applying them to each numbered subplot by default). Likewise,
# `proplot.axes.Axes.format` accepts both axes and figure settings.
# There is also a `proplot.gridspec.SubplotGrid.format` command
# that can be used to change settings for a subset of subplots
# -- for example, ``axs[:2].format(xtickminor=True)``
# turns on minor ticks for the first two subplots. See
# :ref:`this section <ug_subplotgrid>` for more on subplot grids.
#
# The below example shows the many different keyword arguments
# accepted by ``format``, and demonstrates how ``format`` can be
# used to succinctly and efficiently customize plots.

# %%
import proplot as pplt
import numpy as np
fig, axs = pplt.subplots(ncols=2, nrows=2, refwidth=2, share=False)
state = np.random.RandomState(51423)
N = 60
x = np.linspace(1, 10, N)
y = (state.rand(N, 5) - 0.5).cumsum(axis=0)
axs[0].plot(x, y, linewidth=1.5)
axs.format(
    suptitle='Format command demo',
    abc='A.', abcloc='ul',
    title='Main', ltitle='Left', rtitle='Right',  # different titles
    ultitle='Title 1', urtitle='Title 2', lltitle='Title 3', lrtitle='Title 4',
    toplabels=('Column 1', 'Column 2'),
    leftlabels=('Row 1', 'Row 2'),
    xlabel='xaxis', ylabel='yaxis',
    xscale='log',
    xlim=(1, 10), xticks=1,
    ylim=(-3, 3), yticks=pplt.arange(-3, 3),
    yticklabels=('a', 'bb', 'c', 'dd', 'e', 'ff', 'g'),
    ytickloc='both', yticklabelloc='both',
    xtickdir='inout', xtickminor=False, ygridminor=True,
)

# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_subplotgrid:
#
# Subplot grids
# -------------
#
# In matplotlib, `~matplotlib.figure.Figure.subplots` returns a 2D `~numpy.ndarray` for
# figures with more than one column and row, a 1D `~numpy.ndarray` for single-column or
# row figures, or an `~matplotlib.axes.Axes` for single-subplot figures. In proplot,
# `~proplot.figure.Figure.subplots` returns a `~proplot.gridspec.SubplotGrid` that
# unifies these possible return values:
#
# * `~proplot.gridspec.SubplotGrid` permits array-like 2D indexing, e.g.
#   ``axs[1, 0]``. Indexing the `~proplot.gridspec.SubplotGrid` is similar
#   to indexing a `~proplot.gridspec.GridSpec`. The result is a
#   `~proplot.gridspec.SubplotGrid` of subplots that occupy the indexed slot(s).
# * `~proplot.gridspec.SubplotGrid` permits list-like 1D indexing, e.g. ``axs[0]``.
#   The default order can be switched from row-major to column-major by passing
#   ``order='F'`` to `~proplot.ui.subplots`.
# * `~proplot.gridspec.SubplotGrid` behaves like a scalar when it is singleton.
#   That is, if you make a single subplot with ``fig, ax = pplt.subplots()``,
#   ``ax[0].method(...)`` is equivalent to ``ax.method(...)``.
#
# If you added subplots one-by-one with `~proplot.figure.Figure.subplot` or
# `~proplot.figure.Figure.add_subplot`, a `~proplot.gridspec.SubplotGrid` containing
# the numbered subplots is available via the `proplot.figure.Figure.subplotgrid`
# property. `~proplot.gridspec.SubplotGrid` is especially useful because it lets you
# call e.g. `~proplot.gridspec.SubplotGrid.format`,
# `~proplot.gridspec.SubplotGrid.panel_axes`,
# `~proplot.gridspec.SubplotGrid.inset_axes`,
# `~proplot.gridspec.SubplotGrid.altx`,
# and `~proplot.gridspec.SubplotGrid.alty` for all subplots in the grid at once.
# In the below example, we use `proplot.gridspec.SubplotGrid.format` on the grid
# returned by `~proplot.ui.subplots` to format different groups of subplots.

# %%
import proplot as pplt
import numpy as np
state = np.random.RandomState(51423)

# Selected subplots in a simple grid
fig, axs = pplt.subplots(ncols=4, nrows=4, refwidth=1.2, span=True)
axs.format(xlabel='xlabel', ylabel='ylabel', suptitle='SubplotGrid demo')
axs.format(grid=False, xlim=(0, 50), ylim=(-4, 4))
axs[:, 0].format(facecolor='blush', edgecolor='gray7', linewidth=1)  # eauivalent
axs[:, 0].format(fc='blush', ec='gray7', lw=1)
axs[0, :].format(fc='sky blue', ec='gray7', lw=1)
axs[0].format(ec='black', fc='gray5', lw=1.4)
axs[1:, 1:].format(fc='gray1')
for ax in axs[1:, 1:]:
    ax.plot((state.rand(50, 5) - 0.5).cumsum(axis=0), cycle='Grays', lw=2)

# Selected subplots in a complex grid
fig = pplt.figure(refwidth=2, span=False)
axs = fig.subplots([[1, 1, 2], [3, 4, 2], [3, 4, 5]], hratios=[2, 1, 1])
axs.format(xlabel='xlabel', ylabel='ylabel', suptitle='SubplotGrid demo')
axs[0].format(ec='black', fc='gray5', lw=1.4)
axs[1, 1:].format(fc='blush')
axs[1, :1].format(fc='sky blue')
axs[-1, -1].format(fc='gray2', grid=False)

# %% [raw] raw_mimetype="text/restructuredtext"
# .. _ug_rc:
#
# Settings and styles
# -------------------
#
# A dictionary-like object named `~proplot.config.rc` is created when you import
# proplot. `~proplot.config.rc` is similar to the matplotlib `~matplotlib.rcParams`
# dictionary, but can be used to change both `matplotlib settings
# <https://matplotlib.org/stable/tutorials/introductory/customizing.html>`__ and
# :ref:`proplot settings <ug_rcproplot>`. The matplotlib-specific settings are
# stored in `~proplot.config.rc_matplotlib` (our name for `matplotlib.rcParams`) and
# the proplot-specific settings are stored in `~proplot.config.rc_proplot`.
# Proplot also includes a :rcraw:`style` setting that can be used to
# switch between `matplotlib stylesheets
# <https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html>`__.
# See the :ref:`configuration section <ug_config>` for details.
#
# To modify a setting for just one subplot or figure, you can pass it to
# `proplot.axes.Axes.format` or `proplot.figure.Figure.format`. To temporarily
# modify setting(s) for a block of code, use `~proplot.config.Configurator.context`.
# To modify setting(s) for the entire python session, just assign it to the
# `~proplot.config.rc` dictionary or use `~proplot.config.Configurator.update`.
# To reset everything to the default state, use `~proplot.config.Configurator.reset`.
# See the below example.


# %%
import proplot as pplt
import numpy as np

# Update global settings in several different ways
pplt.rc.metacolor = 'gray6'
pplt.rc.update({'fontname': 'Source Sans Pro', 'fontsize': 11})
pplt.rc['figure.facecolor'] = 'gray3'
pplt.rc.axesfacecolor = 'gray4'
# pplt.rc.save()  # save the current settings to ~/.proplotrc

# Apply settings to figure with context()
with pplt.rc.context({'suptitle.size': 13}, toplabelcolor='gray6', metawidth=1.5):
    fig = pplt.figure(figwidth=6, sharey='limits', span=False)
    axs = fig.subplots(ncols=2)

# Plot lines with a custom cycler
N, M = 100, 7
state = np.random.RandomState(51423)
values = np.arange(1, M + 1)
cycle = pplt.get_colors('grays', M - 1) + ['red']
for i, ax in enumerate(axs):
    data = np.cumsum(state.rand(N, M) - 0.5, axis=0)
    lines = ax.plot(data, linewidth=3, cycle=cycle)

# Apply settings to axes with format()
axs.format(
    grid=False, xlabel='xlabel', ylabel='ylabel',
    toplabels=('Column 1', 'Column 2'),
    suptitle='Rc settings demo',
    suptitlecolor='gray7',
    abc='[A]', abcloc='l',
    title='Title', titleloc='r', titlecolor='gray7'
)

# Reset persistent modifications from head of cell
pplt.rc.reset()


# %%
import proplot as pplt
import numpy as np
# pplt.rc.style = 'style'  # set the style everywhere

# Sample data
state = np.random.RandomState(51423)
data = state.rand(10, 5)

# Set up figure
fig, axs = pplt.subplots(ncols=2, nrows=2, span=False, share=False)
axs.format(suptitle='Stylesheets demo')
styles = ('ggplot', 'seaborn', '538', 'bmh')

# Apply different styles to different axes with format()
for ax, style in zip(axs, styles):
    ax.format(style=style, xlabel='xlabel', ylabel='ylabel', title=style)
    ax.plot(data, linewidth=3)
