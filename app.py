from flask_restful import Api
from models.flight import app
from resourses.flight_res import *

api = Api(app)

api.add_resource(FlightRes, '/flights/<id>')
api.add_resource(FlightsList, '/flights')


if __name__ == '__main__':
    app.run(debug=True)
