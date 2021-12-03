from datetime import datetime
import random
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Instantiate database
db = SQLAlchemy()

class ProcessRecord(db.Model):
    """ ProcessRecord for modelling and database CRUD-handling of Process data model """
    __tablename__ = 'process'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), server_onupdate=db.func.now())
    option_1 = db.Column(db.Integer, nullable=False, default=0)
    option_2 = db.Column(db.String, nullable=True, default=None)

    def __repr__(self):
        return '<Process %r>' % self.username

    @staticmethod
    def default_payload():
        temp_process = ProcessRecord()
        return {
            'option_1': 0,
            'option_2': None
        }

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'option_1': self.option_1,
            'option_2': self.option_2
        }

def generate_runtime(self):
    return random.randint(1, 20)


class ProcessSchema(SQLAlchemyAutoSchema):
    """
    ProcessSchema enabling serialization/deserialization
    from corresponding ProcessRecord model class.
    """
    class Meta:
        model = ProcessRecord
        load_instance = True


class ExecutionRecord(db.Model):
    """ ExecutionRecord for modelling and database CRUD-handling of Execution data model """
    __tablename__ = 'execution'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), server_onupdate=db.func.now())
    process_id = db.Column(db.Integer, db.ForeignKey('process.id'), nullable=False)
    runtime = db.Column(db.Integer, nullable=False, default=random.randint(1, 20))

    def status(self, serialized=False):
        """ If time elapsed since record creation is within or over runtime, return current status """
        return self.calculate_status(self.runtime, self.updated_at,serialized)

    @staticmethod
    def calculate_status(runtime, updated_at, serialized=False):
        status = None

        elapsed_time = datetime.now() - updated_at
        elapsed_time_seconds = elapsed_time.total_seconds()
        if runtime > elapsed_time_seconds > 0:
            status = 'running'
        elif elapsed_time_seconds > runtime:
            status = 'completed'

        if not serialized:
            return status
        else:
            return {
                'status': status
            }

    def __repr__(self):
        return '<Execution %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'process_id': self.process_id,
            'runtime': self.runtime
        }

class ExecutionSchema(SQLAlchemyAutoSchema):
    """
    ExecutionSchema enabling serialization/deserialization
    from corresponding ExecutionRecord model class.
    """
    class Meta:
        model = ExecutionRecord
        load_instance = True
