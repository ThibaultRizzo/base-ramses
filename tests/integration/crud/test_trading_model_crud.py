from utils.testing import compare_item, compare_list
from crud.trading_model_crud import TradingModelCrud
from models.trading_model import TradingModel, ModelClass, ModelFrequency

def test_get_active_trading_models(db_session_2):
    # Given one active trading model
    active_model= TradingModel(
        name="trading_model_3",
        model_cls=ModelClass.RAMSES_MODEL,
        execution_frequency=ModelFrequency.HOURLY,
        is_active=True
    )
    inactive_model= TradingModel(
        name="trading_model_2",
        model_cls=ModelClass.RAMSES_MODEL,
        execution_frequency=ModelFrequency.HOURLY,
        is_active=False
    )
    db_session_2.add_all([active_model, inactive_model])
    db_session_2.flush()

    # When retrieving active trading models
    active_models = TradingModelCrud.get_active_trading_models()

    # Then two models are returned
    compare_list(
        [
            {
                "description": "None",
                "execution_frequency": "HOURLY",
                "is_active": "True",
                "is_in_production": "False",
                "model_cls": "RamsesModel",
                "name": "trading_model",
                "portfolio_id": "None"
            }
        ],
        active_models
    )


