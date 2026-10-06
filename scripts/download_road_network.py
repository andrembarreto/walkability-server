import argparse
from pathlib import Path

import osmnx as ox


DEFAULT_PLACE = "Belo Horizonte, Minas Gerais, Brazil"
DEFAULT_OUTPUT = Path("data/road_network.graphml")


def download(place: str, bbox: tuple[float, float, float, float] | None):
    if bbox is not None:
        return ox.graph_from_bbox(bbox, network_type="walk")
    return ox.graph_from_place(place, network_type="walk")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Baixa do OpenStreetMap a malha viária de pedestres usada pela "
            "estratégia de segmentação osm_blocks. A cidade inteira pode gerar "
            "um arquivo grande: prefira --bbox com a área de estudo."
        )
    )
    parser.add_argument("--place", default=DEFAULT_PLACE, help="Nome do lugar a consultar no Nominatim")
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("OESTE", "SUL", "LESTE", "NORTE"),
        help="Área retangular em graus (substitui --place)",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Arquivo GraphML de saída")
    arguments = parser.parse_args()

    graph = download(arguments.place, tuple(arguments.bbox) if arguments.bbox else None)
    graph = ox.project_graph(graph)
    graph = ox.convert.to_undirected(graph)

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(graph, arguments.output)

    print(f"{graph.number_of_edges()} quarteirões salvos em {arguments.output} ({graph.graph['crs']})")


if __name__ == "__main__":
    main()
