from fastapi import APIRouter, Depends, HTTPException

from application.evaluate_journey.evaluate_journey_dtos import EvaluateJourneyInputDTO, EvaluateJourneyOutputDTO
from application.evaluate_journey.evaluate_journey_use_case import EvaluateJourneyUseCase
from application.save_journey.save_journey_dtos import SaveJourneyInputDTO, SaveJourneyOutputDTO
from application.save_journey.save_journey_use_case import SaveJourneyUseCase
from infra.api.database import DBConnection
from infra.journey.mongodb.journey_repository import JourneyRepository

router = APIRouter()

@router.post("/journeys", response_model=SaveJourneyOutputDTO)
def save_journey(request: SaveJourneyInputDTO, session = Depends(DBConnection.get_session)):

    try:
        journey_repository = JourneyRepository(session=session)
        use_case = SaveJourneyUseCase(journey_repository)
        output = use_case.execute(input=request)

        return output

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/journeys/{journey_id}/score", response_model=EvaluateJourneyOutputDTO)
def get_journey_score(request: EvaluateJourneyInputDTO, session = Depends(DBConnection.get_session)):
    try:
        journey_repository = JourneyRepository(session=session)
        use_case = EvaluateJourneyUseCase(journey_repository, evaluators=[])
        output = use_case.execute(input=request)

        return output

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))