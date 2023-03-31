from flask import Flask, jsonify, request, Response
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS, cross_origin
import os
import regex
import openai

app = Flask(__name__, static_folder='../frontend/dist' ,static_url_path="/")
DEBUG = False
cors = CORS(app, resources={r"/api/*":{"origins":"*"}})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")

@app.route('/api/', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def welcome_api():
  return jsonify({"data": "Welcome to the API"})

@app.route('/api/<string:video_id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_video_captions(video_id):
  try:
    captions = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en', 'es'])
    captions = captions[0][video_id]
    caps_joined = ' '.join([i['text'] for i in captions]).replace('\n', ' ')
    # extract with regex everything between '[' and ']' and replace with ''
    caps_joined = regex.sub(r'\[.*?\]', '', caps_joined)

    openai.api_key = os.environ["OPENAI_API_KEY"]
    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages = [
        {
            "role": "user",
            "content" : "Resume en español el siguiente texto que fue extraido de los subtitulos de un video de YouTube: \n" + caps_joined
        }
      ]
    )
    if(request.method == 'GET'):
      summary_text = res.choices[0].message.content
      data = { "data": summary_text, "captions": captions}
      return jsonify(data)
  except Exception as e:
    # respond with http code status error
    return Response(e, status=409)
  
  
if __name__ == '__main__':
    app.run(debug=DEBUG)
