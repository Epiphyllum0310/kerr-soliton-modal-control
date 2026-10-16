# Modal prediction and recovery control of periodically driven Kerr solitons

Authors: Yifan Xie and Hanzhong Wu. Research release: R425.

Repository: https://github.com/Epiphyllum0310/kerr-soliton-modal-control

This repository provides the Python scripts and inputs used to generate the
six main figures. The numerical source data and selected supplementary
analyses are prepared as a separate Zenodo archive. The archive DOI will be
added here after publication of the repository record; no public DOI has yet
been assigned to this local draft.

## Main-figure workflow

The `main_figures/` directory contains the original plotting scripts,
their numerical inputs in `data/`, additional inputs in `figure_sources/data/`,
and dependency information. These scripts redraw the figures from saved
arrays; they do not rerun the underlying nonlinear simulations.

With 64-bit Python, run from `main_figures/`:

```powershell
python -m pip install -r requirements-tested.txt
python rebuild_figures.py
```

To draw only Figure 4:

```powershell
python rebuild_figures.py 4
```

Outputs are written to `figures/`, `preview_after/` and `plotted_data/`.
The retained dependency pins describe the environment reported by the
original figure package. Windows Arial and Symbol fonts were used in the
original rendering; other font environments may change text layout.
This upload preparation did not rerun the numerical solvers or certify a
new cross-platform rendering environment.

## Research archive and source mapping

See `SOURCE_MAP.md` for the data families, supplementary figure mapping,
table data, and the limits of the archived workflows.

The planned Zenodo record contains both data and code, including a copy of
the main-figure scripts in this repository. The public DOI should be added
to this README and `CITATION.cff` after the Zenodo record is published.

The complete historical nonlinear workspace and the full R409 dark
eigenpair archive are not included. Historical supplementary scripts retain
some original path assumptions. The archive does not claim to reproduce
every result from first principles or independently rebuild all thirteen
supplementary figure PDFs.

## Citation and licensing

Use the author names, title and version in `CITATION.cff`; add the registered
Zenodo DOI when it becomes available. Do not use the journal article DOI
as the dataset DOI.

Original code: MIT (`LICENSE`). Research data: CC BY 4.0
(`DATA_LICENSE.md`). Third-party dependencies retain their own licences.
