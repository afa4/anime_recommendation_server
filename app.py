from flask import Flask, make_response, jsonify, request
import pandas as pd


class ModelServer:
    def __init__(self):
        self.model = pd.read_parquet('recommendation_cosine_matrix.parquet')
            
    
    def get_recommendation(self, anime_name, length = 20):
        recommendation = self.model[anime_name].sort_values(ascending=False)
        return recommendation.head(length)
        
        
model_server = ModelServer()
app = Flask(__name__)


@app.route('/recommendation')
def recommendation():
    anime_name = request.args.get('anime_name')
    if(anime_name is None):
        return make_response('Bad Request', 400)
    length = request.args.get('length', default=20, type=int)
    if length > 20:
        length = 20
    recommendation = model_server.get_recommendation(anime_name, length)
    
    return recommendation.to_json()


if __name__ == '__main__':
    print('Loading model...')
    from waitress import serve
    print('Model loaded. Serving app...')
    serve(app, host="0.0.0.0", port=8080)

 