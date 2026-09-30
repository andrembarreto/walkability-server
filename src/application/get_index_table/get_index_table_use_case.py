from domain.index.table import Table, DimensionItem
from .get_index_table_dtos import GetIndexTableOutputDTO, EventDTO, DimensionDTO

class GetIndexTableUseCase:
    def __init__(self, table: Table):
        self._table = table

    def execute(self) -> GetIndexTableOutputDTO:
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

            return GetIndexTableOutputDTO(dimensions=dimensions)

        except Exception as e:
            raise ValueError(f"Erro ao obter tabela do índice: {str(e)}")

    def _extract_events_from_dimension(self, dimension: DimensionItem) -> list[EventDTO]:
        events = []

        for criterium in dimension.criteria:
            for event in criterium.events:
                events.append(EventDTO(
                    id=event.id,
                    description=event.name
                ))

        return events
