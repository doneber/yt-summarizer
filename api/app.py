from flask import Flask, jsonify, request, Response
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS, cross_origin
import os
import cohere
import regex

app = Flask(__name__)
DEBUG = False
cors = CORS(app, resources={r"/api/*":{"origins":"*"}})

@app.route('/api/', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def welcome_api():
  return jsonify({"data": "Welcome to the API"})

@app.route('/api/<string:video_id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def get_video_captions(video_id):
  try:
    captions = YouTubeTranscriptApi.get_transcripts([video_id], languages=['en', 'es'])
    caps_joined = ' '.join([i['text'] for i in captions[0][video_id]]).replace('\n', ' ')
    # extract with regex everything between '[' and ']' and replace with ''
    caps_joined = regex.sub(r'\[.*?\]', '', caps_joined)

    COHERE_API_KEY = os.environ["COHERE_API_KEY"]
    co = cohere.Client(COHERE_API_KEY)
    prompt = f"""
    Extract the main ideas from the following text:

    text: In this video, we'll give you an overview of the captions editor in YouTube Studio which makes it easier to create and edit captions for your videos. When you add in captions, you may be able to reach a wider audience including deaf or hard-of-hearing viewers and viewers who speak another language. On average, videos that are captioned see an increase in watch time compared to videos that don't have them. There are two ways you can use the tool. While uploading your video or once your video has already been published. When you're uploading a video, you can get to the captions editor by looking for the Subtitles section and clicking Add on the Video Elements page. If you want to add captions to a video you've already uploaded go to the Subtitles page in YouTube Studio by clicking into it from the left-hand menu or from a specific video's Details page. Now that you know how to get to the captions editor let's walk through how to add captions and the different options you have to enter them. If the video already has automatic captions pre-populated and you'd like to make changes to them click Duplicate and Edit. If the video doesn't have automatic captions and you want to add your own click Add under the Subtitles column. If there's a specific language you'd like to add, click Add Language here. There are three ways you can add your own subtitles. You can upload a transcript paste captions from a transcript directly into the editor tool and sync them or type out the captions manually as you watch the video. To upload a transcript, select Upload file if you already have a file that contains formatted text of what's said in the video. When you choose this option, select if the file has timings or not which will allow YouTube to process the file correctly. If you want to paste captions in and sync them, select Auto-sync. With this option, you can paste in your full transcript of the video and subtitle timings will be set automatically. Once you paste your transcript here, click Assign Timings which will automatically set the caption timings for you. And finally select Type manually to create subtitles by typing them in as you watch the video. To the right of here, you can manually set the timings or delete the caption. To add additional captions, click Caption at the top or hover over the caption line and click the Add caption line icon. To give yourself more time to add in captions enable the Pause while typing option. You can also check out the keyboard shortcuts to make this faster and easier. For example, press Shift + Space to pause and resume your video. You have more control over timing your captions at the bottom of the editor. To better sync your captions they'll appear over the audio of your video as they're entered. You can click and drag the caption to move its position and also shorten or lengthen the caption. For even more control, you can zoom in and out on the captions timeline here. After your captions are added in, click Publish. You can always click Edit to make changes to your captions. If you have any questions about captions, let us know in the comments below. Thanks for watching.
    TLDR: The video provides an overview of the YouTube Studio's captions editor, which makes it easier to create and edit captions for videos. Captions can help reach a wider audience, including deaf or hard-of-hearing viewers and those who speak another language, and have been shown to increase watch time on average. The captions editor can be accessed while uploading the video or after it has been published. There are three ways to add captions: uploading a transcript, pasting captions from a transcript into the editor and syncing them, or typing out the captions manually as the video plays. The captions editor includes options for controlling timings, editing captions, and adding additional captions. The captions timeline can be zoomed in and out for more control, and the captions can be published or edited at any time.
    --
    text: python a high-level interpreted programming language famous for its zen-like code it's arguably the most popular language in the world because it's easy to learn yet practical for serious projects in fact you're watching this youtube video in a python web application right now it was created by guido van rossum and released in 1991 who named it after monty python's flying circus which is why you'll sometimes find spam and eggs instead of foo and bar in code samples it's commonly used to build server-side applications like web apps with the django framework and is the language of choice for big data analysis and machine learning many students choose python to start learning to code because of its emphasis on readability as outlined by the zen of python beautiful is better than ugly while explicit is better than implicit python is very simple but avoids the temptation to sprinkle in magic that causes ambiguity its code is often organized into notebooks where individual cells can be executed then documented in the same place we're currently at version 3 of the language and you can get started by creating a file that ends in py or ipymb to create an interactive notebook create a variable by setting a name equal to a value it's strongly typed which means values won't change in unexpected ways but dynamic so type annotations are not required the syntax is highly efficient allowing you to declare multiple variables on a single line and define tuples lists and dictionaries with a literal syntax semicolons are not required and if you use them and experience pythonista will say that your code is not pythonic instead of semicolons python uses indentation to terminate or determine the scope of a line of code define a function with the def keyword then indent the next line usually by four spaces to define the function body we might then add a for loop to it and indent that by another four spaces this eliminates the need for curly braces and semicolons found in many other languages python is a multi-paradigm language we can apply functional programming patterns with things like anonymous functions using lambda it also uses objects as an abstraction for data allowing you to implement object-oriented patterns with things like classes and inheritance it also has a huge ecosystem of third-party libraries such as deep learning frameworks like tensorflow and wrappers for many high performance low level packages like open computer vision which are most often installed with the pip package manager this has been the python programming language in 100 seconds hit the like button if you want to see more short videos like this thanks for watching and i will see you in the next one
    TLDR: Python is a high-level interpreted programming language that is easy to learn and practical for serious projects. It was created by Guido van Rossum and released in 1991 and was named after Monty Python's Flying Circus. Python is widely used for building server-side applications, big data analysis, and machine learning. Its emphasis on readability, as outlined by the Zen of Python, makes it a popular choice for students to start learning to code. The syntax is efficient and organized into notebooks, where individual cells can be executed and documented. Python is a multi-paradigm language, allowing for functional programming and object-oriented patterns. It has a large ecosystem of third-party libraries and is installed using the pip package manager.
    --
    text: """+ caps_joined + "\n    TLDR: "
    res = co.generate(
      model='xlarge', 
      prompt = prompt,
      max_tokens= 120, 
      temperature=3,
      stop_sequences=["--"],
      truncate='END')

    if(request.method == 'GET'):
      summary_text = res.generations[0].text.replace('\n', '')
      data = { "data": summary_text, "prompt": prompt }
      print(prompt)
      return jsonify(data)
  except Exception as e:
    # respond with http code status error
    print(e)
    return Response(e, status=409)
  
  
if __name__ == '__main__':
    app.run(debug=DEBUG)
