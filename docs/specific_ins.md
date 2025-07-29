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