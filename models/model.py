

class Model:
    """
    
    """
    id: str
    name: str
    description: str
    function_name: str
    is_active: bool
    portfolio_order_id: str
    instruments: List[Instrument]
    features: List[Feature]
    frequency: str
    model_cls: str

    def activate(self):
        pass

    def execute(self):
        model_cls.execute()
    