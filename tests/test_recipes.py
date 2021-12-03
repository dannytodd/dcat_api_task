import time
from datetime import datetime
from models import ExecutionRecord


def test_get_api_process_new(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a GET request at the '/process/new' endpoint
    THEN check that the correct empty payload is returned
    """
    response = client.get("/process/new")

    assert response.content_type == 'application/json'
    assert response == {"option_1": 0, "option_2": ""}

def test_post_api_process_add(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a POST request at the '/process' endpoint
    THEN check that the correct payload is returned
    """
    data = {"option_1": 1,
            "option_2": "text"}
    response = client.post("/process", json=data)

    assert response.content_type == 'application/json'
    assert response == {"option_1": 1, "option_2": "text"}

def test_post_api_process_add_missing_arg(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a POST request at the '/process/new' endpoint with a missing argument
    THEN check that a '400' status code is returned
    """
    data = {}
    response = client.post("/process", json=data)

    assert response.status_code == 400

def test_post_api_process_add_incorrect_type(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a POST request at the '/process/new' endpoint with incorrect argument types
    THEN check that a '400' status code is returned
    """
    data = {"option_1": "text",
            "option_2": 123}
    response = client.post("/process", json=data)

    assert response.status_code == 400

def test_post_api_process_execute(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a POST request at the '/process/<id>/execute' endpoint
    THEN check that the correct execution model is returned with matching process_id
    """
    id = 2
    response = client.post(f"/process/{id}/execute")

    assert response["process_id"] == id

def test_post_api_process_execute_nonexistent_process(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a POST request at the '/process/<id>/execute' endpoint with a process_id of a nonexistent record
    THEN check that a '404' status code is returned
    """
    id = 9999
    response = client.post(f"/process/{id}/execute")

    assert response.status_code == 404

def test_get_api_execution_status(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a GET request at the '/execution/<id>/status' endpoint
         after executing a POST request at the '/process/<id>/execute' endpoint
    THEN check that the correct execution status is return with value of either 'running' or 'completed'
    """
    id = 2
    _ = client.post(f"/process/{id}/execute")
    response = client.get(f"/execution/{id}/status")

    assert response["status"] == "running" or response["status"] == "completed"


def test_get_api_execution_status_correct(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a GET request at the '/execution/<id>/status' endpoint
         after executing a POST request at the '/process/<id>/execute' endpoint
    THEN check that the correct execution status is calculated and returned by comparing runtime value and current elapsed time
    """
    id = 2
    post_response = client.post(f"/process/{id}/execute")
    runtime = post_response["runtime"]
    updated_at = post_response["updated_at"]

    status = ""
    while status != "completed":
        elapsed_time = datetime.now() - updated_at
        elapsed_time_seconds = elapsed_time.total_seconds()
        status_response = client.get(f"/execution/{id}/status")

        if runtime < elapsed_time_seconds:
            assert status_response["status"] == "running"
        elif runtime >= elapsed_time_seconds:
            assert status_response["status"] == "completed"
        status = status_response["status"]
        time.sleep(0.5)

    assert status == "completed"

def test_get_api_execution_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a GET request at the '/execution/<id>' endpoint
         after executing a POST request at the '/process/' endpoint
         and then executing a POST request at the '/process/<id>/execute' endpoint
    THEN check that the correct execution model is returned with matching process_id and correct runtime randomised value
    """
    data = {"option_1": 1}
    process_post_response = client.post("/process", json=data)

    process_id = process_post_response["id"]
    execution_post_response = client.post(f"/process/{process_id}/execute")
    execution_id = execution_post_response["id"]

    response = client.get(f"/execution/{execution_id}")

    assert response["id"] != None
    assert response["created_at"] != None
    assert response["updated_at"] != None
    assert response["process_id"] != None
    assert response["runtime"] != None
    assert response["process_id"] == process_id
    assert response["runtime"] >= 1
    assert response["runtime"] <= 20

def test_get_api_execution_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN executing a GET request at the '/execution/<id>' endpoint using an id argument with nonexistent ExecutionRecord
    THEN check that a '404' status code is returned
    """
    id = 9999
    response = client.get(f"/execution/{id}")

    assert response.status_code == 404
