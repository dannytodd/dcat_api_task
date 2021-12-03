from flask_restful import reqparse
from run import app
from models import db, ProcessRecord, ExecutionRecord, ProcessSchema, ExecutionSchema


@app.route('/', methods=['GET'])
def home():
    return '''<h1>D-CAT Full Stack Developer Task - Python API</h1>'''

@app.route('/process/new', methods=['GET'])
def api_process_new():
    """Return empty JSON payload for /process endpoint."""
    return ProcessRecord().default_payload()

@app.route('/process', methods=['POST'])
def api_process_add():
    """
    Parse required argument 'option_1' and optional argument 'option_2'
    then create an instance of ProcessRecord using arguments and insert into database.
    Return serialized payload of ProcessRecord instance.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("option_1", type=int, required=True, help="Missing argument")
    parser.add_argument("option_2", type=str, required=False)
    args = parser.parse_args()

    option_1 = args["option_1"]
    option_2 = args["option_2"]

    process = ProcessRecord(option_1=option_1, option_2=option_2)
    db.session.add(process)
    db.session.commit()

    return ProcessSchema().dump(process)

@app.route('/process/<int:id>/execute', methods=['POST'])
def api_process_execute(id):
    """
    Parse required argument 'id'
    then create an instance of ExecutionRecord using argument and insert into database if ProcessRecord exists for id value.
    Return serialized payload of ExecutionRecord instance.
    """
    process_id = id
    process = ProcessRecord.query.filter_by(id=process_id).first_or_404()

    execution = ExecutionRecord(process_id=process_id)
    db.session.add(execution)
    db.session.commit()

    return ExecutionSchema().dump(execution)

@app.route('/execution/<int:id>/status', methods=['GET'])
def api_execution_status(id):
    """
    Parse required argument 'id'
    then query database for ExecutionRecord with the same 'id' value as given argument.
    Return serialized payload describing current status of queried ExecutionRecord instance.
    """
    execution_id = id

    execution = ExecutionRecord.query.filter_by(id=execution_id).first_or_404()

    return execution.status(serialized=True)

@app.route('/execution/<int:id>', methods=['GET'])
def api_execution_get(id):
    """
    Parse required argument 'id'
    then query database for ExecutionRecord with the same 'id' value as given argument.
    Return serialized payload of ExecutionRecord instance.
    """
    execution_id = id

    execution = ExecutionRecord.query.filter_by(id=execution_id).first_or_404()

    return ExecutionSchema().dump(execution)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()
if __name__ == "__main__":
    app.run()