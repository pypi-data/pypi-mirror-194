# DoPe

[**Do**uglas-**Pe**ucker][1] line simplification (data reduction).

Reduces the number of points in a two-dimensional dataset, while preserving its most striking features.

The resulting dataset is a subset of the original dataset.

Although line simplification is typically used for geographical data, e.g. when zooming a digital map (see e.g. [Django's GEOSGeometry.simplify()][4] based on [GEOS][5]),
this type of algorithm can also be applied to general data reduction problems, as an alternative (or addition) to conventional filtering or subsampling. Some examples:
- creating miniature data plots
- pre-processing time-series data for feature detection (e.g. peak detection) 

 

## Installation

Normal installation:

```pip install dopelines```

With plot support (adds `matplotlib`):

```pip install dopelines[plot]```

With development tools:

```pip install dopelines[dev]```

Note: The PyPi project is called `dopelines` instead of `dope`, because PyPi would not let us create a project named `dope`, even though the name appears to be available. 

## Example

```python
from dope import DoPeR

data_original = [
    [0, 0], [1, -1], [2, 2], [3, 0], [4, 0], [5, -1], [6, 1], [7, 0]
]

dp = DoPeR(data=data_original)

# use tolerance threshold (i.e. max. error w.r.t. normalized data)
data_simplified_eps = dp.simplify(tolerance=0.2)

# compare original data and simplified data in a plot
dp.plot()

# or use maximum recursion depth
data_simplified_depth = dp.simplify(max_depth=2)

```

![Example line simplification plot.][3]

Also see examples in [tests][2].

## Limitations

Currently we only offer a recursive implementation (depth-first), which is intuitive, but may not be the most efficient solution.
An iterative implementation is in the works (breadth-first).

## References:

[Douglas DH, Peucker TK. *Algorithms for the reduction of the number of points required to represent a digitized line or its caricature.*
Cartographica: the international journal for geographic information and geovisualization. 1973 Dec 1;10(2):112-22.][1]

[1]: https://doi.org/10.3138/FM57-6770-U75U-7727
[2]: https://github.com/dennisvang/dope/tree/main/tests
[3]: https://github.com/dennisvang/dope/blob/main/pdf/dope-example.png
[4]: https://docs.djangoproject.com/en/stable/ref/contrib/gis/geos/#django.contrib.gis.geos.GEOSGeometry.simplify
[5]: https://libgeos.org/doxygen/namespacegeos_1_1simplify.html
