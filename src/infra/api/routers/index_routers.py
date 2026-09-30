import logging

from fastapi import APIRouter, HTTPException

from domain.index.table import Table
from application.get_index_table.get_index_table_use_case import GetIndexTableUseCase
from infra.api.index_table import get_source as get_index_table_source

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/index")
def get_index_table():
    try:
        index_table = Table(source=get_index_table_source())
        use_case = GetIndexTableUseCase(table=index_table)
        output = use_case.execute()

        return output

    except Exception:
        logger.exception("Erro ao obter tabela do índice")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")