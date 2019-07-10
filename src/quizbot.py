import quizlet
import re
import requests
from bs4 import BeautifulSoup
from time import sleep

client = quizlet.QuizletClient(client_id='')

def answer_file():
	with open('../resources/questions.txt') as file:
		questions = file.read().split('\n\n')

		answer(questions)

def answer_question(question):
	answer([question])

def answer(questions):
	for question in questions:
		soup = BeautifulSoup(requests.get(f'https://www.google.com/search?q=site:quizlet.com "{question}"').text, 'html.parser')

		def find_answer():
			for div in soup.find_all('div', attrs={'class': 'g'}):				
				try:
					set_ = client.api.sets(re.search('\d+', div.find('a')['href'][7:])[0]).get()

					for term in set_.terms:
						if question in term.term:
							print(questions.index(question) + 1, question, '\t\t', term.definition)

							return
				except TypeError:
					pass

		find_answer()
		sleep(2)

answer_file()
