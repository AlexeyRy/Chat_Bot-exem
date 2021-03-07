import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from config import main_token

vk_session = vk_api.VkApi(token=main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


class User:
	def __init__(self, id, mode, status):
		self.id = id
		self.mode = mode
		self.status = status


# ChatBot keyboard
def get_but(text, color):
	return {
		"action": {
			"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"
		},
		"color": f"{color}"
	}


menu_key = {
	"one_time": False,
	"buttons": [
		[get_but("Пройти тестирование", "positive")],
		[get_but("Статус подготовки", "positive")]
	]
}
menu_key = json.dumps(menu_key, ensure_ascii=False).encode('utf-8')
menu_key = str(menu_key.decode('utf-8'))

test_key = {
	"one_time": False,
	"buttons": [
		[get_but("Не знаю", "negative")],
		[get_but("Главное меню", "positive")]
	]
}
test_key = json.dumps(test_key, ensure_ascii=False).encode('utf-8')
test_key = str(test_key.decode('utf-8'))

answer_key = {
	"one_time": False,
	"buttons": [
		[get_but("Да, знаком", "positive")],
		[get_but("Нет, не знаком", "negative")],
		[get_but("Главное меню", "positive")]
	]
}
answer_key = json.dumps(answer_key, ensure_ascii=False).encode('utf-8')
answer_key = str(answer_key.decode('utf-8'))

answer_key2 = {
	"one_time": False,
	"buttons": [
		[get_but("Не знаю, как это решать", "negative")],
		[get_but("Главное меню", "positive")]
	]
}
answer_key2 = json.dumps(answer_key2, ensure_ascii=False).encode('utf-8')
answer_key2 = str(answer_key2.decode('utf-8'))


def send(id, text, keyboard):
	session_api.messages.send(user_id=id, message=text, random_id=0, keyboard=keyboard)


def send_photo(id, url):
	session_api.messages.send(user_id=id, attachment=url, random_id=0)


users = []
trueAnswere = 0
var = 0
number = 0
to_do = 1
falseToDo = 0
repair = 1
listTrueOrFalse = []
sch = 0
phr = ''

for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW:
		if event.to_me:
			message = event.text.lower()
			id = event.user_id

			if message == 'начать' or message == 'главное меню':
				flag1 = 0
				for user in users:
					if user.id == id:
						send(id, 'Выберите действие', menu_key)
						user.mode = 'menu'
						flag1 = 1
				if flag1 == 0:
					users.append(User(id, 'menu', 0))
					send(id, 'Выберите действие', menu_key)

			for user in users:
				if user.id == id:

					if user.mode == 'menu':

						if message == 'пройти тестирование':
							send(id, "Начнём!", answer_key)
							user.mode = 'test'

						if message == "статус подготовки":
							send(id, f'Ты можешь решить: {user.status}', menu_key)
							print(user.status)

					if user.mode == 'test':
						if var == 0:
							if number == 0:

								if to_do == 1:
									send(id, "Ты знаком с темой - Количественные параметры информационных объектов?", answer_key)
									to_do = 0

								if message == "да, знаком":
									repair = 1
									send(id, "Попробуй решить задание \n"
											 "В одной из кодировок Unicode каждый символ кодируется 16 битами. Ваня написал текст (в нём нет лишних пробелов):\n\n"
											 "«Лев, тигр, ягуар, гепард, пантера, ягуарунди — кошачьи».\n\n"
											 "Ученик вычеркнул из списка название одного из представителей семейства кошачьих. Заодно он вычеркнул ставшие лишними запятые и пробелы — два пробела не должны идти подряд.\n"
											 "При этом размер нового предложения в данной кодировке оказался на 14 байт меньше, чем размер исходного предложения. Напишите в ответе вычеркнутое название представителя семейства кошачьих.", answer_key2)

								if message == "ягуар":
									send(id, "Это правильный ответ! Перейдём к следующему заданию", answer_key)
									user.status += 1
									number = 1
									to_do = 1
									listTrueOrFalse.append(1)

								if message != "ягуар" and message != "нет, не знаком" and message != "не знаю, как это решать" and message != "да, знаком" and message != "главное меню" and message != "пройти тестирование" and message != "статус подготовки":
									send(id, "Этот  ответ не правльный. Перейдём к следующему заданию", answer_key2)
									number = 1
									to_do = 1
									listTrueOrFalse.append(0)

								if message == "нет, не знаком":
									repair = 1
									send(id, "Попробуй решить задание \n"
											 "В одной из кодировок Unicode каждый символ кодируется 16 битами. Ваня написал текст (в нём нет лишних пробелов):\n\n"
											 "«Лев, тигр, ягуар, гепард, пантера, ягуарунди — кошачьи».\n\n"
											 "Ученик вычеркнул из списка название одного из представителей семейства кошачьих."
											 "Заодно он вычеркнул ставшие лишними запятые и пробелы — два пробела не должны идти подряд.\n"
											 "При этом размер нового предложения в данной кодировке оказался на 14 байт меньше, чем размер исходного предложения."
											 "Напишите в ответе вычеркнутое название представителя семейства кошачьих.", answer_key2)

								if message == "не знаю, как это решать" and repair == 1:
									send(id, "Хорошо. Перейдём к следующему заданию", answer_key)
									number = 1
									to_do = 1
									repair = 0
									listTrueOrFalse.append(0)

								if message == "главное меню":
									user.mode = 'menu'
									number = 0
									to_do = 1
									send(id, "Прекращаем тестирование", menu_key)

							if number == 1:

								if to_do == 1:
									send(id, "Ты знаком с темой - Кодирование и декодирование информации?", answer_key)
									to_do = 0

								if message == "да, знаком":
									repair = 1
									send(id, "попробуй решить это задание", answer_key2)
									send(id, 'Валя шифрует русские слова (последовательности букв), записывая вместо каждой буквы её код:\n\n'
											 'А = 01\n'
											 'Д = 100\n'
											 'К = 101\n'
											 'Н = 10\n'
											 'О = 111\n'
											 'С = 000\n\n'
											 'Некоторые цепочки можно расшифровать не одним способом. Например, 00010101 может означать не только СКА, но и СНК. Даны три кодовые цепочки:\n\n'
											 '10111101\n'
											 '1010110\n'
											 '10111000\n\n'
											 'Найдите среди них ту, которая имеет только одну расшифровку, и запишите в ответе расшифрованное слово.', answer_key2)
									falseToDo = 1

								if message == "нос":
									send(id, "Это правильный ответ! Перейдём к следующему заданию", answer_key)
									user.status += 1
									number = 2
									to_do = 1
									listTrueOrFalse.append(1)
									falseToDo = 0

								if falseToDo == 1:
									if message != "ягуар" and message != "нет, не знаком" and message != "не знаю, как это решать" and message != "да, знаком" and message != "главное меню" and message != "пройти тестирование" and message != "статус подготовки":
										send(id, "Этот  ответ не правльный. Перейдём к следующему заданию", answer_key2)
										number = 2
										to_do = 1
										listTrueOrFalse.append(0)
										falseToDo = 0

								if message == "нет, не знаком":
									repair = 1
									send(id, "Попробуй решить задание", answer_key2)
									send(id,
										 'Валя шифрует русские слова (последовательности букв), записывая вместо каждой буквы её код:\n\n'
										 'А = 01\n'
										 'Д = 100\n'
										 'К = 101\n'
										 'Н = 10\n'
										 'О = 111\n'
										 'С = 000\n\n'
										 'Некоторые цепочки можно расшифровать не одним способом. Например, 00010101 может означать не только СКА, но и СНК. Даны три кодовые цепочки:\n\n'
										 '10111101\n'
										 '1010110\n'
										 '10111000\n\n'
										 'Найдите среди них ту, которая имеет только одну расшифровку, и запишите в ответе расшифрованное слово.',
										 answer_key2)
									falseToDo = 1

								if message == "главное меню":
									number = 0
									to_do = 1
									falseToDo = 0
									user.mode = 'menu'
									send(id, "Прекращаем тестирование", menu_key)

								if message == "не знаю, как это решать" and repair == 1:
									send(id, "Хоршо, перейдём к следующему вопросу", answer_key)
									number = 2
									to_do = 1
									repair = 0
									falseToDo = 0
									listTrueOrFalse.append(0)

							if number == 2:
								print(falseToDo)
								if to_do == 1:
									send(id, "Ты знаком с темой - Значение логического выражения?", answer_key)
									to_do = 0

								if message == "да, знаком":
									repair = 1
									send(id, "попробуй решить это задание", answer_key2)
									send(id, 'Напишите наименьшее целое число x, для которого истинно высказывание:\n\n'
											 'НЕ (X < 2) И (X < 5).', answer_key2)
									falseToDo = 1

								if message == "2":
									send(id, "Это правильный ответ! Перейдём к следующему заданию", answer_key)
									user.status += 1
									number = 3
									to_do = 1
									listTrueOrFalse.append(1)
									falseToDo = 0

								if falseToDo == 1:
									if message != "2" and message != "нет, не знаком" and message != "не знаю, как это решать" and message != "да, знаком" and message != "главное меню":
										send(id, "Этот  ответ не правльный. Перейдём к следующему заданию", answer_key2)
										number = 3
										to_do = 1
										listTrueOrFalse.append(0)
										falseToDo = 0

								if message == "нет, не знаком":
									repair = 1
									send(id, "Попробуй решить задание", answer_key2)
									send(id, 'Напишите наименьшее целое число x, для которого истинно высказывание:\n\n'
											 'НЕ (X < 2) И (X < 5).', answer_key2)
									falseToDo = 1

								if message == "главное меню":
									number = 0
									to_do = 1
									user.mode = 'menu'
									send(id, "Прекращаем тестирование", menu_key)
									falseToDo = 0

								if message == "не знаю, как это решать" and repair == 1:
									send(id, "Хоршо, перейдём к следующему вопросу", answer_key)
									number = 3
									to_do = 1
									repair = 0
									listTrueOrFalse.append(0)
									falseToDo = 0

							if number == 3:
								print(falseToDo)

								if to_do == 1:
									send(id, "Ты знаком с темой - Формальные описания реальных объектов и процессов?", answer_key)
									to_do = 0

								if message == "да, знаком":
									repair = 1
									send(id, "попробуй решить это задание", answer_key2)
									send(id, 'Между населёнными пунктами А, В, С, D, Е построены дороги, протяжённость которых (в километрах) приведена в таблице:\n\n', answer_key2)
									send_photo(id, 'photo-202414453_457239018')
									send(id, 'Определите длину кратчайшего пути между пунктами А и E. Передвигаться можно только по дорогам, протяжённость которых указана в таблице.', answer_key2)
									falseToDo = 1

								if message == "6":
									send(id, "Это правильный ответ! Перейдём к следующему заданию", answer_key)
									user.status += 1
									number = 4
									to_do = 1
									listTrueOrFalse.append(1)
									falseToDo = 0

								if falseToDo == 1:
									if message != "6" and message != "нет, не знаком" and message != "не знаю, как это решать" and message != "да, знаком" and message != "главное меню":
										send(id, "Этот  ответ неправльный. Перейдём к следующему заданию", answer_key2)
										number = 4
										to_do = 1
										listTrueOrFalse.append(0)
										falseToDo = 0

								if message == "нет, не знаком":
									repair = 1
									send(id,'Между населёнными пунктами А, В, С, D, Е построены дороги, протяжённость которых (в километрах) приведена в таблице:\n\n', answer_key2)
									send_photo(id, 'photo-202414453_457239018')
									send(id, 'Определите длину кратчайшего пути между пунктами А и E. Передвигаться можно только по дорогам, протяжённость которых указана в таблице.', answer_key2)
									falseToDo = 1

								if message == "главное меню":
									number = 0
									to_do = 1
									user.mode = 'menu'
									send(id, "Прекращаем тестирование", menu_key)
									falseToDo = 0

								if message == "не знаю, как это решать" and repair == 1:
									send(id, "Хоршо, перейдём к следующему вопросу", answer_key)
									number = 4
									to_do = 1
									repair = 0
									listTrueOrFalse.append(0)
									falseToDo = 0

							if number == 4:
								print(falseToDo)

								if to_do == 1:
									send(id, "Ты знаком с темой - Простой линейный алгоритм для формального исполнителя?",answer_key)
									to_do = 0

								if message == "да, знаком":
									repair = 1
									send(id, "попробуй решить это задание", answer_key2)
									send(id, "У исполнителя Альфа две команды, которым присвоены номера:\n\n"
											 "1. прибавь 1;\n"
											 "2. умножь на b\n\n"
											 "(b — неизвестное натуральное число; b ≥ 2).\n"
											 "Выполняя первую из них, Альфа увеличивает число на экране на 1, а выполняя вторую, умножает это число на b. Программа для исполнителя Альфа — это последовательность номеров команд. Известно, что программа 11211 переводит число 6 в число 82. Определите значение b.", answer_key2)
									falseToDo = 1

								if message == "10":
									send(id, "Это правильный ответ! Перейдём к следующему заданию", answer_key)
									user.status += 1
									number = 0
									var = 1
									to_do = 1
									listTrueOrFalse.append(1)
									falseToDo = 0
									user.mode = 'menu'
									for i in range(0, 4):

										#for j in listTrueOrFalse:
										#	print(listTrueOrFalse[i])
										#	print(bool(listTrueOrFalse[i]))

										if len(phr) == 0:
											for l in range(0, 5):
												blist = bool(listTrueOrFalse[l])
												phr = phr + str(l + 1) + " " + str(blist) + " "
											send(id, phr, menu_key)


										if bool(listTrueOrFalse[i]) == False:
											if i == 0:
												send(id, 'Ты не справился с первым заданием. Тебе стоит пройти первую неделю курса в Stepik', menu_key)
												sch = 1

											if i == 1:
												if sch == 0:
													send(id, 'Ты не справился со вторым заданием. Подтяни свои знания на второй неделе курса', menu_key)
													sch = 1
												else:
													send(id, 'Так же тебе стоит посмтореть вторую неделю курса', menu_key)
													sch = 2

											if i == 2:
												if sch == 0:
													send(id, 'Ты ошибся в третьем задании. Эта тема обьясняеться на четвёртой неделе курса в первом видеоролеке', menu_key)
													sch = 1
												elif sch == 1:
													send(id, 'Так же ты допустил ошибку в третьем задание. Эта тема разбиралась на четвёртой неделе курса в первом видео', menu_key)
													sch = 2
												else:
													send(id, 'Ошибка так же есть в третьем. Это задание мы так же разбирале в stepik на 4 неделе в первом видео ролике', menu_key)

											if i == 3:
												if sch == 0:
													pass
											if i == 4:
												pass

								if falseToDo == 1:
									if message != "10" and message != "нет, не знаком" and message != "не знаю, как это решать" and message != "да, знаком" and message != "главное меню":
										send(id, "Этот  ответ не правльный. Перейдём к следующему заданию", answer_key2)
										number = 0
										to_do = 1
										listTrueOrFalse.append(0)
										falseToDo = 0
										user.mode = 'menu'
										for i in range(0, 4):

											#for j in listTrueOrFalse:
											#	print(listTrueOrFalse[i])
											#	print(bool(listTrueOrFalse[i]))

											if len(phr) == 0:
												for l in range(0, 5):
													blist = bool(listTrueOrFalse[l])
													phr = phr + str(l + 1) + " " + str(blist) + " "
												send(id, phr, menu_key)


											if bool(listTrueOrFalse[i]) == False:
												if i == 0:
													send(id, 'Ты не справился с первым заданием. Тебе стоит пройти первую неделю курса в Stepik', menu_key)
													sch = 1

												if i == 1:
													if sch == 0:
														send(id, 'Ты не справился со вторым заданием. Подтяни свои знания на второй неделе курса', menu_key)
														sch = 1
													else:
														send(id, 'Так же тебе стоит посмтореть вторую неделю курса', menu_key)
														sch = 2

												if i == 2:
													if sch == 0:
														send(id, 'Ты ошибся в третьем задании. Эта тема обьясняеться на четвёртой неделе курса в первом видеоролеке', menu_key)
														sch = 1
													elif sch == 1:
														send(id, 'Так же ты допустил ошибку в третьем задание. Эта тема разбиралась на четвёртой неделе курса в первом видео', menu_key)
														sch = 2
													else:
														send(id, 'Ошибка так же есть в третьем. Это задание мы так же разбирале в stepik на 4 неделе в первом видео ролике', menu_key)

												if i == 3:
													send(id, "Тебе стоит посмотреть 1 видео 4 недели на курсе в  stepik", menu_key)
												if i == 4:
													send(id, "Тебе стоит посмотреть видео урок на 5 недели на курсе в  stepik")

								if message == "нет, не знаком":
									repair = 1
									send(id, "У исполнителя Альфа две команды, которым присвоены номера:\n\n"
											 "1. прибавь 1;\n"
											 "2. умножь на b\n\n"
											 "(b — неизвестное натуральное число; b ≥ 2).\n"
											 "Выполняя первую из них, Альфа увеличивает число на экране на 1, а выполняя вторую, умножает это число на b. Программа для исполнителя Альфа — это последовательность номеров команд. Известно, что программа 11211 переводит число 6 в число 82. Определите значение b.",
											answer_key2)
									falseToDo = 1

								if message == "главное меню":
									number = 0
									to_do = 1
									falseToDo = 0
									user.mode = 'menu'
									send(id, "Прекращаем тестирование", menu_key)

								if message == "не знаю, как это решать" and repair == 1:
									send(id, "Хоршо, это было последне задание в бэто версии чат-бота", answer_key)
									number = 0
									to_do = 1
									repair = 1
									listTrueOrFalse.append(0)
									falseToDo = 0
									user.mode = 'menu'
									send(id, "Прекращаем тестирование", menu_key)
									for i in range(0, 4):

										#for j in listTrueOrFalse:
										#	print(listTrueOrFalse[i])
										#	print(bool(listTrueOrFalse[i]))

										if len(phr) == 0:
											for l in range(0, 5):
												blist = bool(listTrueOrFalse[l])
												phr = phr + str(l + 1) + " " + str(blist) + " "
											send(id, phr, menu_key)


										if bool(listTrueOrFalse[i]) == False:
											if i == 0:
												send(id, 'Ты не справился с первым заданием. Тебе стоит пройти первую неделю курса в Stepik', menu_key)
												sch = 1

											if i == 1:
												if sch == 0:
													send(id, 'Ты не справился со вторым заданием. Подтяни свои знания на второй неделе курса', menu_key)
													sch = 1
												else:
													send(id, 'Так же тебе стоит посмтореть вторую неделю курса', menu_key)
													sch = 2

											if i == 2:
												if sch == 0:
													send(id, 'Ты ошибся в третьем задании. Эта тема обьясняеться на четвёртой неделе курса в первом видеоролеке', menu_key)
													sch = 1
												elif sch == 1:
													send(id, 'Так же ты допустил ошибку в третьем задание. Эта тема разбиралась на четвёртой неделе курса в первом видео', menu_key)
													sch = 2
												else:
													send(id, 'Ошибка так же есть в третьем. Это задание мы так же разбирале в stepik на 4 неделе в первом видео ролике', menu_key)

											if i == 3:
												send(id, "Советую пройти на 3 неделе курса", menu_key)
											if i == 4:
												send(id, "Советую пройти на 5 неделе курса", menu_key)


#-- https://stepik.org/lesson/475418/step/1?unit=466309
