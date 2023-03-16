
from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource
import map_manager as mm
import vehicle as rvt
import charger as chrg

app = Flask(__name__)
api = Api(app)

chrg.parse_charger_json()
mm.map_manager()
rvt.retrieve_vehicle_properties()

class Input(Resource):
    def post(self):
        data = request.get_json()
        mm.map_manager( data['city1'], data['city2'], data['carId'])
        return jsonify(data)

api.add_resource(Input, '/input')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

