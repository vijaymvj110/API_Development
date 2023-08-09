from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/app_develop'
db = SQLAlchemy(app)


class CandidateRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_title = db.Column(db.String(50), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    time_zone = db.Column(db.String(50), nullable=False)
    skype_id = db.Column(db.String(50), nullable=True)
    mobile = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(50), nullable=True)
    organization = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(50), nullable=True)
    current_company = db.Column(db.String(50), nullable=True)
    domain_expertise = db.Column(db.String(50), nullable=True)
    awards = db.Column(db.String(50), nullable=True)
    user_name = db.Column(db.String(50), nullable=False)
    passport_number = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    source = db.Column(db.String(50), nullable=True)
    expected_ctc = db.Column(db.String(50), nullable=True)
    notice_period = db.Column(db.String(50), nullable=True)


with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/candidate_register', methods=['POST'])
def register_candidate():
    resume_title = request.json['resume_title']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    time_zone = request.json['time_zone']
    skype_id = request.json['skype_id']
    mobile = request.json['mobile']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    country = request.json['country']
    zip_code = request.json['zip_code']
    organization = request.json['organization']
    skills = request.json['skills']
    education = request.json['education']
    current_company = request.json['current_company']
    domain_expertise = request.json['domain_expertise']
    awards = request.json['awards']
    user_name = request.json['user_name']
    passport_number = request.json['passport_number']
    experience = request.json['experience']
    source = request.json['source']
    expected_ctc = request.json['expected_ctc']
    notice_period = request.json['notice_period']

    if not first_name or not last_name or not time_zone or not mobile or not organization or not user_name:
        return jsonify({'Message': f'Mandatory fields not filled'})

    new_candidate = CandidateRegister(resume_title=resume_title, first_name=first_name, last_name=last_name,
                                      time_zone=time_zone,
                                      skype_id=skype_id, mobile=mobile, address=address, city=city, state=state,
                                      country=country,
                                      zip_code=zip_code, organization=organization, skills=skills, education=education,
                                      current_company=current_company, domain_expertise=domain_expertise, awards=awards,
                                      user_name=user_name,
                                      passport_number=passport_number, expected_ctc=expected_ctc, source=source,
                                      experience=experience,
                                      notice_period=notice_period)
    db.session.add(new_candidate)
    db.session.commit()
    return jsonify({'Message': f'Candidate registered successfully'})


@app.route('/candidate_details/<int:id>', methods=['GET'])
def get_candidate_details(id):
    candidate = CandidateRegister.query.get(id)

    if not candidate:
        return jsonify({'Message': f'There is no candidate available for id number {id}'})

    candidate_data = {
        'resume_title': candidate.resume_title,
        'first_name': candidate.first_name,
        'last_name': candidate.last_name,
        'time_zone': candidate.time_zone,
        'skype_id': candidate.skype_id,
        'mobile': candidate.mobile,
        'address': candidate.address,
        'city': candidate.city,
        'state': candidate.state,
        'country': candidate.country,
        'zip_code': candidate.zip_code,
        'organization': candidate.organization,
        'skills': candidate.skills,
        'education': candidate.education,
        'current_company': candidate.current_company,
        'domain_expertise': candidate.domain_expertise,
        'awards': candidate.awards,
        'user_name': candidate.user_name,
        'passport_number': candidate.passport_number,
        'experience': candidate.experience,
        'source': candidate.source,
        'expected_ctc': candidate.expected_ctc,
        'notice_period': candidate.notice_period
    }
    return jsonify(candidate_data), 200


@app.route('/update_candidate/<int:id>', methods=['PUT'])
def candidate_update(id):
    update = CandidateRegister.query.get(id)

    resume_title = request.json['resume_title']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    time_zone = request.json['time_zone']
    skype_id = request.json['skype_id']
    mobile = request.json['mobile']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    country = request.json['country']
    zip_code = request.json['zip_code']
    organization = request.json['organization']
    skills = request.json['skills']
    education = request.json['education']
    current_company = request.json['current_company']
    domain_expertise = request.json['domain_expertise']
    awards = request.json['awards']
    user_name = request.json['user_name']
    passport_number = request.json['passport_number']
    experience = request.json['experience']
    source = request.json['source']
    expected_ctc = request.json['expected_ctc']
    notice_period = request.json['notice_period']

    if not first_name or not last_name or not time_zone or not mobile or not organization or not user_name:
        return jsonify({'Message': f'Mandatory fields not filled'})
    if not update:
        return jsonify({"Message": f"Candidate not available for id {id}"})

    update.resume_title = resume_title
    update.first_name = first_name
    update.last_name = last_name
    update.time_zone = time_zone
    update.skype_id = skype_id
    update.mobile = mobile
    update.address = address
    update.city = city
    update.state = state
    update.country = country
    update.zip_code = zip_code
    update.organization = organization
    update.skills = skills
    update.education = education
    update.current_company = current_company
    update.domain_expertise = domain_expertise
    update.awards = awards
    update.user_name = user_name
    update.passport_number = passport_number
    update.experience = experience
    update.source = source
    update.expected_ctc = expected_ctc
    update.notice_period = notice_period

    db.session.commit()
    return jsonify({"Message": "Candidate details updated successfully"})


@app.route('/delete_candidate/<int:id>', methods=['DELETE'])
def candidate_delete(id):
    delete = CandidateRegister.query.get(id)

    if not delete:
        return jsonify({'Message': f'There is no candidate available for id {id}'})
    db.session.delete(delete)
    db.session.commit()
    return jsonify({'Message': 'Candidate deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
