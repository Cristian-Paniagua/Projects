from flask import Flask, jsonify, request
from flask_cors import CORS

from handler.requisite import RequisiteHandler
from handler.room import RoomHandler
from handler.sections import SectionHandler
from handler.Class import ClassHandler
from handler.meeting import MeetingHandler
from handler.chat import ChatHandler
from handler.UserLogin import UserHandler
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return 'Hello World!'

entity_handler_map = {
    'room': RoomHandler(),
    'section': SectionHandler(),
    'class': ClassHandler(),
    'meeting': MeetingHandler()
    # Add more entities here
}
@app.route('/losprogramadores/requisite', methods=[ 'GET', 'POST' ])
def requisite():
    if request.method == 'GET':
        return RequisiteHandler().getAll()
    else:
        return RequisiteHandler().insert(request.json)

@app.route('/losprogramadores/requisite/<int:classid>/<int:preid>', methods=[ 'GET', 'PUT', 'DELETE' ])
def requisiteById(classid, preid):
    if request.method == 'GET':
        return RequisiteHandler().getById(classid, preid)
    elif request.method == 'PUT':
        return RequisiteHandler().update(classid, preid, request.json)
    else:
        return RequisiteHandler().delete(classid, preid)

@app.route('/losprogramadores/<entity>', methods=['GET', 'POST'])
def Entity(entity):
    handler =entity_handler_map.get(entity)
    if not handler:
        return jsonify(error="Entity not found"), 404

    if request.method == 'GET':
        return handler.getAll()

    else:
        return handler.insert(request.json)

@app.route('/losprogramadores/<entity>/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def getById(entity, id):
    handler =entity_handler_map.get(entity)
    if not handler:
        return jsonify(error="Entity not found"), 404
    if request.method == 'GET':
        return handler.getById(id)
    elif request.method == 'DELETE':
        return handler.deleteById(id)
    else:
        return handler.updateById(id, request.json)

@app.route('/losprogramadores/room/<building>/capacity', methods = ['POST'])
def getTopThreeCap(building):
    try:
        data= request.get_json()
        return RoomHandler().getTopThreeCap(building)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/losprogramadores/room/<building>/ratio', methods=['POST'])
def getTopThreeRatio(building):
    try:
        data = request.get_json()
        return RoomHandler().getTopThreeRatio(building)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/losprogramadores/room/<int:rid>/classes', methods = ['POST'])
def getTopThreeMostTaught(rid):
    try:
        data = request.get_json()
        return RoomHandler().getTopThreeMostTaught(rid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/losprogramadores/most/prerequisite', methods=['POST'])
def getTopThreePrerequisites():
    try:

        data = request.get_json()  # Optional: use if any data is needed in the POST body
        return RequisiteHandler().getTopThreePrerequisites()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/losprogramadores/section/year', methods = ['POST'])
def getTotalSectionsPerYear():
    try:
        data = request.get_json()
        return SectionHandler().getTotalSectionsPerYear()

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/losprogramadores/classes/<year>/<semester>', methods = ['POST'])
def getMostTaughtperSemester(year, semester):
    try:

        data = request.get_json()
        return SectionHandler().getMostTaughtPerSemester(year, semester.capitalize())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/losprogramadores/most/meeting', methods=['POST'])
def getMostMeeting():
    try:
        data = request.get_json()
        return MeetingHandler().getTopMeetingsWithMostSections()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/losprogramadores/least/classes', methods = ['POST'])
def getLeastOfferedClasses():
    try:
        data = request.get_json()
        return SectionHandler().getTopThreeLeastOfferedClasses()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/losprogramadores/chat', methods = ['POST'])
def Chat():
    return ChatHandler().QuestionAndAnswer(request.json)

# @app.route('/losprogramadores/register', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     try:
#         UserHandler().register_user(username, password)
#         return jsonify({"message": "User registered successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400


@app.route('/losprogramadores/login', methods=['POST'])
def login_user():
    return UserHandler().login(request.json)

@app.route('/losprogramadores/class/getByCodeName/<code>/<name>', methods = ['POST'])
def getByCodeName(code, name):
    try:
        if request.method == 'POST':
            return ClassHandler().getByCodeName(code, name)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/losprogramadores/class/getClassSections/<int:cid>', methods=['POST'])
def getClassSections(cid):
    try:
        if request.method == 'POST':
            return ClassHandler().getClassSections(cid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
