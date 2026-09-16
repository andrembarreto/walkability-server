from fastapi import APIRouter, Depends, HTTPException

from application.save_journey.save_journey_dtos import SaveJourneyInputDTO, SaveJourneyOutputDTO
from application.save_journey.save_journey_use_case import SaveJourneyUseCase
from infra.api.database import get_session
from infra.journey.mongodb.journey_repository import JourneyRepository

router = APIRouter()

@router.post("/journeys", response_model=SaveJourneyOutputDTO)
def save_journey(request: SaveJourneyInputDTO, session = Depends(get_session)):

    try:
        journey_repository = JourneyRepository(
            client=session.client,
            database_name=session.database_name
        )
        use_case = SaveJourneyUseCase(journey_repository)
        output = use_case.execute(input=request)

        return output

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))