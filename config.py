"""
config.py — SDI Tehran Pipeline
================================
Single source of truth for all paths, hyperparameters, and constants.
Import this at the top of every notebook:

    import sys; sys.path.insert(0, '..')
    from config import *

All path variables are strings. Update REPO_ROOT if your working directory differs.

Branch: experiment/landuse-join-fix
Purpose: rebuild the landuse column via corrected (overlap-based, not
nearest-centroid) spatial join, then re-run the pipeline downstream of
the fixed training set. NB01 (PCA/clustering) is untouched by this branch
and stays shared — its fit depends only on CH+INT columns, unaffected by
the landuse join fix.
"""

import os

# ─── Root ────────────────────────────────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# ─── Data directories (shared) ────────────────────────────────────────────────
DATA_DIR    = os.path.join(REPO_ROOT, "data")
OUTPUTS_DIR = os.path.join(REPO_ROOT, "data", "outputs")
MODELS_DIR  = os.path.join(REPO_ROOT, "models")   # scalers and PCA objects — shared, NB01 outputs

# ─── Input files (shared) ─────────────────────────────────────────────────────
SEGMENTS_GEOJSON   = os.path.join(DATA_DIR, "segments.geojson")
TRAINING_SET_CSV   = os.path.join(DATA_DIR, "training_set.csv")
PREDICTION_SET_CSV = os.path.join(DATA_DIR, "prediction_set.csv")
CATEGORY_KEYS_JSON = os.path.join(DATA_DIR, "category_keys.json")
LANDUSE_GPKG       = os.path.join(DATA_DIR, "landuse.gpkg")

# ─── Intermediate files (shared — NB01 outputs, not rerun on this branch) ────
SEGMENTS_PCA_CLUSTERED_CSV = os.path.join(OUTPUTS_DIR, "segments_pca_clustered.csv")
PCA_VARIANCE_JSON          = os.path.join(OUTPUTS_DIR, "pca_variance.json")

# ─── Serialised artefacts (shared — NB01 outputs, not rerun on this branch) ──
PCA_SCALER_PATH = os.path.join(MODELS_DIR, "pca_scaler.joblib")  # StandardScaler fitted on training set CH+INT
PCA_MODEL_PATH  = os.path.join(MODELS_DIR, "pca_model.joblib")   # PCA(3) fitted on training set CH+INT

# ─── GCS ─────────────────────────────────────────────────────────────────────
GCS_BUCKET      = "sdi-tehran-assets"
GCS_OUTPUT_PATH = "data/outputs/experiments/landuse-join-fix"
GCS_PROJECT     = "sdi-tehran-v1"

# ─── Local experiment isolation ──────────────────────────────────────────────
# Everything below is isolated to this branch. Single source path
# (GCS_OUTPUT_PATH) controls both local and cloud destinations.
EXPERIMENT_OUTPUTS_DIR = os.path.join(REPO_ROOT, GCS_OUTPUT_PATH)
os.makedirs(EXPERIMENT_OUTPUTS_DIR, exist_ok=True)

EXPERIMENT_MODELS_DIR = os.path.join(EXPERIMENT_OUTPUTS_DIR, "models")

# NB00 outputs — landuse join rebuild
LANDUSE_JOINED_CSV     = os.path.join(EXPERIMENT_OUTPUTS_DIR, "landuse_joined.csv")
TRAINING_SET_FIXED_CSV = os.path.join(EXPERIMENT_OUTPUTS_DIR, "training_set_landuse_fixed.csv")

# NB02 outputs
TRAINED_MODELS_DIR = os.path.join(EXPERIMENT_OUTPUTS_DIR, "trained_models")
EVAL_DIR           = os.path.join(EXPERIMENT_OUTPUTS_DIR, "evaluation_reports")
MODEL_SCALER_PATH  = os.path.join(EXPERIMENT_MODELS_DIR, "model_scaler.joblib")  # StandardScaler fitted on PC1-3, training set only
MODEL_SCORES_JSON  = os.path.join(EXPERIMENT_OUTPUTS_DIR, "model_scores.json")

# NB03 outputs
PREDICTIONS_JOINED_CSV = os.path.join(EXPERIMENT_OUTPUTS_DIR, "predictions_joined.csv")

# NB04 outputs
DISPARITY_INDEX_CSV = os.path.join(EXPERIMENT_OUTPUTS_DIR, "disparity_index.csv")

# NB05 outputs
HEX_GEOJSON         = os.path.join(EXPERIMENT_OUTPUTS_DIR, "hex.geojson")
CLASSIFICATION_JSON = os.path.join(EXPERIMENT_OUTPUTS_DIR, "classification.json")

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
assert len(PCA_INPUT_COLS) == 16, f"Expected 16 PCA input cols, got {len(PCA_INPUT_COLS)}"

# ─── Target attributes ───────────────────────────────────────────────────────
CATEGORICAL_TARGETS = ["policy_era", "dilap_index", "landuse"]
CONTINUOUS_TARGETS  = ["mean_area", "perimeter", "mean_pop"]
TARGET_ATTRS         = CATEGORICAL_TARGETS + CONTINUOUS_TARGETS

# ─── Model hyperparameters ───────────────────────────────────────────────────
RANDOM_STATE      = 42
TEST_SIZE         = 0.2
MLP_HIDDEN_LAYERS = (100, 50)
MLP_MAX_ITER      = 500
PCA_N_COMPONENTS  = 3
N_CLUSTERS        = 12

# ─── H3 ──────────────────────────────────────────────────────────────────────
H3_RESOLUTION        = 8
MIN_SEGMENTS_PER_HEX = 1

# ─── SDI classification ───────────────────────────────────────────────────────
N_SDI_CLASSES = 5

# ─── CRS ─────────────────────────────────────────────────────────────────────
CRS_PROJECTED  = "EPSG:32639"   # UTM Zone 39N — Tehran
CRS_GEOGRAPHIC = "EPSG:4326"    # WGS84 — required for H3

# ─── Ensure shared + experiment output directories exist ────────────────────
for _dir in [OUTPUTS_DIR, MODELS_DIR, EXPERIMENT_OUTPUTS_DIR, EXPERIMENT_MODELS_DIR,
             TRAINED_MODELS_DIR, EVAL_DIR]:
    os.makedirs(_dir, exist_ok=True)