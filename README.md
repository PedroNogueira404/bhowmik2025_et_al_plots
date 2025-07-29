



Latex Figures text are just generated when the images were saved as PDF.

The reason is that PDF images are better scalable, and keep the quality when reduced in small grids (they were set with dpi=600 as default). Therefore the images_latex.py will break run directly and no pdf were generated beforehand.

The png images are JUST created for control and debugging, with dpi=100

Be sure to add these packages and commands in your preamble!!

\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}
\newcommand{\vrulesep}{\unskip \ \vrule\ }
\newcommand{\hrulesep}{\unskip \ \hrule\ }