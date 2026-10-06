import os
from functools import lru_cache
from pathlib import Path

import dotenv

from domain.index.segmentation import (
    RouteSplitter,
    split_by_accumulated_length,
    split_by_distance_from_head,
)
from infra.index.osm_block_splitter import load_osm_block_splitter

dotenv.load_dotenv()


def get_route_splitter() -> RouteSplitter:
    """
    Returns the route splitting strategy selected by SEGMENTATION_STRATEGY:
    'accumulated' (default), 'head_distance' or 'osm_blocks'.
    """
    strategy = os.getenv('SEGMENTATION_STRATEGY', 'accumulated')
    if strategy == 'accumulated':
        return split_by_accumulated_length
    if strategy == 'head_distance':
        return split_by_distance_from_head
    if strategy == 'osm_blocks':
        return _load_osm_block_splitter(os.getenv('ROAD_NETWORK_PATH', 'data/road_network.graphml'))
    raise RuntimeError(f"SEGMENTATION_STRATEGY desconhecida: {strategy!r}")


@lru_cache
def _load_osm_block_splitter(path: str) -> RouteSplitter:
    if not Path(path).is_file():
        raise RuntimeError(
            f"Malha viária não encontrada em {path!r}. "
            "Gere-a com scripts/download_road_network.py ou ajuste ROAD_NETWORK_PATH."
        )
    return load_osm_block_splitter(path)
