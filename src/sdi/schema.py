# ─── Segment ID column ───────────────────────────────────────────────────────
SEG_ID_COL = "Depthmap_R"

# ─── Feature definitions ─────────────────────────────────────────────────────
# Non-normalised Choice and Integration only.
# Global radius (Rn) columns are absent from this dataset — radii start at 400.
# Radii: 400, 800, 1200, 2000, 5000, 10k, 20k, 40k (8 radii, no global Rn).

RADII = ["400", "800", "1200", "2000", "5000", "10k", "20k", "40k"]

CH_COLS  = [f"CH_{r}"  for r in RADII]   # Choice (non-normalised)  — 8 columns
INT_COLS = [f"INT_{r}" for r in RADII]   # Integration (non-normalised) — 8 columns

# PCA input: CH + INT only (16 columns). Global CH/INT absent from dataset.
# Theoretical rationale: CH and INT capture movement potential and structural
# hierarchy independently. NC and TD are excluded on methodological grounds.
PCA_INPUT_COLS      = CH_COLS + INT_COLS   # 16 columns — used in NB01 PCA fit
CLUSTERING_FEATURES = CH_COLS + INT_COLS   # 16 columns — used in NB01 KMeans

# ─── Target attributes ───────────────────────────────────────────────────────
CATEGORICAL_TARGETS = ["policy_era", "dilap_index", "landuse"]
CONTINUOUS_TARGETS  = ["mean_area", "perimeter", "mean_pop"]

# ─── CRS ─────────────────────────────────────────────────────────────────────
CRS_PROJECTED  = "EPSG:32639"   # UTM Zone 39N — Tehran
CRS_GEOGRAPHIC = "EPSG:4326"    # WGS84 — required for H3