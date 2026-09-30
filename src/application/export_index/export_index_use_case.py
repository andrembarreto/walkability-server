from domain.index.table import Table, DimensionItem, EventItem
from .export_index_dtos import ExportIndexOutputDTO, EventDTO, DimensionDTO

class ExportIndexUseCase:
    def __init__(self, table: Table):
        self._table = table

    def execute(self) -> ExportIndexOutputDTO:
        try:
            dimensions = []
            table_dimensions = self._table.dimensions
            for table_dimension in table_dimensions:
                dimension = DimensionDTO(
                    id=table_dimension.id,
                    name=table_dimension.name,
                    events=self._extract_events_from_dimension(table_dimension)
                )
                dimensions.append(dimension)

            return ExportIndexOutputDTO(dimensions=dimensions)

        except Exception as e:
            raise ValueError(f"Erro ao exportar índice: {str(e)}")

    def _extract_events_from_dimension(self, dimension: DimensionItem) -> list[EventDTO]:
        events = []

        for criterium in dimension.criteria:
            for event in criterium.events:
                events.append(EventDTO(
                    id=event.id,
                    description=event.name
                ))

        return events
