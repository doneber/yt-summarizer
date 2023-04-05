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
def get_video_summary(video_id):
  captions = None
  try:
    captions = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en', 'es'])
  except Exception as e:
    return Response("Captions not available for the video", status=404)

  # concat and clean the captions
  caps_joined = ' '.join([i['text'] for i in captions[0][video_id]]).replace('\n', ' ')
  caps_joined = regex.sub(r'\[.*?\]', '', caps_joined)
  
  # then envarioment variable from openai
  openai.api_key = os.environ.get('OPENAI_API_KEY')
  summary_text = ""
  try:
    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {
            "role": "user",
            "content": "Summarize in Spanish the following text extracted of a YouTube video: \n" + caps_joined
          }
      ]
    )
    summary_text = res.choices[0].text
  except Exception as e:
    # return Response("OpenAI failed to generate summary", status=500)
    print("OpenAI failed to generate summary", e)
  data = {"data": summary_text, "captions": captions[0][video_id]}
  return jsonify(data)

if __name__ == '__main__':
    app.run(debug=DEBUG)
