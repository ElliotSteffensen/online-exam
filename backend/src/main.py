from flask_cors import CORS
from flask import Flask, jsonify, request

from .entities.entity import Session, engine, Base
from .entities.exam import Exam, ExamSchema

app = Flask(__name__)
CORS(app)

Base.metadata.create_all(engine)


@app.route('/exams')
def get_exams():
    session = Session()
    exam_objects = session.query(Exam).all()

    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    session.close()
    return jsonify(exams)

@app.route('/exams', methods=['POST'])
def add_exam():
    posted_exam = ExamSchema(only=('title', 'description')).load(request.get_json())

    exam = Exam(**posted_exam, created_by="HTTP post request")

    session = Session()
    session.add(exam)
    session.commit()

    new_exam = ExamSchema().dump(exam)
    session.close()
    return jsonify(new_exam), 201
