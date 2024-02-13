import random
from models import TaskSerializer

import pytest
import requests

tasks = []
user_id = "002"


# Fixture to setup base URL for API requests
@pytest.fixture
def api_base_url():
    return "https://todo.pixegami.io"


# Test case for testing API endpoint
def test_create_task(api_base_url):
    global tasks
    global user_id
    print(f"User_ID: {user_id}")
    body = {
        "content": f"my automation_{random.randint(0, 999999)}",
        "user_id": user_id,
        "task_id": f"{random.randint(0, 999999)}",
        "is_done": False
    }
    response = requests.put(f"{api_base_url}/create-task", json=body)
    flag = False
    print(f"Response Received: {response.json().get('task')}")
    assert response.status_code == 200
    assert response.json().get("task") is not None
    try:
        TaskSerializer().load(response.json().get("task"))
        flag = True
    except Exception as e:
        print(f"ERROR >>> {e}")
        flag = False
    assert flag is True


def test_update_task(api_base_url):
    global tasks
    for task in tasks:
        task["content"] = "Modified Content"
        response = requests.put(f"{api_base_url}/update-task", json=task)
        print(response.json())
        assert response.status_code == 200
        assert response.json().get("task") is not None
        flag = False
        print(f"Response Received: {response.json()}")
        try:
            TaskSerializer().load(response.json().get("task"))
            flag = True
        except Exception as e:
            print(f"ERROR >>> {e}")
            flag = False
        assert flag is True


def test_get_task_by_id(api_base_url):
    global tasks
    for task in tasks:
        response = requests.get(f"{api_base_url}/get-task/{task.get('task_id')}")
        flag = False
        assert response.status_code == 200
        assert response.json().get("task") is not None
        print(f"Response Received: {response.json()}")
        try:
            TaskSerializer().load(response.json().get("task"))
            flag = True
        except Exception as e:
            print(f"ERROR >>> {e}")
            flag = False
        assert response.json().get("task").get("content") == "Modified Content"
        assert flag is True


def test_create_multiple_tasks(api_base_url):
    global tasks
    global user_id
    print("Total Tasks Created: 3")
    print(f"Multiple Tasks for user_id: {user_id}")
    for _ in range(3):
        body = {
            "content": f"my automation_{random.randint(0, 999999)}",
            "user_id": user_id,
            "task_id": f"{random.randint(0, 999999)}",
            "is_done": False
        }
        response = requests.put(f"{api_base_url}/create-task", json=body)
        flag = False
        print(f"Response Received: {response.json()}")
        assert response.status_code == 200
        assert response.json().get("task") is not None
        try:
            TaskSerializer().load(response.json().get("task"))
            flag = True
        except Exception as e:
            print(f"ERROR >>> {e}")
            flag = False
        assert flag is True


def test_get_list(api_base_url):
    global tasks
    global user_id
    print(f"User_ID: {user_id}")
    tasks = []
    response = requests.get(f"{api_base_url}/list-tasks/{user_id}")
    assert response.status_code == 200
    assert len(response.json().get("tasks")) != 0
    print(f"Response Received: {response.json()}")
    if len(response.json().get("tasks")) != 0:
        tasks = response.json().get("tasks")
        for task in tasks:
            flag = False
            try:
                TaskSerializer().load(task)
                flag = True
            except Exception as e:
                print(e)
                flag = False
            assert flag is True


def test_delete_task(api_base_url):
    global tasks
    for task in tasks:
        response = requests.delete(f"{api_base_url}/delete-task/{task.get('task_id')}")
        assert response.status_code == 200
        print(f"Response Received: {response.json()}")
