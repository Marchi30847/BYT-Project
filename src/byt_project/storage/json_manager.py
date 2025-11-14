import json
from pathlib import Path
from typing import Type, TypeVar, Generic, Optional
from ..models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class JSONStorage(Generic[T]):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    # Returns path to certain table
    def get_file_path(self, model_type: str, filename: Optional[str] = None) -> Path:
        model_dir = self.data_dir / model_type
        model_dir.mkdir(exist_ok=True)

        # Check for existing files, if not then mkdir
        if filename:
            return model_dir / f"{filename}.json"
        return model_dir

    # Saves one object into file
    def save_single(self, obj: T, filename: Optional[str] = None) -> str:
        if filename is None:
            filename = f"{obj.MODEL_TYPE}_{getattr(obj, 'id', 'unknown')}"

        file_path = self.get_file_path(obj.MODEL_TYPE, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(obj.to_dict(), f, ensure_ascii=False, indent=2)

        return str(file_path)

    # Get single object from file
    def load_single(self, model_class: Type[T], filename: str) -> T:
        file_path = self.get_file_path(model_class.MODEL_TYPE, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return model_class.from_dict(data)

    # Save collection to file
    def save_collection(self, objects: list[T], filename: str) -> str:
        if not objects:
            raise ValueError("No objects to save")

        model_type = objects[0].MODEL_TYPE
        file_path = self.get_file_path(model_type, filename)

        data = [obj.to_dict() for obj in objects]

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(file_path)

    # Get collection of objects from file
    def load_collection(self, model_class: Type[T], filename: str) -> list[T]:
        file_path = self.get_file_path(model_class.MODEL_TYPE, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            data_list = json.load(f)

        return [model_class.from_dict(data) for data in data_list]

    # List of all model types
    def list_files(self, model_type: str) -> list[str]:
        model_dir = self.get_file_path(model_type)
        return [f.stem for f in model_dir.glob("*.json")]

    # Deletes file
    def delete_file(self, model_type: str, filename: str) -> bool:
        file_path = self.get_file_path(model_type, filename)
        if file_path.exists():
            file_path.unlink()
            return True
        return False


storage = JSONStorage()
