Catchmentwide Erosion Rate Calculator for in situ cosmogenic nuclides 
---------------------------------------------------------------------

This calculator processes geospatial data (digital elevation model, catchment
outline and other) to extract hypsometry statistics of the catchment and
determine a cosmogenic nuclide catchmentwide erosion rate. It uses the online
erosion rate calculator by Greg Balco (e.g. http://stoneage.hzdr.de/) to
calculate cosmogenic nuclide production.

The method currently works for in situ Be-10 and Al-26 data and is considered
robust for catchments up to approx. 600 km x 600 km; for larger catchments
the effect of latitude on cosmogenic production may become significant.

Citation
--------

The software is described in:

Stübner, K., Balco, G., and Schmeisser, N. (in review). Calculating catchmentwide erosion rates using an existing online calculator. *Radiocarbon*. 

Installation and Usage
----------------------

This software has been developed on python 3.9 and needs the packages
`xarray`, `rasterio`, `fiona` and `pyproj` as well as several other common
python packages. Example scripts are provided as `jupyter` notebooks.

This release has two folders: The folder `riversand` has the
actual code. The folder `example_scripts` is an example of what your project might look
like. It has two jupyter notebooks [`quickstart.ipynb`](https://github.com/kstueb/catchmentwide_erosion_rates/blob/main/riversand/example_scripts/quickstart.ipynb) and
[`step-by-step.ipynb`](https://github.com/kstueb/catchmentwide_erosion_rates/blob/main/riversand/example_scripts/step-by-step.ipynb)
and a folder `test_data` with example data.


License
-------

Copyright (C) 2023 Konstanze Stübner <kstueb@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
