from datetime import datetime

import networkx as nx
from pyproj import Transformer

from domain.journey.position import Position
from infra.index.osm_block_splitter import OsmBlockSplitter

# WGS 84 / UTM 23S, a projeção que o OSMnx escolhe para Belo Horizonte
GRAPH_CRS = "EPSG:32723"
TO_GRAPH_CRS = Transformer.from_crs("EPSG:4326", GRAPH_CRS, always_xy=True)
TO_LATLONG = Transformer.from_crs(GRAPH_CRS, "EPSG:4326", always_xy=True)
ORIGIN_X, ORIGIN_Y = TO_GRAPH_CRS.transform(-43.937, -19.932)


def make_graph() -> nx.MultiGraph:
	"""
	Três quarteirões que se encontram no nó 2:

	          3
	          |  B
	  1 ----- 2 ----- 4
	      A       C
	"""
	graph = nx.MultiGraph(crs=GRAPH_CRS)
	for node, (dx, dy) in {1: (0, 0), 2: (100, 0), 3: (100, 100), 4: (200, 0)}.items():
		graph.add_node(node, x=ORIGIN_X + dx, y=ORIGIN_Y + dy)
	graph.add_edge(1, 2, key=0, length=100)
	graph.add_edge(2, 3, key=0, length=100)
	graph.add_edge(2, 4, key=0, length=100)
	return graph


def make_position(dx: float, dy: float) -> Position:
	longitude, latitude = TO_LATLONG.transform(ORIGIN_X + dx, ORIGIN_Y + dy)
	return Position(latitude=latitude, longitude=longitude, timestamp=datetime(2026, 1, 1))


def test_returns_empty_list_for_empty_route():
	assert OsmBlockSplitter(make_graph())([]) == []


def test_splits_route_at_the_intersection_between_blocks():
	on_a = [make_position(20, -8), make_position(50, 6), make_position(80, -5)]
	on_b = [make_position(108, 30), make_position(95, 60)]

	assert OsmBlockSplitter(make_graph())(on_a + on_b) == [on_a, on_b]


def test_joins_positions_from_different_passes_through_the_same_block():
	first_pass_on_a = [make_position(20, -8), make_position(60, 5)]
	on_b = [make_position(105, 40), make_position(96, 70)]
	second_pass_on_a = [make_position(70, 7), make_position(30, -4)]
	on_c = [make_position(150, -6)]

	segments = OsmBlockSplitter(make_graph())(first_pass_on_a + on_b + second_pass_on_a + on_c)

	assert segments == [first_pass_on_a + second_pass_on_a, on_b, on_c]
