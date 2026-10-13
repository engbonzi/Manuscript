# Mapping Socio-Spatial Polarization Across the 50 Largest U.S. Metropolitan Areas

**Author:** Dr. Mohamed Ahmed Abdelbaset Hamed  
*Department of Architectural Engineering, Faculty of Engineering at Mataria, Helwan University, Cairo 11718, Egypt*

## Overview
This repository archives the empirical dataset and spatial autocorrelation outputs for the manuscript:  
**"Mapping Socio-Spatial Polarization Across the 50 Largest U.S. Metropolitan Areas: A Principal-Component, Environmental Orthogonality, and Spatial Autocorrelation Analysis"** (*Computers, Environment and Urban Systems*).

## Repository Contents
- `USSVI_50_MSAs_Full_Dataset.csv`: Complete empirical matrix for the 50 largest U.S. MSAs (2017–2021 ACS Tables B19013, B19083, B25071; 2021 NLCD 30m Tree Canopy Cover; PCA-derived USSVI scores under Scenario S3; and ArcGIS Pro polygon Getis-Ord Gi* statistics `GiZ_ArcGIS`, `GiP_ArcGIS`, `BH_q_ArcGIS`, `Gi_Bin_ArcGIS`).
- `MoransI_Result_16088_43712_.html`: Official ArcGIS Pro Global Moran's I report ($k = 8$ nearest neighbors, row-standardized, chordal distances; $I = 0.113295, z = 2.329625, p = 0.019826$).

## License
Released under the MIT License.
