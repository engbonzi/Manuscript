# Mapping Socio-Spatial Polarization Across the 50 Largest U.S. Metropolitan Areas

**Author:** Dr. Mohamed Ahmed Abdelbaset Hamed  
*Department of Architectural Engineering, Faculty of Engineering at Mataria, Helwan University, Cairo 11718, Egypt*

## Overview
This repository archives the empirical dataset, official spatial autocorrelation reports, and reproduction scripts for the manuscript:  
**"Mapping Socio-Spatial Polarization Across the 50 Largest U.S. Metropolitan Areas: A Principal-Component, Environmental Orthogonality, and Spatial Autocorrelation Analysis"** *(Submitted to Computers, Environment and Urban Systems)*.

## Repository Contents
- `USSVI_50_MSAs_Full_Dataset.csv`: Complete empirical matrix for the 50 largest U.S. metropolitan statistical areas ($N = 50$, including San Juan, PR), containing:
  - 2017–2021 American Community Survey (ACS) 5-year estimates: Median Household Income (`Table B19013`), Gini Index (`Table B19083`), and Median Gross Rent as a Percentage of Household Income, GRAPI (`Table B25071`).
  - 2021 USFS/NLCD 30-meter Tree Canopy Cover percentage (`USGS/NLCD_RELEASES/2023_REL/TCC/v2023-5`, covering CONUS and OCONUS/Puerto Rico).
  - Principal Component Analysis (PCA) composite polarization scores (`USSVI_S3_Score`, Scenario S3: $\lambda_1 = 1.657$, $55.2\%$ variance explained, $\text{KMO} = 0.611$).
  - Official ArcGIS Pro polygon Local Getis-Ord $Gi^*$ outputs (`GiZ_ArcGIS`, `GiP_ArcGIS`, Benjamini–Hochberg FDR-adjusted `BH_q_ArcGIS`, and `Gi_Bin_ArcGIS` at $k = 8$).
- `MoransI_Result_16088_43712_.html`: Official ArcGIS Pro Global Moran's $I$ spatial autocorrelation report computed on CBSA polygons ($k = 8$ nearest neighbors, row-standardized, 3D chordal distances on NAD83; $I = 0.113295, E[I] = -0.020408, z = 2.329625, p = 0.019826$).
- `reproduce_USSVI_analysis.py`: Python script reproducing the descriptive statistics (Table 1), PCA eigenvalue spectra and factorability diagnostics comparing Scenario S3 vs. Scenario S2 (Tables 2 and 3), and Benjamini–Hochberg false discovery rate (FDR) local clustering adjustments (Table 6 and Appendix Table A1).

## License
Released under the MIT License.
