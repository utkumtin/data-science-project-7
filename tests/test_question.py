import pytest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tasks.task_manager import create_student_dict, create_student_tuple, add_spell_to_set, filter_students_by_house, is_student_allowed, merge_spell_sets, remove_forbidden_item, count_students_per_house, house_with_most_students, student_summary

def test_create_student_tuple():
    assert create_student_tuple("Harry", 17, "Gryffindor") == ("Harry", 17, "Gryffindor")

def test_add_spell_to_set():
    assert add_spell_to_set({"Expelliarmus"}, "Alohomora") == {"Expelliarmus", "Alohomora"}

def test_remove_forbidden_item():
    assert remove_forbidden_item({"Horcrux", "Elder Wand"}, "Horcrux") == {"Elder Wand"}

def test_count_students_per_house():
    students = [("Harry", "Gryffindor"), ("Draco", "Slytherin"), ("Ron", "Gryffindor")]
    assert count_students_per_house(students) == {"Gryffindor": 2, "Slytherin": 1}

def test_house_with_most_students():
    houses = {"Gryffindor": 10, "Slytherin": 8, "Ravenclaw": 9}
    assert house_with_most_students(houses) == "Gryffindor"

def test_student_summary():
    tup = ("Hermione", 17, "Gryffindor")
    assert student_summary(tup) == "Hermione, age 17, is in Gryffindor."

def test_merge_spell_sets():
    set1 = {"Lumos", "Alohomora"}
    set2 = {"Expelliarmus", "Alohomora"}
    assert merge_spell_sets(set1, set2) == {"Lumos", "Alohomora", "Expelliarmus"}

def test_create_student_dict():
    spells = {"Lumos", "Accio"}
    expected = {"name": "Luna", "age": 16, "spells": spells}
    assert create_student_dict("Luna", 16, spells) == expected

def test_is_student_allowed():
    assert is_student_allowed({"Wand", "Book"}, {"Horcrux", "Elder Wand"}) == True
    assert is_student_allowed({"Horcrux"}, {"Horcrux", "Elder Wand"}) == False

def test_filter_students_by_house():
    students = [
        {"name": "Harry", "house": "Gryffindor"},
        {"name": "Draco", "house": "Slytherin"},
        {"name": "Ron", "house": "Gryffindor"},
    ]
    result = filter_students_by_house(students, "Gryffindor")
    assert result == [
        {"name": "Harry", "house": "Gryffindor"},
        {"name": "Ron", "house": "Gryffindor"}
    ]

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://edugen-backend-487d2168bc6c.herokuapp.com/projectLog/"
    payload = {
        "user_id": 34,
        "project_id": 133,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()