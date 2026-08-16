
from fastapi import APIRouter, Depends
from starlette import status
from app.api.v1.dependency.dependency import get_current_user,get_data_service
from app.repository.db_models import *
from app.service.DataService import DataService
from app.DTO.transactions import *
router = APIRouter()


@router.post("/transactions", response_model = TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
        data: TransactionCreateDTO,
        service : DataService = Depends(get_data_service),
        user: User = Depends (get_current_user)
):
    full_data = TransactionDTO(
        name = data.name,
        sum=data.sum,
        description=data.description,
        categoryId=data.categoryId,
        Tags = data.tagIds
    )
    return service.create_transaction(Transactions, full_data, user.id)


@router.get("/transactions/{page}",response_model = list[TransactionResponse], status_code = status.HTTP_200_OK)
def read_transactions(
        page:int = None,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    return service.read_records_by_page(Transactions, page, user.id)
@router.patch("/transactions/{transaction_id}",response_model = TransactionResponse, status_code=status.HTTP_200_OK)
def update_transaction(
        transaction_id:int,
        data: TransactionUpdateDTO,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):

    return service.update_transaction(Transactions,transaction_id,data, user.id)

@router.delete("/transactions/{transaction_id", response_model=None, status_code = status.HTTP_204_NO_CONTENT)
def delete_transaction(
        transaction_id:int,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    service.delete_record(Transactions, transaction_id, user.id)
    return