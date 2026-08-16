from sqlalchemy import select, inspect



#todo: async()
#todo: специализированный менеджер для будущих моделей

class DbManager():
    #model - умное название для таблицы в бд
    def __init__(self, db):
        self.db = db

    def create(self, model, data:dict):
        obj = model(**data)
        self.db.add(obj)
        self.db.commit()
        return obj

    #рудимент
    # в какой модели, по какому параметру и значению ищем решает верхний слой
    def check(self, model, *conditions) -> bool:
        query = select(model).where(*conditions)
        return self.db.scalar(query) is not None

    #возвращение первой попавшейся записи
    def get_record(self, model, data:dict):
        #list comprehension
        conditions= [
            getattr(model,field) == value
            for field, value in data.items()
        ]
        query = select(model).where(*conditions)
        return self.db.scalars(query).one()

    def get_records_by_pages(self,model, _offset,_limit, data:dict) -> list:
        conditions= [
            getattr(model,field) == value
            for field, value in data.items()
        ]
        query = (
            select(model)
            .where(*conditions)
            .order_by(model.id)
            .offset(_offset)
            .limit(_limit)
        )
        output_model = [

        ]
        result = self.db.execute(query).scalars()
        for record in result:
            output_model.append(record)
        return output_model

    #возвращение всей таблицы или полей по запросу query
    def get_records(self, model, conditions:list | None) ->list:
            query=select(model)
            if conditions is not None:
                query = query.where(*conditions)
            output_model = [
                ]
            result = self.db.execute(query).scalars()

            for record in result:
                output_model.append(record)
            return output_model

    def get_records_by_id(self, model, ids:list[int]):
        return self.get_records(model, [model.id.in_(ids)])


    def update(self, target, data):
        try:
            update_data = data #не включать в словарь непереданные поля
            for field, value in update_data.items():
                setattr(target,field,value)
            self.db.commit()
            return target

        except Exception:
            self.db.rollback()
            raise

    def delete(self, target) -> bool:
        self.db.delete(target)
        self.db.commit()
        #self.db.flush()
        return True


    def get_relationships(self, target) -> list:
        return list(inspect(target).relationships)



