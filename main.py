from flask import Flask, request
import logging
import json
from googletrans import Translator

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

translator = Translator()

@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Response: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я умею переводить слова. Скажи: Переведи слово *слово*'
        return
        text = req['request']['original_utterance'].lower()
        if "переведи слово" in text or "переведи" in text :
            words = text.split()
            if len(words) > 3:
                word_to_translate = words[-1]
                translation = translator.translate(word_to_translate, dest='en', src='ru')
                res['response']['text'] = translation.text
            else:
                res['response']['text'] = "Я не поняла какое слово нужно перевести"

if __name__ == '__main__':
    app.run()
