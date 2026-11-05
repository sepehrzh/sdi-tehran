import pytest
from sdi import schema

def test_ch_and_int_cols_have_one_column_per_radius():
    assert len(schema.CH_COLS) == len(schema.RADII), f"Expected {len(schema.RADII)} CH cols, got {len(schema.CH_COLS)}"
    assert len(schema.INT_COLS) == len(schema.RADII), f"Expected {len(schema.RADII)} INT cols, got {len(schema.INT_COLS)}"


def test_pca_input_cols():
    assert len(schema.PCA_INPUT_COLS) == 16, f"Expected 16 PCA input cols, got {len(schema.PCA_INPUT_COLS)}"
    assert schema.PCA_INPUT_COLS[0] == "CH_400", f"Expected first PCA input col to be 'CH_400', got {schema.PCA_INPUT_COLS[0]}"
    assert schema.PCA_INPUT_COLS[-1] == "INT_40k", f"Expected last PCA input col to be 'INT_40k', got {schema.PCA_INPUT_COLS[-1]}"


def test_pca_input_clustering_features_match():
    assert schema.PCA_INPUT_COLS == schema.CLUSTERING_FEATURES, "PCA input cols and clustering features should match"


def test_radii_value_order():
    expected_order = ["400", "800", "1200", "2000", "5000", "10k", "20k", "40k"]
    assert schema.RADII == expected_order, f"Expected radii order {expected_order}, got {schema.RADII}"


@pytest.mark.parametrize("name", ["RADII", "CH_COLS", "INT_COLS", "PCA_INPUT_COLS", "CLUSTERING_FEATURES"])
def test_no_duplicates(name):
    cols = getattr(schema, name)
    assert len(cols) == len(set(cols)), f"Duplicate values found in {name}"