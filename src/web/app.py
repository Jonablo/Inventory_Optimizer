from flask import Flask
from src.web.api.optimization_routes import optimization_bp
from src.web.api.data_routes import data_bp

app = Flask(__name__)
app.register_blueprint(optimization_bp, url_prefix='/optimization')
app.register_blueprint(data_bp, url_prefix='/data')

if __name__ == '__main__':
    app.run(debug=True)
