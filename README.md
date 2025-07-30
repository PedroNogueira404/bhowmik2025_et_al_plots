# Plots Builder

Automated pipeline to convert input data tables, FITS files, and radial profiles into:

- Individual plots of observations and models  
- LaTeX-ready figure grids with consistent formatting and grouping  

---

### 📌 Example Output

#### Individual Plot Example  
![image_example](/src/bhowmik2025plots/imagetest.png)

#### Grid Example (LaTeX output)  
![grid_example](/src/bhowmik2025plots/grid_example.png)

---

## 📄 Description

This tool was developed for generating plots for **ALMA Band 8**, high-resolution protoplanetary disks. It was created for **Bhowmik et al. 2025**, part of the **ODISEA** series.

> 📚 The paper will be linked here once published.

The pipeline includes:

- Plot generation for individual disks
    - Three panel format: data, model and radial profile

- Sorting/grouping of figures by disk properties

- Automatic LaTeX `.tex` files for 2-column figure grids


---

## 🧠 Core Modules

These are the main Python modules:

1. `table_creator.py` — prepares and reads the metadata  
2. `plotter_w_decorators.py` — generates plots with relevant visual info  
3. `images_latex.py` — creates LaTeX code with grids of plots  

All modules can be run in sequence via `main.py`.

---

## 🗂️ Project Structure

```text
.
├── docs
├── src
│   └── bhowmik2025plots
│       ├── input_files
│       │   ├── fits_files
│       │   ├── frank_profiles
|       |   ├──*table.csv*
|       |   └── *gap_ring_infl_pt.csv*
│       ├── outputs
│       │   ├── generated_figures_for_tex
│       │   ├── pdf
│       │   └── png
│       └── utils
│       ├── *table_creator.py*
│       ├── *plotter_w_decorators.py*
│       ├── *images_latex.py*
│       └── *main.py*
├── tests
│   ├── table_creator.ipynb
│   ├── plotter.ipynb
│   └── images_latex.ipynb
```

---

> ⚠️ Input and output files are confidential and will be made available **after the paper is published**.


> 📚 Module instructions and dataset-specific behavior are detailed in the `docs/` folder.

---

## ⚙️ Plot Logic & Behavior

- **Plot order**:
  - If `png`: follows the index from `table.csv` 
  - If `pdf`: sorts by flux (low → high)

  > Example: Index `100`  
  > - In PNG mode → `ODISEA_C4_130`  
  > - In PDF mode → `RA162813.74` (highest flux) of this sample

- **Plot Settings**:
  - Data: `vmin = rms_data`

  - Models:

    - Most: `vmin = 5%` of peak

    - Binaries: `10%`

    - Special cases: `1%` (e.g., `C4_41`, `C4_143`, `C4_51`)

  - Disks in Stage 0 or 1: Gaussian smoothing applied  
    ```python
    gaussian_filter(data, sigma=0, mode="nearest")
    ```

  - `ODISEA_C4_094a` and `094b`: special treatment for model zoom  
    (black padding added where model is smaller than zoom window)

---

## 🖼️ LaTeX Output Notes

- LaTeX `.tex` files are **only generated** if plots were saved as **PDF** (`dpi=600`).

  - Ensures scalability and high quality for grids.

- PNGs (`dpi=100`) are created **only** for debugging or quick inspection.

- If `images_latex.py` is executed **without** prior PDF generation, it will fail.

---

## 🧾 Required LaTeX Preamble

Ensure the following packages and commands are present in your LaTeX preamble:

```latex
\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}
\newcommand{\vrulesep}{\unskip \ \vrule\ }
\newcommand{\hrulesep}{\unskip \ \hrule\ }
