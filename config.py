"""
config.py — SDI Tehran Pipeline
================================
Single source of truth for all paths, hyperparameters, and constants.
Import this at the top of every notebook:

    import sys; sys.path.insert(0, '..')
    from config import *

All path variables are strings. Update REPO_ROOT if your working directory differs.
"""

import os

# ─── Root ────────────────────────────────────────────────────────────────────
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# ─── Data directories ────────────────────────────────────────────────────────
DATA_DIR            = os.path.join(REPO_ROOT, "data")
OUTPUTS_DIR         = os.path.join(REPO_ROOT, "data", "outputs")
MODELS_DIR          = os.path.join(REPO_ROOT, "models")           # scalers and PCA objects
TRAINED_MODELS_DIR  = os.path.join(REPO_ROOT, "trained_models")  # MLP classifiers and regressor
EVAL_DIR            = os.path.join(REPO_ROOT, "evaluation_reports")

# ─── Input files ─────────────────────────────────────────────────────────────
SEGMENTS_GEOJSON    = os.path.join(DATA_DIR, "segments.geojson")
TRAINING_SET_CSV    = os.path.join(DATA_DIR, "training_set.csv")
PREDICTION_SET_CSV  = os.path.join(DATA_DIR, "prediction_set.csv")
CATEGORY_KEYS_JSON  = os.path.join(DATA_DIR, "category_keys.json")

# ─── Intermediate files ───────────────────────────────────────────────────────
SEGMENTS_PCA_CLUSTERED_CSV = os.path.join(OUTPUTS_DIR, "segments_pca_clustered.csv")
PCA_VARIANCE_JSON          = os.path.join(OUTPUTS_DIR, "pca_variance.json")
PREDICTIONS_JOINED_CSV     = os.path.join(OUTPUTS_DIR, "predictions_joined.csv")
MODEL_SCORES_JSON          = os.path.join(DATA_DIR, "model_scores.json")

# ─── Serialised artefacts ────────────────────────────────────────────────────
PCA_SCALER_PATH   = os.path.join(MODELS_DIR, "pca_scaler.joblib")    # StandardScaler fitted on training set CH+INT
PCA_MODEL_PATH    = os.path.join(MODELS_DIR, "pca_model.joblib")     # PCA(3) fitted on training set CH+INT
MODEL_SCALER_PATH = os.path.join(MODELS_DIR, "model_scaler.joblib")  # StandardScaler fitted on PC1-3, training set only

# ─── Final outputs ────────────────────────────────────────────────────────────
DISPARITY_INDEX_CSV  = os.path.join(OUTPUTS_DIR, "disparity_index.csv")
HEX_GEOJSON          = os.path.join(OUTPUTS_DIR, "hex.geojson")
CLASSIFICATION_JSON  = os.path.join(OUTPUTS_DIR, "classification.json")

# ─── GCS ─────────────────────────────────────────────────────────────────────
GCS_BUCKET       = "sdi-tehran-assets"
# Branch-isolated by default so this experiment can never silently overwrite
# the live production path the public dashboard fetches client-side (see
# phase 7a handoff, "Critical infrastructure note: GCS output isolation").
# Override with SDI_EXPERIMENT_OUTPUT_PATH for a different run if needed;
# falling back to "data/outputs" is NOT the default on this branch on purpose.
GCS_OUTPUT_PATH  = os.environ.get("SDI_EXPERIMENT_OUTPUT_PATH", "data/outputs/experiments/class-weighting")
GCS_PROJECT = "sdi-tehran-v1"

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
CATEGORICAL_TARGETS  = ["policy_era", "dilap_index", "landuse"]
CONTINUOUS_TARGETS   = ["mean_area", "perimeter", "mean_pop"]
TARGET_ATTRS         = CATEGORICAL_TARGETS + CONTINUOUS_TARGETS

# ─── Model hyperparameters ───────────────────────────────────────────────────
RANDOM_STATE       = 42
TEST_SIZE          = 0.2
MLP_HIDDEN_LAYERS  = (100, 50)
MLP_MAX_ITER       = 500
PCA_N_COMPONENTS   = 3
N_CLUSTERS         = 12

# Candidate categorical classifiers (experiment/class-weighting) — both
# trained with explicit sample_weight, see NB02 Section 3 methodology note.
RF_N_ESTIMATORS    = 300
RF_MAX_DEPTH       = None
HGB_MAX_ITER       = 300
HGB_LEARNING_RATE  = 0.1
HGB_MAX_DEPTH      = None

# ─── H3 ──────────────────────────────────────────────────────────────────────
H3_RESOLUTION        = 8
MIN_SEGMENTS_PER_HEX = 1

# ─── SDI classification ───────────────────────────────────────────────────────
N_SDI_CLASSES = 5

# ─── CRS ─────────────────────────────────────────────────────────────────────
CRS_PROJECTED  = "EPSG:32639"   # UTM Zone 39N — Tehran
CRS_GEOGRAPHIC = "EPSG:4326"   # WGS84 — required for H3

# ─── Ensure output directories exist ─────────────────────────────────────────
for _dir in [OUTPUTS_DIR, MODELS_DIR, TRAINED_MODELS_DIR, EVAL_DIR]:
    os.makedirs(_dir, exist_ok=True)