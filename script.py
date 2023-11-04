from sqlalchemy import delete, select, update

from crud.trading_model_crud import TradingModelCrud
from database import get_db
from models import Portfolio, User
from models.trading_model import ModelClass, ModelFrequency, TradingModel

session = next(get_db())

# ## CREATE
# # 1. creer une instance de classe sqlalchemy
# new_model = TradingModel(
#     name="my model",
#     model_cls=ModelClass.RAMSES_MODEL,
#     frequency=ModelFrequency.DAILY,
#     is_active=True
# )

# # 2. Ajouter l'instance a la session
# session.add(new_model)

# # 3. Commit la session
# session.commit()

# # CREATION avec la classe CRUD
# TradingModelCrud.create_one(session, {
#     "name":"my model_2",
#     "model_cls":ModelClass.RAMSES_MODEL,
#     "frequency":ModelFrequency.DAILY,
#     "is_active":True
# })

## READ
# 1. Preparer la query
statement = select(TradingModel.id, TradingModel.description).where(TradingModel.is_active.is_(True))

# 2. Executer la query
result = session.execute(statement).scalars().all()

# READ avec la classe CRUD
trading_models = TradingModelCrud.get_all(session)
print(f"trading_models {trading_models}")


## UPDATE
trading_model = TradingModelCrud.get_one(session, (TradingModel.name == "my model"))
trading_model.description = "Bonjour 2"
session.commit()


## DELETE
stmt = delete(TradingModel).where(TradingModel.name == "my model")
session.execute(stmt)
session.commit()

# trading_model.execute()
