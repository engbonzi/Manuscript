"""
Reproducibility Script for:
"Mapping Socio-Spatial Polarization Across the 50 Largest U.S. Metropolitan Areas:
A Principal-Component, Environmental Orthogonality, and Spatial Autocorrelation Analysis"
Author: Dr. Mohamed Ahmed Abdelbaset Hamed (Helwan University)
License: MIT
"""

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, pearsonr


def compute_kmo_and_bartlett(Z: np.ndarray):
    """Compute Kaiser-Meyer-Olkin (KMO) measure and Bartlett's test of sphericity."""
    n, p = Z.shape
    R = np.corrcoef(Z, rowvar=False)
    invR = np.linalg.inv(R)
    D = np.diag(1.0 / np.sqrt(np.diag(invR)))
    P = -D @ invR @ D
    np.fill_diagonal(P, 0.0)
    R_off = R.copy()
    np.fill_diagonal(R_off, 0.0)
    kmo = np.sum(R_off**2) / (np.sum(R_off**2) + np.sum(P**2))
    detR = np.linalg.det(R)
    chi_sq = -(n - 1 - (2 * p + 5) / 6.0) * np.log(detR)
    dof = int(p * (p - 1) / 2)
    p_val = chi2.sf(chi_sq, dof)
    return kmo, chi_sq, dof, p_val, R


def run_pca_scenario(df: pd.DataFrame, cols: list, name: str):
    """Run sample-standardized PCA on correlation matrix R and orient PC1 positively on Gini."""
    Z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=1)
    kmo, chi_sq, dof, p_val, R = compute_kmo_and_bartlett(Z.values)
    eigvals, eigvecs = np.linalg.eigh(R)
    idx = np.argsort(eigvals)[::-1]
    eigvals, eigvecs = eigvals[idx], eigvecs[:, idx]

    gini_idx = cols.index("Gini_Index")
    if eigvecs[gini_idx, 0] < 0:
        eigvecs[:, 0] *= -1
    if len(cols) == 4 and eigvecs[cols.index("NLCD_2021_Tree_Canopy_Pct"), 1] < 0:
        eigvecs[:, 1] *= -1

    print(f"\n=== {name} ===")
    print(f"KMO = {kmo:.3f} | Bartlett chi2({dof}) = {chi_sq:.2f}, p = {p_val:.4f}")
    print("Eigenvalues:", np.round(eigvals, 3))
    print("Variance Explained (%):", np.round(eigvals / len(cols) * 100, 1))
    print("PC1 Loadings:", dict(zip(cols, np.round(eigvecs[:, 0], 3))))
    if len(cols) == 4:
        print("PC2 Loadings:", dict(zip(cols, np.round(eigvecs[:, 1], 3))))
    return Z.values @ eigvecs[:, 0]


if __name__ == "__main__":
    df = pd.read_csv("USSVI_50_MSAs_Full_Dataset.csv")
    print(f"Loaded N = {len(df)} Metropolitan Statistical Areas.")

    # 1. Reproduce Table 1: Descriptive Statistics & Bivariate Correlations
    cols_all = [
        "Median_Income_USD",
        "Gini_Index",
        "Rent_Burden_GRAPI_Pct",
        "NLCD_2021_Tree_Canopy_Pct",
    ]
    print("\n--- Table 1: Descriptive Statistics ---")
    for c in cols_all:
        print(
            f"{c}: Mean = {df[c].mean():.3f}, SD = {df[c].std(ddof=1):.3f}, "
            f"Median = {df[c].median():.3f}, Min = {df[c].min():.3f}, Max = {df[c].max():.3f}"
        )

    # 2. Reproduce Tables 2 & 3: PCA Diagnostics (Scenario S3 vs. Scenario S2)
    ussvi_s3 = run_pca_scenario(
        df,
        ["Median_Income_USD", "Gini_Index", "Rent_Burden_GRAPI_Pct"],
        "Scenario S3 (3 ACS Indicators)",
    )
    _ = run_pca_scenario(
        df,
        cols_all,
        "Scenario S2 (3 ACS Indicators + NLCD 2021 Tree Canopy)",
    )

    r_tree, p_tree = pearsonr(df["NLCD_2021_Tree_Canopy_Pct"], ussvi_s3)
    print(f"\nCorrelation (Tree Canopy vs. USSVI S3): r = {r_tree:+.3f}, p = {p_tree:.4f}")

    # 3. Verify Benjamini-Hochberg FDR q-values on ArcGIS Polygon Gi* p-values (Table 6 & Table A1)
    p_vals = df["GiP_ArcGIS"].values
    m = len(p_vals)
    order = np.argsort(p_vals)
    ranked_p = p_vals[order]
    q_raw = ranked_p * m / np.arange(1, m + 1)
    q_adj = np.minimum.accumulate(q_raw[::-1])[::-1]
    df["BH_q_reproduced"] = np.empty(m)
    df.loc[order, "BH_q_reproduced"] = np.round(q_adj, 4)

    hotspots = df[df["Gi_Bin_ArcGIS"] == 2][
        ["Rank", "CBSA", "Metropolitan_Statistical_Area", "USSVI_S3_Score", "GiZ_ArcGIS", "GiP_ArcGIS", "BH_q_ArcGIS"]
    ]
    print("\n--- Table 6: Nominal Gi* Hot Spots (ArcGIS Polygon Export, k = 8) ---")
    print(hotspots.to_string(index=False))
