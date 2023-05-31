from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/app_develop'
db = SQLAlchemy(app)


class JobRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(50), nullable=False)
    job_category = db.Column(db.String(50), nullable=False)
    employment_type = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=True)
    compensation_range = db.Column(db.String(50), nullable=True)
    major_skills = db.Column(db.String(50), nullable=True)
    minor_skills = db.Column(db.String(50), nullable=True)
    vacancy = db.Column(db.Integer, nullable=False)
    job_description = db.Column(db.String(500), nullable=False)
    job_responsibilities = db.Column(db.String(500), nullable=True)


with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/job_register', methods=['POST'])
def register_job():
    job_title = request.json['job_title']
    organization = request.json['organization']
    job_category = request.json['job_category']
    employment_type = request.json['employment_type']
    priority = request.json['priority']
    level = request.json['level']
    experience = request.json['experience']
    currency = request.json['currency']
    compensation_range = request.json['compensation_range']
    major_skills = request.json['major_skills']
    minor_skills = request.json['minor_skills']
    vacancy = request.json['vacancy']
    job_description = request.json['job_description']
    job_responsibilities = request.json['job_responsibilities']

    if not job_title and not organization and not job_category:
        return jsonify({'Message': 'Mandatory fields not filled'})
    if not experience and not vacancy and not job_description:
        return jsonify({'Message': 'Mandatory fields not filled'})

    new_job = JobRegister(job_title=job_title, organization=organization, job_category=job_category,
                          employment_type=employment_type,
                          priority=priority, level=level, experience=experience, currency=currency,
                          compensation_range=compensation_range,
                          major_skills=major_skills, minor_skills=minor_skills, vacancy=vacancy,
                          job_description=job_description, job_responsibilities=job_responsibilities)
    db.session.add(new_job)
    db.session.commit()
    return jsonify({'Message': 'Job registered successfully'})


@app.route('/job_details/<int:id>', methods=['GET'])
def get_job_details(id):
    job = JobRegister.query.get(id)

    if not job:
        return jsonify({'Message': f'No job available for id number {id}'}), 400

    job_data = {
        'job_title': job.job_title,
        'organization': job.organization,
        'job_category': job.job_category,
        'employment_type': job.employment_type,
        'priority': job.priority,
        'level': job.level,
        'experience': job.experience,
        'currency': job.currency,
        'compensation_range': job.compensation_range,
        'major_skills': job.major_skills,
        'minor_skills': job.minor_skills,
        'vacancy': job.vacancy,
        'job_description': job.job_description,
        'job_responsibilities': job.job_responsibilities
    }
    return jsonify(job_data), 200


@app.route('/delete_job/<int:id>', methods=['DELETE'])
def delete_job(id):
    job = JobRegister.query.get(id)

    if not job:
        return jsonify({'Message': f'There is no job available to delete the id number {id}'})
    db.session.delete(job)
    db.session.commit()
    return jsonify(job)


if __name__ == '__main__':
    app.run(debug=True)
