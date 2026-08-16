from fastapi import APIRouter, Depends
from starlette import status
from app.api.v1.dependency.dependency import get_current_user, get_data_service
from app.repository.db_models import *
from app.service.DataService import DataService
from app.DTO.tags import *
router = APIRouter()


@router.post("/tag", response_model = TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(
        data: TagCreateDTO,
        service : DataService = Depends(get_data_service),
        user: User = Depends (get_current_user)
):
    return service.create_record(Tags, data, user.id)


@router.get("/tag",response_model = list[TagResponse], status_code = status.HTTP_200_OK)
def read_tags(
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    return  service.read_model(Tags, {"user_id" : user.id})


@router.patch("/tag/{tag_id}",response_model = TagResponse, status_code=status.HTTP_200_OK)
def update_tag(
        tag_id:int,
        data: TagUpdateDTO,
        service : DataService = Depends(get_data_service)
):
    return service.update_record(Tags, tag_id, data)

@router.delete("/tag/{tag_id}", response_model=None, status_code = status.HTTP_204_NO_CONTENT)
def delete_tag(
        tag_id:int,
        service : DataService = Depends(get_data_service),
        user: User = Depends(get_current_user)
):
    service.delete_record(Tags, tag_id, user.id)
    return


