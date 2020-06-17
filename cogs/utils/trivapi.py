"""Open Trivia DB Api
this code was made by niztg/nizcomix
contact him on discord ♿️niztg#7532 for questions
"""

import random
from html import unescape as unes

import requests


def link():
    url = "https://opentdb.com/api.php?amount=1"
    request = requests.get(url).json()
    return request


class TrivApi():
    def __init__(self):
        pass
    
    @property
    def question(self):
        return unes(link()['results'][0]['question'])
    
    @property
    def topic(self):
        return unes(link()['results'][0]['category'])
    
    @property
    def incorrect_answers(self):
        return unes(link()['results'][0]['incorrect_answers'])
    
    @property
    def correct_answer(self):
        return unes(link()['results'][0]['correct_answer'])
    
    @property
    def answer_format(self):
        an = []
        answers = [unes(answer) for answer in link()["results"][0]['incorrect_answers']]
        answers.append(unes(link()["results"][0]['correct_answer']))
        random.shuffle(answers)
        for numb, ans in enumerate(answers, 1):
            an.append(f'{numb}. **{ans}**')
        an = '\n'.join(an)
        return an
    
    @property
    def difficulty(self):
        return unes(link()['results'][0]['difficulty'])
