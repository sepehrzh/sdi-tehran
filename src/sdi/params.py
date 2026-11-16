from dataclasses import dataclass


@dataclass(frozen=True)
class ModelParams:
    random_state: int = 42
    test_size: float = 0.2
    mlp_hidden_layers: tuple[int, ...] = (100, 50)
    mlp_max_iter: int = 500
    pca_n_components: int = 3
    n_clusters: int = 12

@dataclass(frozen=True)
class H3Params:
    resolution: int = 8
    min_segments_per_hex: int = 1

@dataclass(frozen=True)
class SDIParams:
    n_classes: int = 5