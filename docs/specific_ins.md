# Specific instructions and workarounds

In case of having errors caused by mpl_toolkits and incompatible/multiple versions of matplotlib I have found the following workaround:

---
[text](https://github.com/matplotlib/matplotlib/issues/26827)

or the following steps to fix it:

> sudo apt remove python3-matplotlib

Uninstalling the previously installed Matplotlib using pip:

> pip uninstall matplotlib

Reinstalling Matplotlib via pip:

> pip install matplotlib

## Number in Front of the Disks Names

The number displayed before each disk name indicates its **flux ranking** relative to the entire set you selected for plotting. You can define the flux ranking in your input, but the numbering in the saved files will reflect this ranking **only** if you choose to plot the **entire sample**.

For example, if you generate a PDF plot starting from disk index `6`, that disk corresponds to the **sixth lowest-flux** object in the full set. However, it will still be saved as `000_diskname`, since the numbering in the saved files is always based on the subset being plotted, not the full ranking, **unless** the full sample is used.