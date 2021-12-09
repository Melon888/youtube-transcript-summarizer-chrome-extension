from flask import Flask, jsonify, request, Response
from youtube_transcript_api import YouTubeTranscriptApi
import json
from flask_cors import CORS
from transformers import pipeline

video_link = "https://www.youtube.com/watch?v=FVsI1AgyxGM&t=128s"


# video_id = video_link.split("=")[1]


def converter(transcript):
    result = ""
    for x in transcript:
        text_string = json.dumps(x)
        text_dict = json.loads(text_string)
        # print(text_dict["text"])
        result += (text_dict["text"])
        result += " "

    return result


# print(summarizer(original_text, max_length=130, min_length=30, do_sample=False))

def summarizeAll(original_text):
    summarizer = pipeline("summarization")
    lenofScript = len(original_text)
    length = int(len(original_text)/1000)

    summary_text = ""
    text = ""
    for eachLine in range(0, length+1):
        start = 0
        start = eachLine*1000
        end = (eachLine+1)*1000
        if end > lenofScript:
            end = lenofScript

        text = original_text[start:end]
        # print("eachLine-text:",text)

        # print(summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text'])
        summary_text += summarizer(text, max_length=130,
                                   min_length=30, do_sample=False)[0]['summary_text']

    return summary_text


# summary_text = summarization(original_text)[0]['summary_text']
# print("Summary:", summary_text)


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})


@app.route('/', methods=['Post', 'GET'])
def index():
    if False:
        return jsonify({"result": "failure", "error": "401", "message": "unauthorized"}), 401
    print("Succesfull!!! HTTP code 200")
    requestUrl = request.url
    print(requestUrl)
    # video = requestUrl.rfind("=")
    # video_id = requestUrl[video+1:]

    video = requestUrl.find("=")
    print(video)
    video_first = requestUrl[video+1:]
    print(video_first)
    video_1 = video_first.find("=")
    print(video_1)
    video_2 = video_first.rfind("=")
    print(video_2)

    if video_1 != video_2:
        video_id = video_first[video_1+1:video_2]
    else:
        video_id = video_first[video_1+1:]

    #video_id = requestUrl.rsplit("=")[1]
    print("video id is:")
    print(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # using pipeline API for summarization task
    # summarizer = pipeline("summarization")
    script = converter(transcript)

    summary_text = summarizeAll(script)

    print("transcript is ready!!!!!")
    return summary_text


@app.route('/test', methods=['GET'])
def get_url():
    return "hey"


if __name__ == "__main__":
    app.run(debug=True, port=8000)


# def converter_to_summary(video_id):