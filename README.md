# SISEC MUS Preview-Generator

Script to generate 30s previews from SISEC MUS Estimates, by trimming using a
[predefined cut-list](data/previews.csv).

## Usage

1. Install the python [dsdtools](http://github.com/faroit/dsdtools) package

```
pip install dsdtools
```

2. Trim estimates by running

```
python trim_estimates.py Your_Estimates_Dir/ Output_Dir/
```

where `Your_Estimates_Dir` is the source files that includes your SISEC MUS
results and `Output_Dir` is a directory that will be created in order to render
the trimmed 30s previews.

To run this script, make sure that you also have the full DSD100 Dataset available
by set the DSD_PATH (Unix) `export DSD_PATH=/Full/Path/to/DSD100` or adjust the
`root_dir` variable in the `trim_estimates.py` script.
