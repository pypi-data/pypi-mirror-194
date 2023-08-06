#!/usr/bin/env python3
"""
The standard Cartesian axes used for most proplot figures.
"""
import copy
import inspect

import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np

from .. import constructor
from .. import scale as pscale
from .. import ticker as pticker
from ..config import rc
from ..internals import ic  # noqa: F401
from ..internals import _not_none, _pop_rc, dependencies, docstring, texts, warnings
from . import plot, shared

__all__ = ['CartesianAxes']


# Dictionary to reverse side keywords
REVERSE_SIDE = {
    'left': 'right',
    'right': 'left',
    'bottom': 'top',
    'top': 'bottom',
}


# Format docstring
_format_docstring = """
aspect : {'auto', 'equal'} or float, optional
    The data aspect ratio. See `~matplotlib.axes.Axes.set_aspect`
    for details.
xlabel, ylabel : str, optional
    The x and y axis labels. Applied with `~matplotlib.axes.Axes.set_xlabel`
    and `~matplotlib.axes.Axes.set_ylabel`.
xlabel_kw, ylabel_kw : dict-like, optional
    Additional axis label settings applied with `~matplotlib.axes.Axes.set_xlabel`
    and `~matplotlib.axes.Axes.set_ylabel`. See also `labelpad`, `labelcolor`,
    `labelsize`, and `labelweight` below.
xlim, ylim : 2-tuple of floats or None, optional
    The x and y axis data limits. Applied with `~matplotlib.axes.Axes.set_xlim`
    and `~matplotlib.axes.Axes.set_ylim`.
xmin, ymin : float, optional
    The x and y minimum data limits. Useful if you do not want
    to set the maximum limits.
xmax, ymax : float, optional
    The x and y maximum data limits. Useful if you do not want
    to set the minimum limits.
xreverse, yreverse : bool, optional
    Whether to "reverse" the x and y axis direction. Makes the x and
    y axes ascend left-to-right and top-to-bottom, respectively.
xscale, yscale : scale-spec, optional
    The x and y axis scales. Passed to the `~proplot.scale.Scale` constructor.
    For example, ``xscale='log'`` applies logarithmic scaling, and
    ``xscale=('cutoff', 100, 2)`` applies a `~proplot.scale.CutoffScale`.
xscale_kw, yscale_kw : dict-like, optional
    The x and y axis scale settings. Passed to `~proplot.scale.Scale`.
xmargin, ymargin, margin : float, optional
    The default margin between plotted content and the x and y axis spines in
    axes-relative coordinates. Use this to add whitespace between plotted content and
    axes edges without explicitly setting the limits. Use `margin` to set both at once.
xbounds, ybounds : 2-tuple of float, optional
    The x and y axis data bounds within which to draw the spines. For example,
    ``xlim=(0, 4)`` combined with ``xbounds=(2, 4)`` will prevent the spines
    from meeting at the origin. This also applies ``xspineloc='bottom'`` and
    ``yspineloc='left'`` by default if both spines are currently visible.
xtickrange, ytickrange : 2-tuple of float, optional
    The x and y axis data ranges within which major tick marks are labelled.
    For example, ``xlim=(-5, 5)`` combined with ``xtickrange=(-1, 1)`` and a
    tick interval of 1 will only label the ticks marks at -1, 0, and 1. See
    `~proplot.ticker.AutoFormatter` for details.
xwraprange, ywraprange : 2-tuple of float, optional
    The x and y axis data ranges with which major tick mark values are wrapped. For
    example, ``xwraprange=(0, 3)`` causes the values 0 through 9 to be formatted as
    0, 1, 2, 0, 1, 2, 0, 1, 2, 0. See `~proplot.ticker.AutoFormatter` for details. This
    can be combined with `xtickrange` and `ytickrange` to make "stacked" line plots.
xloc, yloc : optional
    Shorthands for `xspineloc`, `yspineloc`.
xspineloc, yspineloc : {'bottom', 'top', 'left', 'right', \
'both', 'neither', 'none', 'zero', 'center'} or 2-tuple, optional
    The x and y spine locations. Applied with `~matplotlib.spines.Spine.set_position`.
    Propagates to `tickloc` unless specified otherwise.
xtickloc, ytickloc \
: {'bottom', 'top', 'left', 'right', 'both', 'neither', 'none'}, optional
    Which x and y axis spines should have major and minor tick marks. Inherits from
    `spineloc` by default and propagates to `ticklabelloc` unless specified otherwise.
xticklabelloc, yticklabelloc \
: {'bottom', 'top', 'left', 'right', 'both', 'neither', 'none'}, optional
    Which x and y axis spines should have major tick labels. Inherits from `tickloc`
    by default and propagates to `labelloc` and `offsetloc` unless specified otherwise.
xlabelloc, ylabelloc : {'bottom', 'top', 'left', 'right'}, optional
    Which x and y axis spines should have axis labels. Inherits from
    `ticklabelloc` by default (if `ticklabelloc` is a single side).
xoffsetloc, yoffsetloc : {'left', 'right'}, optional
    Which x and y axis spines should have the axis offset indicator. Inherits from
    `ticklabelloc` by default (if `ticklabelloc` is a single side).
xtickdir, ytickdir, tickdir : {'out', 'in', 'inout'}
    Direction that major and minor tick marks point for the x and y axis.
    Default is :rc:`tick.dir`. Use `tickdir` to control both.
xticklabeldir, yticklabeldir : {'in', 'out'}
    Whether to place x and y axis tick label text inside or outside the axes.
    Propagates to `xtickdir` and `ytickdir` unless specified otherwise.
xrotation, yrotation : float, optional
    The rotation for x and y axis tick labels. Default is ``0``
    for normal axes, :rc:`formatter.timerotation` for time x axes.
xgrid, ygrid, grid : bool, optional
    Whether to draw major gridlines on the x and y axis.
    Use `grid` to toggle both.
xgridminor, ygridminor, gridminor : bool, optional
    Whether to draw minor gridlines for the x and y axis.
    Use `gridminor` to toggle both.
xtickminor, ytickminor, tickminor : bool, optional
    Whether to draw minor ticks on the x and y axes.
    Use `tickminor` to toggle both.
xticks, yticks : optional
    Aliases for `xlocator`, `ylocator`.
xlocator, ylocator : locator-spec, optional
    Used to determine the x and y axis tick mark positions. Passed
    to the `~proplot.constructor.Locator` constructor.  Can be float,
    list of float, string, or `matplotlib.ticker.Locator` instance.
    Use ``[]``, ``'null'``, or ``'none'`` for no ticks.
xlocator_kw, ylocator_kw : dict-like, optional
    Keyword arguments passed to the `matplotlib.ticker.Locator` class.
xminorticks, yminorticks : optional
    Aliases for `xminorlocator`, `yminorlocator`.
xminorlocator, yminorlocator : optional
    As for `xlocator`, `ylocator`, but for the minor ticks.
xminorlocator_kw, yminorlocator_kw
    As for `xlocator_kw`, `ylocator_kw`, but for the minor locator.
xticklabels, yticklabels : optional
    Aliases for `xformatter`, `yformatter`.
xformatter, yformatter : formatter-spec, optional
    Used to determine the x and y axis tick label string format.
    Passed to the `~proplot.constructor.Formatter` constructor.
    Can be string, list of strings, or `matplotlib.ticker.Formatter`
    instance. Use ``[]``, ``'null'``, or ``'none'`` for no labels.
xformatter_kw, yformatter_kw : dict-like, optional
    Keyword arguments passed to the `matplotlib.ticker.Formatter` class.
xcolor, ycolor, color : color-spec, optional
    Color for the x and y axis spines, ticks, tick labels, and axis
    labels. Use `color` to set both at once.
xgridcolor, ygridcolor, gridcolor : color-spec, optional
    Color for the x and y axis major and minor gridlines. Default is :rc:`grid.color`.
    Use `gridcolor` to set both at once.
xlinewidth, ylinewidth, linewidth : color-spec, optional
    Line width for the x and y axis spines and major ticks. Propagates to
    `tickwidth` unless specified otherwise. Use `linewidth` to set both at once.
xtickcolor, ytickcolor, tickcolor : color-spec, optional
    Color for the x and y axis ticks. Default is `xcolor`, `ycolor`, and `color` or
    :rc:`tick.color` if they were not passed. Use `tickcolor` to set both at once.
xticklen, yticklen, ticklen : unit-spec, optional
    Major tick lengths for the x and y axis. Default is :rc:`tick.len`.
    %(units.pt)s
    Use `ticklen` to set both at once.
xticklenratio, yticklenratio, ticklenratio : float, optional
    Relative scaling of `xticklen` and `yticklen` used to determine
    minor tick lengths. Default is :rc:`tick.lenratio`.
    Use `ticklenratio` to set both at once.
xtickwidth, ytickwidth, tickwidth, : unit-spec, optional
    Major tick widths for the x ans y axis. Default is `linewidth`
    or :rc:`tick.width` if `linewidth` was not passed.
    %(units.pt)s
    Use `tickwidth` to set both at once.
xtickwidthratio, ytickwidthratio, tickwidthratio
    Relative scaling of `xtickwidth` and `ytickwidth` used to determine
    minor tick widths. Default is :rc:`tick.widthratio`.
    Use `tickwidthratio` to set both at once.
xticklabelpad, yticklabelpad : unit-spec, optional
    The padding between the x and y axis ticks and
    tick labels. Default is :rcraw:`tick.labelpad`.
    %(units.pt)s
xticklabelcolor, yticklabelcolor, ticklabelcolor : color-spec, optional
    Color for the x and y tick labels. Default is `xcolor`, `ycolor`, and `color` or
    :rc:`tick.labelcolor` if they were not passed. Use `ticklabelcolor` to set both.
xticklabelsize, yticklabelsize, ticklabelsize : unit-spec or str, optional
    Font size for the x and y tick labels. Default is :rc:`tick.labelsize`.
    %(units.pt)s
    Use `ticklabelsize` to set both at once.
xticklabelweight, yticklabelweight, ticklabelweight : str, optional
    Font weight for the x and y axis labels. Default is :rc:`label.weight`.
    Use `ticklabelweight` to set both at once.
xlabelpad, ylabelpad : unit-spec, optional
    The padding between the x and y axis bounding box and
    the x and y axis labels. Default is :rc:`label.pad`.
    %(units.pt)s
xlabelcolor, ylabelcolor, labelcolor : color-spec, optional
    Color for the x and y axis labels. Default is `xcolor`, `ycolor`, and `color` or
    :rc:`label.color` if they were not passed. Use `labelcolor` to set both at once.
xlabelsize, ylabelsize, labelsize : unit-spec or str, optional
    Font size for the x and y axis labels. Default is :rc:`label.size`.
    %(units.pt)s
    Use `labelsize` to set both at once.
xlabelweight, ylabelweight, labelweight : str, optional
    Font weight for the x and y axis labels. Default is :rc:`label.weight`.
    Use `labelweight` to set both at once.
fixticks : bool, optional
    Whether to always transform the tick locators to a
    `~matplotlib.ticker.FixedLocator` instance. Default is ``False``.
    If your axis ticks are doing weird things (for example, ticks
    drawn outside of the axis spine), try setting this to ``True``.
"""
docstring._snippet_manager['cartesian.format'] = _format_docstring


# Shared docstring
_shared_x_keys = {
    'x': 'x', 'x1': 'bottom', 'x2': 'top',
    'y': 'y', 'y1': 'left', 'y2': 'right',
}
_shared_y_keys = {
    'x': 'y', 'x1': 'left', 'x2': 'right',
    'y': 'x', 'y1': 'bottom', 'y2': 'top',
}
_shared_docstring = """
%(descrip)s
Parameters
----------
%(extra)s**kwargs
    Passed to `~proplot.axes.CartesianAxes`. Supports all valid
    `~proplot.axes.CartesianAxes.format` keywords. You can optionally
    omit the {x} from keywords beginning with ``{x}`` -- for example
    ``ax.alt{x}(lim=(0, 10))`` is equivalent to ``ax.alt{x}({x}lim=(0, 10))``.
    You can also change the default side for the axis spine, axis tick marks,
    axis tick labels, and/or axis labels by passing ``loc`` keywords. For example,
    ``ax.alt{x}(loc='{x1}')`` changes the default side from {x2} to {x1}.

Returns
-------
proplot.axes.CartesianAxes
    The resulting axes.

Note
----
This enforces the following default settings:

* Places the old {x} axis on the {x1} and the new {x}
  axis on the {x2}.
* Makes the old {x2} spine invisible and the new {x1}, {y1},
  and {y2} spines invisible.
* Adjusts the {x} axis tick, tick label, and axis label positions
  according to the visible spine positions.
* Syncs the old and new {y} axis limits and scales, and makes the
  new {y} axis labels invisible.
"""

# Alt docstrings
# NOTE: Used by SubplotGrid.altx
_alt_descrip = """
Add an axes locked to the same location with a
distinct {x} axis.
This is an alias and possibly more intuitive name for
`~proplot.axes.CartesianAxes.twin{y}`, which generates
two {x} axes with a shared ("twin") {y} axes.
"""
_alt_docstring = _shared_docstring % {'descrip': _alt_descrip, 'extra': ''}
docstring._snippet_manager['axes.altx'] = _alt_docstring.format(**_shared_x_keys)
docstring._snippet_manager['axes.alty'] = _alt_docstring.format(**_shared_y_keys)

# Twin docstrings
# NOTE: Used by SubplotGrid.twinx
_twin_descrip = """
Add an axes locked to the same location with a
distinct {x} axis.
This builds upon `matplotlib.axes.Axes.twin{y}`.
"""
_twin_docstring = _shared_docstring % {'descrip': _twin_descrip, 'extra': ''}
docstring._snippet_manager['axes.twinx'] = _twin_docstring.format(**_shared_y_keys)
docstring._snippet_manager['axes.twiny'] = _twin_docstring.format(**_shared_x_keys)

# Dual docstrings
# NOTE: Used by SubplotGrid.dualx
_dual_descrip = """
Add an axes locked to the same location whose {x} axis denotes
equivalent coordinates in alternate units.
This is an alternative to `matplotlib.axes.Axes.secondary_{x}axis` with
additional convenience features.
"""
_dual_extra = """
funcscale : callable, 2-tuple of callables, or scale-spec
    The scale used to transform units from the parent axis to the secondary
    axis. This can be a `~proplot.scale.FuncScale` itself or a function,
    (function, function) tuple, or an axis scale specification interpreted
    by the `~proplot.constructor.Scale` constructor function, any of which
    will be used to build a `~proplot.scale.FuncScale` and applied
    to the dual axis (see `~proplot.scale.FuncScale` for details).
"""
_dual_docstring = _shared_docstring % {'descrip': _dual_descrip, 'extra': _dual_extra.lstrip()}  # noqa: E501
docstring._snippet_manager['axes.dualx'] = _dual_docstring.format(**_shared_x_keys)
docstring._snippet_manager['axes.dualy'] = _dual_docstring.format(**_shared_y_keys)


class CartesianAxes(shared._SharedAxes, plot.PlotAxes):
    """
    Axes subclass for plotting in ordinary Cartesian coordinates. Adds the
    `~CartesianAxes.format` method and overrides several existing methods.

    Important
    ---------
    This is the default axes subclass. It can be specified explicitly by passing
    ``proj='cart'``, ``proj='cartesian'``, ``proj='rect'``, or ``proj='rectilinear'``
    to axes-creation commands like `~proplot.figure.Figure.add_axes`,
    `~proplot.figure.Figure.add_subplot`, and `~proplot.figure.Figure.subplots`.
    """
    _name = 'cartesian'
    _name_aliases = ('cart', 'rect', 'rectilinar')  # include matplotlib name

    @docstring._snippet_manager
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        *args
            Passed to `matplotlib.axes.Axes`.
        %(cartesian.format)s

        Other parameters
        ----------------
        %(axes.format)s
        %(rc.init)s

        See also
        --------
        CartesianAxes.format
        proplot.axes.Axes
        proplot.axes.PlotAxes
        proplot.figure.Figure.subplot
        proplot.figure.Figure.add_subplot
        """
        # Initialize axes
        self._xaxis_current_rotation = 'horizontal'  # current rotation
        self._yaxis_current_rotation = 'horizontal'
        self._xaxis_isdefault_rotation = True  # whether to auto rotate the axis
        self._yaxis_isdefault_rotation = True
        super().__init__(*args, **kwargs)

        # Apply default formatter
        if self.xaxis.isDefault_majfmt:
            self.xaxis.set_major_formatter(pticker.AutoFormatter())
            self.xaxis.isDefault_majfmt = True
        if self.yaxis.isDefault_majfmt:
            self.yaxis.set_major_formatter(pticker.AutoFormatter())
            self.yaxis.isDefault_majfmt = True

        # Dual axes utilities
        self._dualx_funcscale = None  # for scaling units on dual axes
        self._dualx_prevstate = None  # prevent excess _dualy_scale calls
        self._dualy_funcscale = None
        self._dualy_prevstate = None

    def _apply_axis_sharing(self):
        """
        Enforce the "shared" axis labels and axis tick labels. If this is not
        called at drawtime, "shared" labels can be inadvertantly turned off.
        """
        # X axis
        # NOTE: Critical to apply labels to *shared* axes attributes rather
        # than testing extents or we end up sharing labels with twin axes.
        # NOTE: Similar to how _align_super_labels() calls _apply_title_above() this
        # is called inside _align_axis_labels() so we align the correct text.
        # NOTE: The "panel sharing group" refers to axes and panels *above* the
        # bottommost or to the *right* of the leftmost panel. But the sharing level
        # used for the leftmost and bottommost is the *figure* sharing level.
        axis = self.xaxis
        if self._sharex is not None and axis.get_visible():
            level = 3 if self._panel_sharex_group else self.figure._sharex
            if level > 0:
                texts._transfer_text(axis.label, self._sharex.xaxis.label)
                axis.label.set_visible(False)
            if level > 2:
                # WARNING: Cannot set NullFormatter because shared axes share the
                # same Ticker(). Instead use approach copied from mpl subplots().
                axis.set_tick_params(which='both', labelbottom=False, labeltop=False)
        # Y axis
        axis = self.yaxis
        if self._sharey is not None and axis.get_visible():
            level = 3 if self._panel_sharey_group else self.figure._sharey
            if level > 0:
                texts._transfer_text(axis.label, self._sharey.yaxis.label)
                axis.label.set_visible(False)
            if level > 2:
                axis.set_tick_params(which='both', labelleft=False, labelright=False)
        axis.set_minor_formatter(mticker.NullFormatter())

    def _dualx_scale(self):
        """
        Lock the child "dual" *x* axis limits to the parent.
        """
        # NOTE: We bypass autoscale_view because we set limits manually, and bypass
        # child.stale = True because that is done in call to set_xlim() below.
        # NOTE: We set the scale using private API to bypass application of
        # set_default_locators_and_formatters: only_if_default=True is critical
        # to prevent overriding user settings!
        # NOTE: Dual axis only needs to be constrained if the parent axis scale
        # and limits have changed, and limits are always applied before we reach
        # the child.draw() because always called after parent.draw()
        funcscale, parent, child = self._dualx_funcscale, self._altx_parent, self
        if funcscale is None or parent is None:
            return
        olim = parent.get_xlim()
        scale = parent.xaxis._scale
        if (scale, *olim) == child._dualx_prevstate:
            return
        funcscale = pscale.FuncScale(funcscale, invert=True, parent_scale=scale)
        child.xaxis._scale = funcscale
        child._update_transScale()
        funcscale.set_default_locators_and_formatters(child.xaxis, only_if_default=True)
        nlim = list(map(funcscale.functions[1], np.array(olim)))
        if np.sign(np.diff(olim)) != np.sign(np.diff(nlim)):
            nlim = nlim[::-1]  # if function flips limits, so will set_xlim!
        child.set_xlim(nlim, emit=False)
        child._dualx_prevstate = (scale, *olim)

    def _dualy_scale(self):
        """
        Lock the child "dual" *y* axis limits to the parent.
        """
        # See _dualx_scale() comments
        funcscale, parent, child = self._dualy_funcscale, self._alty_parent, self
        if funcscale is None or parent is None:
            return
        olim = parent.get_ylim()
        scale = parent.yaxis._scale
        if (scale, *olim) == child._dualy_prevstate:
            return
        funcscale = pscale.FuncScale(funcscale, invert=True, parent_scale=scale)
        child.yaxis._scale = funcscale
        child._update_transScale()
        funcscale.set_default_locators_and_formatters(child.yaxis, only_if_default=True)
        nlim = list(map(funcscale.functions[1], np.array(olim)))
        if np.sign(np.diff(olim)) != np.sign(np.diff(nlim)):
            nlim = nlim[::-1]
        child.set_ylim(nlim, emit=False)
        child._dualy_prevstate = (scale, *olim)

    def _fix_ticks(self, x, fixticks=False):
        """
        Ensure there are no out-of-bounds ticks. Mostly a brute-force version of
        `~matplotlib.axis.Axis.set_smart_bounds` (which I couldn't get to work).
        """
        # NOTE: Previously triggered this every time FixedFormatter was found
        # on axis but 1) that seems heavy-handed + strange and 2) internal
        # application of FixedFormatter by boxplot resulted in subsequent format()
        # successfully calling this and messing up the ticks for some reason.
        # So avoid using this when possible, and try to make behavior consistent
        # by cacheing the locators before we use them for ticks.
        axis = getattr(self, f'{x}axis')
        sides = ('bottom', 'top') if x == 'x' else ('left', 'right')
        l0, l1 = getattr(self, f'get_{x}lim')()
        bounds = tuple(self.spines[side].get_bounds() or (None, None) for side in sides)
        skipticks = lambda xs: [  # noqa: E731
            x for x in xs if not any(
                x < _not_none(b0, l0) or x > _not_none(b1, l1) for (b0, b1) in bounds
            )
        ]
        if fixticks or any(x is not None for b in bounds for x in b):
            # Major locator
            locator = getattr(axis, '_major_locator_cached', None)
            if locator is None:
                locator = axis._major_locator_cached = axis.get_major_locator()
            locator = constructor.Locator(skipticks(locator()))
            axis.set_major_locator(locator)
            # Minor locator
            locator = getattr(axis, '_minor_locator_cached', None)
            if locator is None:
                locator = axis._minor_locator_cached = axis.get_minor_locator()
            locator = constructor.Locator(skipticks(locator()))
            axis.set_minor_locator(locator)

    def _get_spine_side(self, x, loc):
        """
        Get the spine side implied by the input location or position. This
        propagates to tick mark, tick label, and axis label positions.
        """
        sides = ('bottom', 'top') if x == 'x' else ('left', 'right')
        centers = ('zero', 'center')
        options = (*sides, 'both', 'neither', 'none')
        if np.iterable(loc) and len(loc) == 2 and loc[0] in ('axes', 'data', 'outward'):
            lim = getattr(self, f'get_{x}lim')()
            if loc[0] == 'outward':  # ambiguous so just choose first side
                side = sides[0]
            elif loc[0] == 'axes':
                side = sides[int(loc[1] > 0.5)]
            else:
                side = sides[int(loc[1] > lim[0] + 0.5 * (lim[1] - lim[0]))]
        elif loc in centers:  # ambiguous so just choose first side
            side = sides[0]
        elif loc is None or loc in options:
            side = loc
        else:
            raise ValueError(
                f'Invalid {x} spine location {loc!r}. Options are: '
                + ', '.join(map(repr, (*options, *centers)))
                + " or a coordinate position ('axes', coord), "
                + " ('data', coord), or ('outward', coord)."
            )
        return side

    def _is_panel_group_member(self, other):
        """
        Return whether the axes belong in a panel sharing stack..
        """
        return (
            self._panel_parent is other  # other is child panel
            or other._panel_parent is self  # other is main subplot
            or other._panel_parent and self._panel_parent  # ...
            and other._panel_parent is self._panel_parent  # other is sibling panel
        )

    def _sharex_limits(self, sharex):
        """
        Safely share limits and tickers without resetting things.
        """
        # Copy non-default limits and scales. Either this axes or the input
        # axes could be a newly-created subplot while the other is a subplot
        # with possibly-modified user settings we are careful to preserve.
        for (ax1, ax2) in ((self, sharex), (sharex, self)):
            if ax1.get_xscale() == 'linear' and ax2.get_xscale() != 'linear':
                ax1.set_xscale(ax2.get_xscale())  # non-default scale
            if ax1.get_autoscalex_on() and not ax2.get_autoscalex_on():
                ax1.set_xlim(ax2.get_xlim())  # non-default limits
        # Copy non-default locators and formatters
        self._shared_x_axes.join(self, sharex)  # share limit/scale changes
        if sharex.xaxis.isDefault_majloc and not self.xaxis.isDefault_majloc:
            sharex.xaxis.set_major_locator(self.xaxis.get_major_locator())
        if sharex.xaxis.isDefault_minloc and not self.xaxis.isDefault_minloc:
            sharex.xaxis.set_minor_locator(self.xaxis.get_minor_locator())
        if sharex.xaxis.isDefault_majfmt and not self.xaxis.isDefault_majfmt:
            sharex.xaxis.set_major_formatter(self.xaxis.get_major_formatter())
        if sharex.xaxis.isDefault_minfmt and not self.xaxis.isDefault_minfmt:
            sharex.xaxis.set_minor_formatter(self.xaxis.get_minor_formatter())
        self.xaxis.major = sharex.xaxis.major
        self.xaxis.minor = sharex.xaxis.minor

    def _sharey_limits(self, sharey):
        """
        Safely share limits and tickers without resetting things.
        """
        # NOTE: See _sharex_limits for notes
        for (ax1, ax2) in ((self, sharey), (sharey, self)):
            if ax1.get_yscale() == 'linear' and ax2.get_yscale() != 'linear':
                ax1.set_yscale(ax2.get_yscale())
            if ax1.get_autoscaley_on() and not ax2.get_autoscaley_on():
                ax1.set_ylim(ax2.get_ylim())
        self._shared_y_axes.join(self, sharey)  # share limit/scale changes
        if sharey.yaxis.isDefault_majloc and not self.yaxis.isDefault_majloc:
            sharey.yaxis.set_major_locator(self.yaxis.get_major_locator())
        if sharey.yaxis.isDefault_minloc and not self.yaxis.isDefault_minloc:
            sharey.yaxis.set_minor_locator(self.yaxis.get_minor_locator())
        if sharey.yaxis.isDefault_majfmt and not self.yaxis.isDefault_majfmt:
            sharey.yaxis.set_major_formatter(self.yaxis.get_major_formatter())
        if sharey.yaxis.isDefault_minfmt and not self.yaxis.isDefault_minfmt:
            sharey.yaxis.set_minor_formatter(self.yaxis.get_minor_formatter())
        self.yaxis.major = sharey.yaxis.major
        self.yaxis.minor = sharey.yaxis.minor

    def _sharex_setup(self, sharex, *, labels=True, limits=True):
        """
        Configure shared axes accounting. Input is the 'parent' axes from which this
        one will draw its properties. Use keyword args to override settings.
        """
        # Share panels across *different* subplots
        super()._sharex_setup(sharex)
        # Get the axis sharing level
        level = (
            3 if self._panel_sharex_group and self._is_panel_group_member(sharex)
            else self.figure._sharex
        )
        if level not in range(5):  # must be internal error
            raise ValueError(f'Invalid sharing level sharex={level!r}.')
        if sharex in (None, self) or not isinstance(sharex, CartesianAxes):
            return
        # Share future axis label changes. Implemented in _apply_axis_sharing().
        # Matplotlib only uses these attributes in __init__() and cla() to share
        # tickers -- all other builtin sharing features derives from _shared_x_axes
        if level > 0 and labels:
            self._sharex = sharex
        # Share future axis tickers, limits, and scales
        # NOTE: Only difference between levels 2 and 3 is level 3 hides tick
        # labels. But this is done after the fact -- tickers are still shared.
        if level > 1 and limits:
            self._sharex_limits(sharex)

    def _sharey_setup(self, sharey, *, labels=True, limits=True):
        """
        Configure shared axes accounting for panels. The input is the
        'parent' axes, from which this one will draw its properties.
        """
        # NOTE: See _sharex_setup for notes
        super()._sharey_setup(sharey)
        level = (
            3 if self._panel_sharey_group and self._is_panel_group_member(sharey)
            else self.figure._sharey
        )
        if level not in range(5):  # must be internal error
            raise ValueError(f'Invalid sharing level sharey={level!r}.')
        if sharey in (None, self) or not isinstance(sharey, CartesianAxes):
            return
        if level > 0 and labels:
            self._sharey = sharey
        if level > 1 and limits:
            self._sharey_limits(sharey)

    def _update_formatter(
        self, x, formatter=None, *, formatter_kw=None,
        tickrange=None, wraprange=None,
    ):
        """
        Update the axis formatter. Passes `formatter` through `Formatter` with kwargs.
        """
        # Test if this is date axes
        # See: https://matplotlib.org/api/units_api.html
        # And: https://matplotlib.org/api/dates_api.html
        axis = getattr(self, x + 'axis')
        date = isinstance(axis.converter, mdates.DateConverter)

        # Major formatter
        # NOTE: The default axis formatter accepts lots of keywords. So unlike
        # everywhere else that uses constructor functions we also allow only
        # formatter_kw input without formatter and use 'auto' as the default.
        formatter_kw = formatter_kw or {}
        formatter_kw = formatter_kw.copy()
        if formatter is not None or tickrange is not None or wraprange is not None or formatter_kw:  # noqa: E501
            # Tick range
            formatter = _not_none(formatter, 'auto')
            if tickrange is not None or wraprange is not None:
                if formatter != 'auto':
                    warnings._warn_proplot(
                        'The tickrange and autorange features require '
                        'proplot.AutoFormatter formatter. Overriding the input.'
                    )
                if tickrange is not None:
                    formatter_kw.setdefault('tickrange', tickrange)
                if wraprange is not None:
                    formatter_kw.setdefault('wraprange', wraprange)

            # Set the formatter
            # Note some formatters require 'locator' as keyword arg
            if formatter in ('date', 'concise'):
                locator = axis.get_major_locator()
                formatter_kw.setdefault('locator', locator)
            formatter = constructor.Formatter(formatter, date=date, **formatter_kw)
            axis.set_major_formatter(formatter)

    def _update_labels(self, x, *args, **kwargs):
        """
        Apply axis labels to the relevant shared axis. If spanning labels are toggled
        this keeps the labels synced for all subplots in the same row or column. Label
        positions will be adjusted at draw-time with figure._align_axislabels.
        """
        # NOTE: Critical to test whether arguments are None or else this
        # will set isDefault_label to False every time format() is called.
        # NOTE: This always updates the *current* labels and sharing is handled
        # later so that labels set with set_xlabel() and set_ylabel() are shared too.
        # See notes in _align_axis_labels() and _apply_axis_sharing().
        kwargs = self._get_label_props(**kwargs)
        no_args = all(a is None for a in args)
        no_kwargs = all(v is None for v in kwargs.values())
        if no_args and no_kwargs:
            return  # also returns if args and kwargs are empty
        setter = getattr(self, 'set_' + x + 'label')
        getter = getattr(self, 'get_' + x + 'label')
        if no_args:  # otherwise label text is reset!
            args = (getter(),)
        setter(*args, **kwargs)

    def _update_locators(
        self, x, locator=None, minorlocator=None, *,
        tickminor=None, locator_kw=None, minorlocator_kw=None,
    ):
        """
        Update the locators. Requires `Locator` instances.
        """
        # Apply input major locator
        axis = getattr(self, x + 'axis')
        locator_kw = locator_kw or {}
        if locator is not None:
            locator = constructor.Locator(locator, **locator_kw)
            axis.set_major_locator(locator)
            if isinstance(locator, mticker.IndexLocator):
                tickminor = _not_none(tickminor, False)  # disable 'index' minor ticks

        # Apply input or default minor locator
        # NOTE: Parts of API (dualxy) rely on minor tick toggling preserving the
        # isDefault_minloc setting. In future should override mpl minorticks_on()
        # NOTE: Unlike matplotlib when "turning on" minor ticks we *always* use the
        # scale default, thanks to scale classes refactoring with _ScaleBase.
        isdefault = minorlocator is None
        minorlocator_kw = minorlocator_kw or {}
        if not isdefault:
            minorlocator = constructor.Locator(minorlocator, **minorlocator_kw)
        elif tickminor:
            minorlocator = getattr(axis._scale, '_default_minor_locator', None)
            minorlocator = copy.copy(minorlocator)
            minorlocator = constructor.Locator(minorlocator or 'minor')
        if minorlocator is not None:
            axis.set_minor_locator(minorlocator)
            axis.isDefault_minloc = isdefault

        # Disable minor ticks
        # NOTE: Generally if you *enable* minor ticks on a dual axis, want to
        # allow FuncScale updates to change the minor tick locators. If you
        # *disable* minor ticks, do not want FuncScale applications to turn them
        # on. So we allow below to set isDefault_minloc to False.
        if tickminor is not None and not tickminor:
            axis.set_minor_locator(constructor.Locator('null'))

    def _update_limits(self, x, *, min_=None, max_=None, lim=None, reverse=None):
        """
        Update the axis limits.
        """
        # Set limits for just one side or both at once
        axis = getattr(self, x + 'axis')
        if min_ is not None or max_ is not None:
            if lim is not None:
                warnings._warn_proplot(
                    f'Overriding {x}lim={lim!r} '
                    f'with {x}min={min_!r} and {x}max={max_!r}.'
                )
            lim = (min_, max_)
        if lim is not None:
            getattr(self, 'set_' + x + 'lim')(lim)

        # Reverse direction
        # NOTE: 3.1+ has axis.set_inverted(), below is from source code
        if reverse is not None:
            lo, hi = axis.get_view_interval()
            if reverse:
                lim = (max(lo, hi), min(lo, hi))
            else:
                lim = (min(lo, hi), max(lo, hi))
            axis.set_view_interval(*lim, ignore=True)

    def _update_rotation(self, x, *, rotation=None):
        """
        Rotate the tick labels. Rotate 90 degrees by default for datetime *x* axes.
        """
        # Apply rotation for datetime axes.
        # NOTE: Rotation is done *before* horizontal/vertical alignment. Cannot
        # change alignment with set_tick_params so we must apply to text objects.
        # Note fig.autofmt_date calls subplots_adjust, so we cannot use it.
        x = _not_none(x, 'x')
        current = '_' + x + 'axis_current_rotation'
        default = '_' + x + 'axis_isdefault_rotation'
        axis = getattr(self, x + 'axis')
        if rotation is not None:
            setattr(self, default, False)
        elif not getattr(self, default):
            return  # do not rotate
        elif x == 'x' and isinstance(axis.converter, mdates.DateConverter):
            rotation = rc['formatter.timerotation']
        else:
            rotation = 'horizontal'

        # Apply tick label rotation if necessary
        if rotation != getattr(self, current):
            rotation = {'horizontal': 0, 'vertical': 90}.get(rotation, rotation)
            kw = {'rotation': rotation}
            if rotation not in (0, 90, -90):
                kw['ha'] = 'right' if rotation > 0 else 'left'
            for label in axis.get_ticklabels():
                label.update(kw)
            setattr(self, current, rotation)

    def _update_spines(self, x, *, loc=None, bounds=None):
        """
        Update the spine settings.
        """
        # Iterate over spines associated with this axis
        sides = ('bottom', 'top') if x == 'x' else ('left', 'right')
        pside = self._get_spine_side(x, loc)  # side for set_position()
        if bounds is not None and all(self.spines[s].get_visible() for s in sides):
            loc = _not_none(loc, sides[0])
        for side in sides:
            # Change default spine location from 'both' to the first relevant
            # side if the user passes 'bounds'.
            spine = self.spines[side]
            # Eliminate sides
            if loc is None:
                pass
            elif loc == 'neither' or loc == 'none':
                spine.set_visible(False)
            elif loc == 'both':
                spine.set_visible(True)
            elif loc in sides:  # make relevant spine visible
                spine.set_visible(side == loc)
            # Special spine location, usually 'zero', 'center', or tuple with
            # (units, location) where 'units' can be 'axes', 'data', or 'outward'.
            # Matplotlib internally represents these with 'bottom' and 'left'.
            elif pside != side:
                spine.set_visible(False)
            else:
                spine.set_visible(True)
                try:
                    spine.set_position(loc)
                except ValueError:
                    raise ValueError(
                        f'Invalid {x} spine location {loc!r}. Options are: '
                        + ', '.join(map(repr, (*sides, 'both', 'neither'))) + '.'
                    )
            # Apply spine bounds
            if bounds is not None:
                spine.set_bounds(*bounds)

    def _update_locs(
        self, x, *, tickloc=None, ticklabelloc=None, labelloc=None, offsetloc=None
    ):
        """
        Update the tick, tick label, and axis label locations.
        """
        # The tick and tick label sides for Cartesian axes
        kw = {}
        sides = ('bottom', 'top') if x == 'x' else ('left', 'right')
        sides_map = {'both': sides, 'neither': (), 'none': (), None: None}
        sides_active = tuple(side for side in sides if self.spines[side].get_visible())

        # The tick side(s)
        # NOTE: Silently forbids adding ticks to sides with invisible spines
        ticklocs = sides_map.get(tickloc, (tickloc,))
        if ticklocs and any(loc not in sides for loc in ticklocs):
            raise ValueError(
                f'Invalid tick mark location {tickloc!r}. Options are '
                + ', '.join(map(repr, sides + tuple(sides_map))) + '.'
            )
        if ticklocs is not None:
            kw.update({side: side in ticklocs for side in sides})
        kw.update(
            {
                side: False for side in sides if side not in sides_active
            }
        )

        # The tick label side(s). Make sure these only appear where ticks are
        # NOTE: Silently forbids adding labels to sides with invisible ticks or spines
        ticklabellocs = sides_map.get(ticklabelloc, (ticklabelloc,))
        if ticklabellocs and any(loc not in sides for loc in ticklabellocs):
            raise ValueError(
                f'Invalid tick label location {ticklabelloc!r}. Options are '
                + ', '.join(map(repr, sides + tuple(sides_map))) + '.'
            )
        if ticklabellocs is not None:
            kw.update({'label' + side: (side in ticklabellocs) for side in sides})
        kw.update(
            {
                'label' + side: False for side in sides
                if side not in sides_active
                or ticklocs is not None and side not in ticklocs
            }
        )

        # The axis label side(s)
        # NOTE: Silently forbids adding labels and offsets to sides with missing spines
        if ticklocs is not None:
            options = tuple(_ for _ in sides if _ in ticklocs and _ in sides_active)
            if len(options) == 1:
                labelloc = _not_none(labelloc, options[0])
                offsetloc = _not_none(offsetloc, options[0])
        if labelloc is not None and labelloc not in sides:
            raise ValueError(
                f'Invalid label location {labelloc!r}. Options are '
                + ', '.join(map(repr, sides)) + '.'
            )

        # Apply the tick, tick label, and label locations
        # Uses ugly mpl 3.3+ tick_top() tick_bottom() kludge for offset location
        # See: https://matplotlib.org/3.3.1/users/whats_new.html
        axis = getattr(self, x + 'axis')
        self.tick_params(axis=x, which='both', **kw)
        if labelloc is not None:
            axis.set_label_position(labelloc)
        if offsetloc is not None:
            if hasattr(axis, 'set_offset_position'):  # y axis (and future x axis?)
                axis.set_offset_position(offsetloc)
            elif x == 'x' and dependencies._version_mpl >= 3.3:  # ugly mpl kludge
                axis._tick_position = offsetloc
                axis.offsetText.set_verticalalignment(REVERSE_SIDE[offsetloc])

    @docstring._snippet_manager
    def format(
        self, *,
        aspect=None,
        xloc=None, yloc=None,
        xspineloc=None, yspineloc=None,
        xoffsetloc=None, yoffsetloc=None,
        xwraprange=None, ywraprange=None,
        xreverse=None, yreverse=None,
        xlim=None, ylim=None,
        xmin=None, ymin=None,
        xmax=None, ymax=None,
        xscale=None, yscale=None,
        xbounds=None, ybounds=None,
        xmargin=None, ymargin=None,
        xrotation=None, yrotation=None,
        xformatter=None, yformatter=None,
        xticklabels=None, yticklabels=None,
        xticks=None, yticks=None,
        xlocator=None, ylocator=None,
        xminorticks=None, yminorticks=None,
        xminorlocator=None, yminorlocator=None,
        xcolor=None, ycolor=None,
        xlinewidth=None, ylinewidth=None,
        xtickloc=None, ytickloc=None, fixticks=False,
        xtickdir=None, ytickdir=None,
        xtickminor=None, ytickminor=None,
        xtickrange=None, ytickrange=None,
        xtickcolor=None, ytickcolor=None,
        xticklen=None, yticklen=None,
        xticklenratio=None, yticklenratio=None,
        xtickwidth=None, ytickwidth=None,
        xtickwidthratio=None, ytickwidthratio=None,
        xticklabelloc=None, yticklabelloc=None,
        xticklabeldir=None, yticklabeldir=None,
        xticklabelpad=None, yticklabelpad=None,
        xticklabelcolor=None, yticklabelcolor=None,
        xticklabelsize=None, yticklabelsize=None,
        xticklabelweight=None, yticklabelweight=None,
        xlabel=None, ylabel=None,
        xlabelloc=None, ylabelloc=None,
        xlabelpad=None, ylabelpad=None,
        xlabelcolor=None, ylabelcolor=None,
        xlabelsize=None, ylabelsize=None,
        xlabelweight=None, ylabelweight=None,
        xgrid=None, ygrid=None,
        xgridminor=None, ygridminor=None,
        xgridcolor=None, ygridcolor=None,
        xlabel_kw=None, ylabel_kw=None,
        xscale_kw=None, yscale_kw=None,
        xlocator_kw=None, ylocator_kw=None,
        xformatter_kw=None, yformatter_kw=None,
        xminorlocator_kw=None, yminorlocator_kw=None,
        **kwargs
    ):
        """
        Modify axes limits, axis scales, axis labels, spine locations,
        tick locations, tick labels, and more.

        Parameters
        ----------
        %(cartesian.format)s

        Other parameters
        ----------------
        %(axes.format)s
        %(figure.format)s
        %(rc.format)s

        See also
        --------
        proplot.axes.Axes.format
        proplot.figure.Figure.format
        proplot.config.Configurator.context

        Note
        ----
        If you plot something with a `datetime64 \
<https://docs.scipy.org/doc/numpy/reference/arrays.datetime.html>`__,
        `pandas.Timestamp`, `pandas.DatetimeIndex`, `datetime.date`, `datetime.time`,
        or `datetime.datetime` array as the x or y axis coordinate, the axis ticks
        and tick labels will be automatically formatted as dates.
        """
        rc_kw, rc_mode = _pop_rc(kwargs)
        with rc.context(rc_kw, mode=rc_mode):
            # No mutable default args
            xlabel_kw = xlabel_kw or {}
            ylabel_kw = ylabel_kw or {}
            xscale_kw = xscale_kw or {}
            yscale_kw = yscale_kw or {}
            xlocator_kw = xlocator_kw or {}
            ylocator_kw = ylocator_kw or {}
            xformatter_kw = xformatter_kw or {}
            yformatter_kw = yformatter_kw or {}
            xminorlocator_kw = xminorlocator_kw or {}
            yminorlocator_kw = yminorlocator_kw or {}

            # Color keyword arguments. Inherit from 'color' when necessary
            color = kwargs.pop('color', None)
            xcolor = _not_none(xcolor, color)
            ycolor = _not_none(ycolor, color)
            if 'tick.color' not in rc_kw:
                xtickcolor = _not_none(xtickcolor, xcolor)
                ytickcolor = _not_none(ytickcolor, ycolor)
            if 'tick.labelcolor' not in rc_kw:
                xticklabelcolor = _not_none(xticklabelcolor, xcolor)
                yticklabelcolor = _not_none(yticklabelcolor, ycolor)
            if 'label.color' not in rc_kw:
                xlabelcolor = _not_none(xlabelcolor, xcolor)
                ylabelcolor = _not_none(ylabelcolor, ycolor)

            # Flexible keyword args, declare defaults
            # NOTE: 'xtickdir' and 'ytickdir' read from 'tickdir' arguments here
            xmargin = _not_none(xmargin, rc.find('axes.xmargin', context=True))
            ymargin = _not_none(ymargin, rc.find('axes.ymargin', context=True))
            xtickdir = _not_none(xtickdir, rc.find('xtick.direction', context=True))
            ytickdir = _not_none(ytickdir, rc.find('ytick.direction', context=True))
            xformatter = _not_none(xformatter=xformatter, xticklabels=xticklabels)
            yformatter = _not_none(yformatter=yformatter, yticklabels=yticklabels)
            xlocator = _not_none(xlocator=xlocator, xticks=xticks)
            ylocator = _not_none(ylocator=ylocator, yticks=yticks)
            xtickminor = _not_none(xtickminor, rc.find('xtick.minor.visible', context=True))  # noqa: E501
            ytickminor = _not_none(ytickminor, rc.find('ytick.minor.visible', context=True))  # noqa: E501
            xminorlocator = _not_none(xminorlocator=xminorlocator, xminorticks=xminorticks)  # noqa: E501
            yminorlocator = _not_none(yminorlocator=yminorlocator, yminorticks=yminorticks)  # noqa: E501
            ticklabeldir = kwargs.pop('ticklabeldir', None)
            xticklabeldir = _not_none(xticklabeldir, ticklabeldir)
            yticklabeldir = _not_none(yticklabeldir, ticklabeldir)
            xtickdir = _not_none(xtickdir, xticklabeldir)
            ytickdir = _not_none(ytickdir, yticklabeldir)

            # Sensible defaults for spine, tick, tick label, and label locs
            # NOTE: Allow tick labels to be present without ticks! User may
            # want this sometimes! Same goes for spines!
            xspineloc = _not_none(xloc=xloc, xspineloc=xspineloc)
            yspineloc = _not_none(yloc=yloc, yspineloc=yspineloc)
            xside = self._get_spine_side('x', xspineloc)
            yside = self._get_spine_side('y', yspineloc)
            if xside is not None and xside not in ('zero', 'center', 'both'):
                xtickloc = _not_none(xtickloc, xside)
            if yside is not None and yside not in ('zero', 'center', 'both'):
                ytickloc = _not_none(ytickloc, yside)
            if xtickloc != 'both':  # then infer others
                xticklabelloc = _not_none(xticklabelloc, xtickloc)
                if xticklabelloc in ('bottom', 'top'):
                    xlabelloc = _not_none(xlabelloc, xticklabelloc)
                    xoffsetloc = _not_none(xoffsetloc, yticklabelloc)
            if ytickloc != 'both':  # then infer others
                yticklabelloc = _not_none(yticklabelloc, ytickloc)
                if yticklabelloc in ('left', 'right'):
                    ylabelloc = _not_none(ylabelloc, yticklabelloc)
                    yoffsetloc = _not_none(yoffsetloc, yticklabelloc)
            xtickloc = _not_none(xtickloc, self._get_loc('x', 'xtick'))  # rc
            ytickloc = _not_none(ytickloc, self._get_loc('y', 'ytick'))  # rc
            xspineloc = _not_none(xspineloc, self._get_loc('x', 'axes.spines'))  # rc
            yspineloc = _not_none(yspineloc, self._get_loc('y', 'axes.spines'))  # rc

            # Loop over axes
            for (
                x,
                min_,
                max_,
                lim,
                reverse,
                margin,
                bounds,
                tickrange,
                wraprange,
                scale,
                scale_kw,
                spineloc,
                tickloc,
                ticklabelloc,
                labelloc,
                offsetloc,
                grid,
                gridminor,
                locator,
                locator_kw,
                minorlocator,
                minorlocator_kw,
                formatter,
                formatter_kw,
                label,
                label_kw,
                color,
                gridcolor,
                linewidth,
                rotation,
                tickminor,
                tickdir,
                tickcolor,
                ticklen,
                ticklenratio,
                tickwidth,
                tickwidthratio,
                ticklabeldir,
                ticklabelpad,
                ticklabelcolor,
                ticklabelsize,
                ticklabelweight,
                labelpad,
                labelcolor,
                labelsize,
                labelweight,
            ) in zip(
                ('x', 'y'),
                (xmin, ymin),
                (xmax, ymax),
                (xlim, ylim),
                (xreverse, yreverse),
                (xmargin, ymargin),
                (xbounds, ybounds),
                (xtickrange, ytickrange),
                (xwraprange, ywraprange),
                (xscale, yscale),
                (xscale_kw, yscale_kw),
                (xspineloc, yspineloc),
                (xtickloc, ytickloc),
                (xticklabelloc, yticklabelloc),
                (xlabelloc, ylabelloc),
                (xoffsetloc, yoffsetloc),
                (xgrid, ygrid),
                (xgridminor, ygridminor),
                (xlocator, ylocator),
                (xlocator_kw, ylocator_kw),
                (xminorlocator, yminorlocator),
                (xminorlocator_kw, yminorlocator_kw),
                (xformatter, yformatter),
                (xformatter_kw, yformatter_kw),
                (xlabel, ylabel),
                (xlabel_kw, ylabel_kw),
                (xcolor, ycolor),
                (xgridcolor, ygridcolor),
                (xlinewidth, ylinewidth),
                (xrotation, yrotation),
                (xtickminor, ytickminor),
                (xtickdir, ytickdir),
                (xtickcolor, ytickcolor),
                (xticklen, yticklen),
                (xticklenratio, yticklenratio),
                (xtickwidth, ytickwidth),
                (xtickwidthratio, ytickwidthratio),
                (xticklabeldir, yticklabeldir),
                (xticklabelpad, yticklabelpad),
                (xticklabelcolor, yticklabelcolor),
                (xticklabelsize, yticklabelsize),
                (xticklabelweight, yticklabelweight),
                (xlabelpad, ylabelpad),
                (xlabelcolor, ylabelcolor),
                (xlabelsize, ylabelsize),
                (xlabelweight, ylabelweight),
            ):
                # Axis scale
                # WARNING: This relies on monkey patch of mscale.scale_factory
                # that allows it to accept a custom scale class!
                # WARNING: Changing axis scale also changes default locators
                # and formatters, and restricts possible range of axis limits,
                # so critical to do it first.
                if scale is not None:
                    scale = constructor.Scale(scale, **scale_kw)
                    getattr(self, 'set_' + x + 'scale')(scale)

                # Axis limits
                self._update_limits(
                    x, min_=min_, max_=max_, lim=lim, reverse=reverse
                )
                if margin is not None:
                    self.margins(**{x: margin})

                # Axis spine settings
                # NOTE: This sets spine-specific color and linewidth settings. For
                # non-specific settings _update_background is called in Axes.format()
                self._update_spines(
                    x, loc=spineloc, bounds=bounds
                )
                self._update_background(
                    x, edgecolor=color, linewidth=linewidth,
                    tickwidth=tickwidth, tickwidthratio=tickwidthratio,
                )

                # Axis tick settings
                self._update_locs(
                    x, tickloc=tickloc, ticklabelloc=ticklabelloc,
                    labelloc=labelloc, offsetloc=offsetloc,
                )
                self._update_rotation(
                    x, rotation=rotation
                )
                self._update_ticks(
                    x, grid=grid, gridminor=gridminor,
                    ticklen=ticklen, ticklenratio=ticklenratio,
                    tickdir=tickdir, labeldir=ticklabeldir, labelpad=ticklabelpad,
                    tickcolor=tickcolor, gridcolor=gridcolor, labelcolor=ticklabelcolor,
                    labelsize=ticklabelsize, labelweight=ticklabelweight,
                )

                # Axis label settings
                # NOTE: This must come after set_label_position, or any ha and va
                # overrides in label_kw are overwritten.
                kw = dict(
                    labelpad=labelpad,
                    color=labelcolor,
                    size=labelsize,
                    weight=labelweight,
                    **label_kw
                )
                self._update_labels(x, label, **kw)

                # Axis locator
                if minorlocator is True or minorlocator is False:  # must test identity
                    warnings._warn_proplot(
                        f'You passed {x}minorticks={minorlocator}, but this '
                        'argument is used to specify tick *locations*. If '
                        'you just want to *toggle* minor ticks on and off, '
                        f'please use {x}tickminor=True or {x}tickminor=False.'
                    )
                    minorlocator = None
                self._update_locators(
                    x, locator, minorlocator, tickminor=tickminor,
                    locator_kw=locator_kw, minorlocator_kw=minorlocator_kw,
                )

                # Axis formatter
                self._update_formatter(
                    x, formatter, formatter_kw=formatter_kw,
                    tickrange=tickrange, wraprange=wraprange,
                )

                # Ensure ticks are within axis bounds
                self._fix_ticks(x, fixticks=fixticks)

        # Parent format method
        if aspect is not None:
            self.set_aspect(aspect)
        super().format(rc_kw=rc_kw, rc_mode=rc_mode, **kwargs)

    def _parse_alt(self, x, **kwargs):
        """
        Optionally omit the leading x or y from "twin axes" methods.
        """
        sig = self._format_signatures[CartesianAxes]
        keys = tuple(key[1:] for key in sig.parameters if key[0] == x)
        kwargs = {(x + key if key in keys else key): val for key, val in kwargs.items()}
        for axis in 'xy':  # standardize format() location aliases
            if axis + 'spineloc' in kwargs:
                kwargs[axis + 'loc'] = kwargs.pop(axis + 'spineloc')
        return kwargs

    @docstring._snippet_manager
    def altx(self, **kwargs):
        """
        %(axes.altx)s
        """
        # Initialize axes
        # WARNING: We add axes as children for tight layout algorithm convenience and
        # to support eventual paradigm of arbitrarily many duplicates with spines
        # arranged in an edge stack. However this means all artists drawn there take
        # on zorder of their axes when drawn inside the "parent" (see Axes.draw()).
        # To restore matplotlib behavior, which draws "child" artists on top simply
        # because the axes was created after the "parent" one, use the inset_axes
        # zorder of 4 and make the background transparent.
        kwargs = self._parse_alt('x', **kwargs)
        kwargs.setdefault('yloc', 'neither')
        kwargs.setdefault('xloc', 'top')  # other locations follow by default
        kwargs.setdefault('grid', False)  # note xgrid=True would override this
        kwargs.setdefault('zorder', 4)
        kwargs.setdefault('autoscaley_on', self.get_autoscaley_on())

        # Initialize twin axes
        ax = self._make_twin_axes(
            sharey=self, number=False, autoshare=False, projection='cartesian', **kwargs
        )
        ax._altx_parent = self
        ax.patch.set_visible(False)
        ax.yaxis.set_visible(False)

        # Parent defaults
        kwformat = {'xloc': REVERSE_SIDE.get(kwargs['xloc'], None)}
        self.format(**kwformat)
        self.add_child_axes(ax)  # to facilitate tight layout
        self.figure._axstack.remove(ax)  # or gets drawn twice!

        return ax

    @docstring._snippet_manager
    def alty(self, **kwargs):
        """
        %(axes.alty)s
        """
        # Parse input args
        kwargs = self._parse_alt('y', **kwargs)
        kwargs.setdefault('xloc', 'neither')
        kwargs.setdefault('yloc', 'right')  # other locations follow by default
        kwargs.setdefault('grid', False)  # note ygrid=True would override this
        kwargs.setdefault('zorder', 4)
        kwargs.setdefault('autoscalex_on', self.get_autoscalex_on())

        # Initialize twin axes
        ax = self._make_twin_axes(
            sharex=self, number=False, autoshare=False, projection='cartesian', **kwargs
        )
        ax._alty_parent = self
        ax.patch.set_visible(False)
        ax.xaxis.set_visible(False)

        # Update parent axes
        kwformat = {'yloc': REVERSE_SIDE.get(kwargs['yloc'], None)}
        self.format(**kwformat)
        self.add_child_axes(ax)  # to facilitate tight layout
        self.figure._axstack.remove(ax)  # or gets drawn twice!

        return ax

    @docstring._snippet_manager
    def dualx(self, funcscale, **kwargs):
        """
        %(axes.dualx)s
        """
        # NOTE: Matplotlib 3.1 has a 'secondary axis' feature. For the time
        # being, our version is more robust (see FuncScale) and simpler, since
        # we do not create an entirely separate _SecondaryAxis class.
        ax = self.altx(**kwargs)
        ax._dualx_funcscale = funcscale
        ax._dualx_scale()
        return ax

    @docstring._snippet_manager
    def dualy(self, funcscale, **kwargs):
        """
        %(axes.dualy)s
        """
        ax = self.alty(**kwargs)
        ax._dualy_funcscale = funcscale
        ax._dualy_scale()
        return ax

    @docstring._snippet_manager
    def twinx(self, **kwargs):
        """
        %(axes.twinx)s
        """
        return self.alty(**kwargs)

    @docstring._snippet_manager
    def twiny(self, **kwargs):
        """
        %(axes.twiny)s
        """
        return self.altx(**kwargs)

    def draw(self, renderer=None, *args, **kwargs):
        # Perform extra post-processing steps
        # NOTE: In *principle* axis sharing application step goes here. But should
        # already be complete because auto_layout() (called by figure pre-processor)
        # has to run it before aligning labels. So this is harmless no-op.
        self._dualx_scale()
        self._dualy_scale()
        self._apply_axis_sharing()
        self._update_rotation('x')
        super().draw(renderer, *args, **kwargs)

    def get_tightbbox(self, renderer, *args, **kwargs):
        # Perform extra post-processing steps
        self._dualx_scale()
        self._dualy_scale()
        self._apply_axis_sharing()
        self._update_rotation('x')
        return super().get_tightbbox(renderer, *args, **kwargs)


# Apply signature obfuscation after storing previous signature
# NOTE: This is needed for __init__, altx, and alty
CartesianAxes._format_signatures[CartesianAxes] = inspect.signature(CartesianAxes.format)  # noqa: E501
CartesianAxes.format = docstring._obfuscate_kwargs(CartesianAxes.format)
