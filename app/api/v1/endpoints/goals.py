from fastapi import APIRouter, Depends
from starlette import status
from app.api.v1.dependency.dependency import get_current_user, get_data_service
from app.repository.db_models import *
from app.service.DataService import DataService
from app.DTO.goals import *
router = APIRouter()

@router.post("/goals", response_model = GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
        data: GoalCreateDTO,
        service : DataService = Depends(get_data_service),
        user: User = Depends (get_current_user)
):
    return service.create_record(Goals, data, user.id)


@router.get("/goals",response_model = list[GoalResponse], status_code = status.HTTP_200_OK)
def read_goals(
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    return  service.read_model(Goals, {"user_id" : user.id})

@router.patch("/goals/{goal_id}",response_model = GoalResponse, status_code=status.HTTP_200_OK)
def update_goal(
        goal_id:int,
        data: GoalUpdateDTO,
        service : DataService = Depends(get_data_service)
):

    return service.update_record(Goals,goal_id,data)

@router.delete("/goals/{goal_id", response_model=None, status_code = status.HTTP_204_NO_CONTENT)
def delete_transaction(
        goal_id:int,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    service.delete_record(Goals, goal_id,user.id)
    return