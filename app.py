from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import sys
sys.path.append('./app/')
from backend.crossword.main import Crossword_Generator

# instantiate the app
app = Flask(__name__, static_folder='app', static_url_path="/")
app.config.from_object(__name__)
app.config['DEBUG'] = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def home_page():
  return app.send_static_file("views/index.html")

@app.route("/clues", methods=['POST'])
def get_grid_specs():
  res = request.json
  
  if not(res.get('theme') and res.get('dimensions') and res.get('level')):
    return jsonify({'error': "Data are not valid"})

  INPUT_THEME = res.get('theme')
  GRID_SIZE = res.get('dimensions')
  # IS_LEVEL_EASY = res.get('level') == 'Easy'
  IS_LEVEL_EASY = True
  
  cross_gen = Crossword_Generator(INPUT_THEME, GRID_SIZE, IS_LEVEL_EASY)
  cross_gen.begin_generate()
  cross_data = cross_gen.adjust_answers_to_clues()

  json_results = jsonify({
    'grid': cross_gen.grid,
    'answers': cross_data
  })

  # print(json_results)
  return json_results

if __name__ == '__main__':
  app.run()