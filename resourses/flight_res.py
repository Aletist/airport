from flask import jsonify
from flask_restful import Resource, abort, reqparse
from models.flight import db, Flight

db.create_all()

class FlightRes(Resource):

    def get(self, id):
        flight = Flight.query.get(id)
        if flight is None:
            abort(404)
        return jsonify(flight.serialize())

    def put(self, id):
        flight = Flight.query.get(id)
        if flight is None:
            abort(400)
        parser = reqparse.RequestParser()
        parser.add_argument('destination')
        parser.add_argument('carrier')
        parser.add_argument('terminal')
        parser.add_argument('status')
        parser.add_argument('is_arriving', type=bool)
        args = {k: v
                for k, v
                in parser.parse_args().items()
                if v is not None}
        if args.get('status') == 'unknown':
            args['status'] = None
        for key in args:
            setattr(flight, key, args[key])
        db.session.commit()
        return '', 200

    def delete(self, id):
        flight = Flight.query.get(id)
        if flight is None:
            abort(400)
        db.session.delete(flight)
        db.session.commit()
        return '', 204


class FlightsList(Resource):
    def get(self):
        query = Flight.query
        parser = reqparse.RequestParser()
        parser.add_argument('destination')
        parser.add_argument('carrier')
        parser.add_argument('terminal')
        parser.add_argument('status')
        parser.add_argument('is_arriving', type=bool)
        args = {k: v
                for k, v
                in parser.parse_args().items()
                if v is not None}
        if args.get('status') == 'unknown':
            args['status'] = None
        print(args)
        for attr in args:
            query = query.filter(getattr(Flight, attr) == args[attr])
        result = query.all()
        return jsonify([item.serialize() for item in result])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('destination', required=True)
        parser.add_argument('carrier', required=True)
        parser.add_argument('terminal', required=True)
        parser.add_argument('status', required=False)
        parser.add_argument('is_arriving', type=bool, required=True)
        args = parser.parse_args()
        flight = Flight(**args)
        db.session.add(flight)
        db.session.commit()
        return flight.id, 201
