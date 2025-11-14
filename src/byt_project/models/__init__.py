from .base import BaseModel, Serializable
from .employee import Employee

MODEL_REGISTRY = {
    "employee": Employee,
    # add other models here...
}


def create_model_from_dict(data: dict) -> BaseModel:
    model_type = data.get("type")
    if model_type not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model type: {model_type}")

    return MODEL_REGISTRY[model_type].from_dict(data)
