from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

stn = {
    "cozy":{"age":21, "stack":"front-end"},
    "ransford":{"age":21, "stack":"back-end api"},
    "dadson":{"age":28, "stack":"full-stack"},
}

class Hello(Resource):
    def get(self, name):
        return stn[name]

    def post(self):
        return {"data":"post-hello"}

api.add_resource(Hello, "/hello/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)