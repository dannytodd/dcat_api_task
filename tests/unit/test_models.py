from ...models import ProcessRecord, ExecutionRecord
#import models


def test_new_process():
    """
    GIVEN a Process model
    WHEN a new ProcessRecord is created
    THEN check the option_1 and option_2 attributes have the correct values
    """
    process = models.ProcessRecord(12, "text")
    assert process.option_1 == 12
    assert process.option_2 == 'text'

def test_new_process_missing_arg():
    """
    GIVEN an empty Process model
    WHEN a new ProcessRecord creation is attempted
    THEN check that ProcessRecord was not instantiated
    """
    process = models.ProcessRecord(None)
    assert process == None

def test_new_process_incorrect_type():
    """
    GIVEN a Process model with incorrect types
    WHEN a new ProcessRecord creation is attempted
    THEN check that ProcessRecord was not instantiated
    """
    process = models.ProcessRecord("text", 123)
    assert process == None

def test_new_execution():
    """
    GIVEN a Execution model
    WHEN a new Execution is created
    THEN check the process_id attribute has the correct value
    """
    execution = models.ExecutionRecord(2)
    assert execution.process_id == 2

def test_new_execution_missing_arg():
    """
    GIVEN an empty Execution model
    WHEN a new ExecutionRecord creation is attempted
    THEN check that ExecutionRecord was not instantiated
    """
    execution = models.ExecutionRecord(None)
    assert execution == None

def test_new_execution_incorrect_type():
    """
    GIVEN a Execution model with incorrect types
    WHEN a new ExecutionRecord creation is attempted
    THEN check that ExecutionRecord was not instantiated
    """
    execution = models.ExecutionRecord("text")
    assert execution == None

