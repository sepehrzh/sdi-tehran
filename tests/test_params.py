from dataclasses import FrozenInstanceError
import pytest
from sdi.params import ModelParams, H3Params, SDIParams



def test_model_params_defaults():
    p = ModelParams()
    assert p.random_state == 42
    assert p.test_size == 0.2
    assert p.mlp_hidden_layers == (100, 50)
    assert p.mlp_max_iter == 500
    assert p.pca_n_components == 3
    assert p.n_clusters == 12

    h = H3Params()
    assert h.resolution == 8
    assert h.min_segments_per_hex == 1
    
    s = SDIParams()
    assert s.n_classes == 5



def test_model_params_immutable():
    p = ModelParams()
    with pytest.raises(FrozenInstanceError):
        p.n_clusters = 5