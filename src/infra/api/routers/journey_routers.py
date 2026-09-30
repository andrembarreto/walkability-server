import logging

from fastapi import APIRouter, Depends, HTTPException

from domain.index.table import Table
from application.evaluate_journey.evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO
from application.evaluate_journey.evaluate_journey_use_case import EvaluateJourneyUseCase
from application.save_journey.save_journey_dtos import SaveJourneyInputDTO, SaveJourneyOutputDTO
from application.save_journey.save_journey_use_case import SaveJourneyUseCase
from infra.api.database import DBConnection
from infra.api.index_table import get_source as get_index_table_source
from infra.journey.mongodb.journey_repository import JourneyRepository

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/journeys", response_model=SaveJourneyOutputDTO)
def save_journey(request: SaveJourneyInputDTO, session = Depends(DBConnection.get_session)):

    try:
        journey_repository = JourneyRepository(session=session)
        use_case = SaveJourneyUseCase(journey_repository)
        output = use_case.execute(input=request)

        return output

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        logger.exception("Erro ao salvar jornada")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/journeys/{journey_id}/score", response_model=EvaluateJourneyOutputDTO)
def get_journey_score(journey_id: str, session = Depends(DBConnection.get_session)):
    try:
        journey_repository = JourneyRepository(session=session)
        index_table = Table(source=get_index_table_source())
        use_case = EvaluateJourneyUseCase(
            journey_repository=journey_repository,
            index_table=index_table,
        )
        output = use_case.execute(input=EvaluateJourneyInputDTO(journey_id=journey_id))

        return output

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        logger.exception("Erro ao avaliar jornada")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")