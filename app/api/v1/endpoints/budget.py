
from fastapi import APIRouter, Depends
from starlette import status
from app.api.v1.dependency.dependency import get_current_user, get_data_service
from app.repository.db_models import *
from app.service.DataService import DataService
from app.DTO.budget import *

router = APIRouter()

@router.post("/budget", response_model = BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        data: BudgetCreateDTO,
        service : DataService = Depends(get_data_service),
        user: User = Depends (get_current_user)
):
    full_data = BudgetDTO(
        name = data.name,
        limit = data.limit,
        colour = data.colour
    )
    return service.create_record(Budget,full_data, user.id)


@router.get("/budget",response_model = list[BudgetResponse], status_code = status.HTTP_200_OK)
def read_categories(
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    return  service.read_model(Budget, {"user_id" : user.id})


@router.patch("/budget/{category_id}",response_model = BudgetResponse, status_code=status.HTTP_200_OK)
def update_category(
        category_id:int,
        data: BudgetUpdateDTO,
        service : DataService = Depends(get_data_service)
):

    return service.update_record(Budget,category_id,data)

@router.delete("/budget/{category_id}", response_model=None, status_code = status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id:int,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    service.delete_record(Budget, category_id,user.id)
    return