
from app.repository.db_manager import DbManager
from app.exceptions.exceptions import WrongPasswordError
from app.repository.db_models import Tags


class DataService:

    def __init__(self, db_manager:DbManager):
        self.db_manager = db_manager

    def update_password(self,user, data):
        if data.old_password != user.password:
            raise WrongPasswordError
        return self.db_manager.update(user,{"password":data["new_password"]})

    #правило - если у модели отношение с второй моделью,
    #то поле отношения наследует имя второй модели
    #то же касается имен полей в ДТО
    def create_record(self, model, data, user_id):
        data=data.model_dump()
        data["user_id"] = user_id
        new_record = self.db_manager.create(model, data)
        return new_record

    def create_transaction(self,model, data, user_id):
        # получение названий моделей, с которыми у нас отношения
        # relationships = self.db_manager.get_relationships(model)
        # for relationship in relationships:
        #     # для каждого отошения ищем записи по указанным айди
        #     # и добавляем их в data
        #     selected_records = self.db_manager.get_records_by_id(relationship.mapper.class_,
        #                                                          data[f"{relationship.key}"])
        #     data[f"{relationship.key}"] = selected_records
        data=data.model_dump()
        data["user_id"] = user_id
        data["Tags"] = self.db_manager.get_records_by_id(Tags,data["Tags"])
        new_record = self.db_manager.create(model, data)
        return new_record

    def read_record(self,model, record_id):
        data = {
            "id": record_id
        }
        target_record = self.db_manager.get_record(model, data)
        return target_record

    def read_records_by_page(self, model, page, user_id ):
        data = {
            "user_id": user_id
        }
        return self.db_manager.get_records_by_pages(model, page*5-5, 5, data)

    def read_model(self,model, conditions=None) -> list:
        records = self.db_manager.get_records(model,self.dict_to_query_list(conditions,model))
        return records

    def update_record(self, model, target_id:int, data):
        target_record = self.db_manager.get_record(model, {"id":target_id})
        return self.db_manager.update(target_record, data.model_dump())

    def update_transaction(self, model, target_id:int, data, user_id):
        target_record = self.db_manager.get_record(model, {"id":target_id, "user_id":user_id})
        tags_ids = [
            tag.id
            for tag in target_record.Tags
        ]
        data=data.model_dump()
        if "tagIds" in data and set(data["tagIds"]) != set(tags_ids):
            data["Tags"]=(self.db_manager.get_records_by_id(Tags, data["tagIds"]))
        return self.db_manager.update(target_record, data)

    def delete_record(self, model,target_id:int, user_id) -> None:
        target_record = self.db_manager.get_record(model, {"id":target_id, "user_id":user_id})
        return self.db_manager.delete(target_record)

    def dict_to_query_list(self, query_dict:dict | None, model) ->list:
        if query_dict is not None:
            query_list =[
                getattr(model, field) == value
                for field, value in query_dict.items()
            ]
            return query_list
        return None