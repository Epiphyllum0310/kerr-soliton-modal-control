# R425 source-data and code map

| Result | Location in the Zenodo upload ZIP |
|---|---|
| Main Figures 1-6: plotting scripts and inputs | `main_figures/` |
| Main Figures 1-6: exported plotting arrays | `main_figures/plotted_data/` |
| Supplementary Figures S1-S13 | `05_Source_Data_and_Code/Supplementary_Source_Data/` |
| Mapping of current S numbers to historical filenames | `05_Source_Data_and_Code/SUPPLEMENTARY_SOURCE_LINEAGE.json` |
| Additional bright-rate and dark-field response data | `05_Source_Data_and_Code/Additional_Response_Data/` |
| Selected dark control, trajectories, branches and solver modules | `05_Source_Data_and_Code/R410_analysis_and_inputs.zip` |
| Retained historical supplementary plotting context | `05_Source_Data_and_Code/Historical_SI_Plotting_Context/` |
| Supplementary Tables S1-S17, CSV and TeX cell copies | `02_Supplementary_Information/Editable_Tables/` |

The table files preserve the supplied values. Their scientific definitions
and captions are in the manuscript's Supplementary Information. Metadata,
normalizations, time steps and parameter meanings are documented by the
retained JSON files and original analysis README.

The supplementary lineage JSON retains its original R410 archive filename;
in this distribution that scientific content is provided as
`R410_analysis_and_inputs.zip`. The latter keeps analysis arrays, numerical
scripts, scientific modules and seeds, while excluding manuscript-building
scripts, editorial provenance files and redundant figure exports.

Historical filenames and numerical values are preserved. Some JSON and
script references describe the original workspace. That entire workspace,
including the full R409 dark eigenpair archive, is not included. The supplied
arrays permit inspection of the reported plotted data, but their presence
alone is not a claim of complete independent simulation reproducibility.
