import json
import pytest
from datetime import date
from pathlib import Path

from src.byt_project.models.employee import Employee, Shift
from src.byt_project.storage.json_manager import JSONStorage


class TestEmployeePersistence:
    def setup_method(self):
        self.test_storage = JSONStorage("data")
        self.employee = Employee(
            hire_date=date(2023, 5, 15),
            salary=50000.0,
            shift=Shift.DAY
        )

    def teardown_method(self):
        test_dir = Path("data")
        if test_dir.exists():
            for file in test_dir.glob("**/*.json"):
                file.unlink()
            for dir in test_dir.glob("*/"):
                dir.rmdir()
            test_dir.rmdir()

    def test_01_save_single_employee_creates_correct_file(self):
        file_path = self.test_storage.save_single(self.employee, "test_employee")

        assert Path(file_path).exists()
        assert file_path.endswith("data\\employee\\test_employee.json")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data["hire_date"] == "2023-05-15"
        assert data["salary"] == 50000.0
        assert data["shift"] == "day"
        assert data["type"] == "employee"

    def test_02_load_single_employee_restores_all_fields(self):
        self.test_storage.save_single(self.employee, "test_employee")

        loaded_employee = self.test_storage.load_single(Employee, "test_employee")

        assert loaded_employee.hire_date == self.employee.hire_date
        assert loaded_employee.salary == self.employee.salary
        assert loaded_employee.shift == self.employee.shift
        assert loaded_employee.MODEL_TYPE == self.employee.MODEL_TYPE

    def test_03_save_and_load_multiple_employees(self):
        employees = [
            Employee(hire_date=date(2020, 1, 1), salary=40000, shift=Shift.DAY),
            Employee(hire_date=date(2021, 2, 1), salary=45000, shift=Shift.NIGHT),
            Employee(hire_date=date(2022, 3, 1), salary=50000, shift=Shift.DAY),
        ]

        for i, employee in enumerate(employees, 1):
            self.test_storage.save_single(employee, f"employee_{i}")

        loaded_employees = []
        for i in range(1, len(employees) + 1):
            employee = self.test_storage.load_single(Employee, f"employee_{i}")
            loaded_employees.append(employee)

        assert len(loaded_employees) == len(employees)
        for original, loaded in zip(employees, loaded_employees):
            assert original.hire_date == loaded.hire_date
            assert original.salary == loaded.salary
            assert original.shift == loaded.shift

    def test_05_employee_to_dict_includes_all_required_fields(self):
        result = self.employee.to_dict()

        expected_fields = {"hire_date", "salary", "shift", "type"}
        assert set(result.keys()) == expected_fields
        assert result["hire_date"] == "2023-05-15"
        assert result["shift"] == "day"
        assert result["type"] == "employee"

    def test_06_from_dict_creates_identical_object(self):
        original_dict = self.employee.to_dict()

        recreated_employee = Employee.from_dict(original_dict)

        assert recreated_employee.hire_date == self.employee.hire_date
        assert recreated_employee.salary == self.employee.salary
        assert recreated_employee.shift == self.employee.shift

    def test_07_json_serialization_round_trip(self):
        json_str = self.employee.to_json()
        recreated_employee = Employee.from_json(json_str)

        assert recreated_employee.hire_date == self.employee.hire_date
        assert recreated_employee.salary == self.employee.salary
        assert recreated_employee.shift == self.employee.shift

        new_json_str = recreated_employee.to_json()
        assert json_str == new_json_str

    def test_10_error_handling_for_invalid_files(self):
        corrupt_file_path = self.test_storage.get_file_path("employee", "corrupt")
        corrupt_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(corrupt_file_path, 'w', encoding='utf-8') as f:
            f.write('{"invalid": json}')

        with pytest.raises((json.JSONDecodeError, KeyError)):
            self.test_storage.load_single(Employee, "corrupt")

    def test_11_list_files_returns_correct_filenames(self):
        employees = [
            Employee(hire_date=date(2020, 1, 1), salary=40000, shift=Shift.DAY),
            Employee(hire_date=date(2021, 2, 1), salary=45000, shift=Shift.NIGHT),
        ]

        for i, employee in enumerate(employees, 1):
            self.test_storage.save_single(employee, f"emp_{i}")

        files = self.test_storage.list_files("employee")

        assert "emp_1" in files
        assert "emp_2" in files
        assert len(files) == len(employees)

    def test_12_delete_file_removes_existing_file(self):
        self.test_storage.save_single(self.employee, "to_delete")
        file_path = self.test_storage.get_file_path("employee", "to_delete")
        assert file_path.exists()

        result = self.test_storage.delete_file("employee", "to_delete")

        assert result is True
        assert not file_path.exists()

    def test_13_shift_enum_serialization_deserialization(self):
        day_employee = Employee(hire_date=date.today(), salary=50000, shift=Shift.DAY)
        night_employee = Employee(hire_date=date.today(), salary=55000, shift=Shift.NIGHT)

        day_dict = day_employee.to_dict()
        night_dict = night_employee.to_dict()

        day_restored = Employee.from_dict(day_dict)
        night_restored = Employee.from_dict(night_dict)

        assert day_restored.shift == Shift.DAY
        assert night_restored.shift == Shift.NIGHT
        assert day_dict["shift"] == "day"
        assert night_dict["shift"] == "night"
