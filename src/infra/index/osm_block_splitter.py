import networkx as nx
import osmnx as ox
from pyproj import Transformer
from shapely import STRtree, points

from domain.journey.position import Position


class OsmBlockSplitter:
    """ Divide a rota pelos trechos de rua entre duas interseções
    (quarteirões) da malha viária do OpenStreetMap. Cada ponto é
    associado à aresta mais próxima, e pontos da mesma aresta formam
    um único segmento, mesmo que venham de passagens diferentes. """

    def __init__(self, graph: nx.MultiGraph):
        edges = ox.convert.graph_to_gdfs(graph, nodes=False, fill_edge_geometry=True)
        self._edge_ids = list(edges.index)
        self._tree = STRtree(edges.geometry.values)
        self._to_graph_crs = Transformer.from_crs(
            "EPSG:4326", graph.graph["crs"], always_xy=True
        )

    def __call__(self, route: list[Position]) -> list[list[Position]]:
        if len(route) == 0:
            return []

        xs, ys = self._to_graph_crs.transform(
            [position.longitude for position in route],
            [position.latitude for position in route],
        )
        route_indexes, edge_indexes = self._tree.query_nearest(
            points(xs, ys), all_matches=False
        )

        segments_by_edge: dict[tuple, list[Position]] = {}
        for route_index, edge_index in sorted(zip(route_indexes, edge_indexes)):
            edge_id = self._edge_ids[edge_index]
            segments_by_edge.setdefault(edge_id, []).append(route[route_index])

        return list(segments_by_edge.values())


def load_osm_block_splitter(path: str) -> OsmBlockSplitter:
    return OsmBlockSplitter(ox.load_graphml(path))
