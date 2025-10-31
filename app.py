from flask import Flask
from presentation.routes import router
import os

# Caminho correto para a pasta templates dentro do módulo presentation
template_folder = os.path.join(os.path.dirname(__file__), "presentation", "templates")

app = Flask(__name__, template_folder=template_folder)

app.register_blueprint(router)

if __name__ == "__main__":
    app.run(debug=True)
