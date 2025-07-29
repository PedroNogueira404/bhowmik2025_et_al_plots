

The range of files chosen follows the order of indexes if chosen pngs as outputs (set in table.csv and full_table.csv) but follows the sequence of fluxes, lower to higher if pdf output is set. 

So, for example, if chosen index 100, it will correspond to Odisea_c4_130 disk if png output, but RA162813.74 disk if pdf output (the higher flux in my sequence of 101 disks, starting from index 0).

-----------------------------------------------------
Important plotted info:

The data plots were set with vmin = rms_data
Model plots, with 5% to all but binaries (that had 10%) and ODISEA_C4_41, ODISEA_C4_143 and ODISEA_C4_51 which had 1% of the maximum flux. The values were normalized but kept consistent in the radial profile plots.

For disks in stage 0 and 1, a gaussian smooth was applied (gaussian_filter(data_data, sigma=0, mode="nearest"))

The disks Odiseas_c4_094a and b had models specially plotted, filling the extra space in the plot with black since their zooms were larger than the original model size

-----------------------------------------------------

Latex Figures text are just generated when the images were saved as PDF.

The reason is that PDF images are better scalable, and keep the quality when reduced in small grids (they were set with dpi=600 as default). Therefore the images_latex.py will break run directly and no pdf were generated beforehand.

The png images are JUST created for control and debugging, with dpi=100

Be sure to add these packages and commands in your preamble!!

\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}
\newcommand{\vrulesep}{\unskip \ \vrule\ }
\newcommand{\hrulesep}{\unskip \ \hrule\ }