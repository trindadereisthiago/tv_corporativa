from flask import Blueprint, render_template
from infrastructure.weather_api import OpenWeatherAPI
from domain.weather_service import WeatherService
from dotenv import load_dotenv
import os
import json

router = Blueprint('router', __name__)

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
weather_repository = OpenWeatherAPI(api_key)
weather_service = WeatherService(weather_repository)

@router.route("/")
def index():
    weather_info = weather_service.get_weather_with_forecast("Jaragua do Sul")

    # Caminhos dos arquivos
    assets_path = os.path.join("assets", "assets.json")
    slides_extra_path = os.path.join("static", "config", "slides.json")

    # --- Carrega o assets.json (textos, imagens, etc.) ---
    with open(assets_path, "r", encoding="utf-8") as f:
        slides_data = json.load(f)

    slides = slides_data.get("slides", [])
    footer = slides_data.get("footer", "")

    # --- Carrega slides adicionais (vídeos) se existir ---
    if os.path.exists(slides_extra_path):
        with open(slides_extra_path, "r", encoding="utf-8") as f:
            extra_data = json.load(f)

        # aceita formato {"slides": [...]} ou {"videos": [...]}
        if isinstance(extra_data, dict):
            if "slides" in extra_data:
                slides.extend(extra_data["slides"])
            elif "videos" in extra_data:
                for v in extra_data["videos"]:
                    slides.append({"type": "video", "file": v["path"]})

     # --- Reposiciona a imagem para o final, se existir ---
    imagens = [s for s in slides if s.get("type") == "image"]
    outros = [s for s in slides if s.get("type") != "image"]
    slides = outros + imagens  # garante que as imagens fiquem por último
                
    return render_template("index.html", weather=weather_info, slides=slides, footer=footer)
