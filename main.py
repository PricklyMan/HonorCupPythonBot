# -*- coding: utf-8 -*-
"""
Created on 10/22/2020 12:09 PM

@author: N. Amelchenko
"""

# pip install selenium
# download geckodriver (https://github.com/mozilla/geckodriver/releases)


from selenium import webdriver
import time

# first of all, get a token

TOKEN = 'https://quiz.honorcup.ru/app/?id=57706&sign=3517a7ae6a591d938f0bd30d43a5340d'

# open a browser (FireFox)
browser = webdriver.Firefox(executable_path='geckodriver.exe')
browser.get(TOKEN)
time.sleep(2)
# #click battle_button
battle_button = browser.find_element_by_class_name('about__buttons')
battle_button.click()
time.sleep(2)

# #choose a category and theme
category = browser.find_elements_by_class_name('slider__item')
category[3].click()

theme = browser.find_elements_by_class_name('profile__theme')
theme[1].click()

categories_play_button = browser.find_element_by_xpath(
    '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div')  # ('button-group-2x')
categories_play_button.click()


def play(s1=None):
    for i in range(5):

        k = 0
        round_question = browser.find_element_by_class_name('game__question-text')
        round_answers = browser.find_elements_by_class_name('game__answer')
        s = round_question.text
        s0 = s
        f = open('base.txt', 'r')
        for line in f:
            if line.startswith(s):
                print('****')
                k = 1
                for ij in range(4):

                    s1 = round_answers[ij].text + '\n'
                    if line.endswith(s1):
                        round_answers[ij].click()
                        time.sleep(35)
                        break
        f.close()
        if k == 0:  # Проверяем отсутствие ответа в базе данных
            points = browser.find_elements_by_class_name('game__user-value')
            print(points[0].text, '<<до ответа')
            a = int(points[0].text)
            p = int(0)

            def skip():  # функция, которая пропускает вариант ответа, основываясь на предыдущих ошибках

                nonlocal p
                s1 = round_answers[p].text + '\n'
                f = open('base_of_wrong.txt', 'r')
                z=0
                for line in f:
                    if line.startswith(s):
                      if line.endswith(s1):
                        print('ПРОПУСКАЕМ')
                        z=1
                if z==1: p=p+1

                f.close()

            skip()
            print(p)
            skip()
            print(p)
            skip()


            round_answers[p].click() #кликаем туда, куда еще не кликали
            time.sleep(1)
            points1 = browser.find_elements_by_class_name('game__user-value')
            print(round_question.text)
            print(round_answers[0].text)
            b = int((points1[0].text))
            print('A=', a, 'B=', b)
            if b > a: #если ответ верный дописываем его в базу данных
                f = open('base.txt', 'a')
                otvet = round_question.text + ' Ответ: ' + round_answers[p].text + '\n'
                f.write(otvet)
                f.close()
            else:
                f = open('base_of_wrong.txt', 'a')
                otvet = round_question.text + ' Ответ: ' + round_answers[p].text + '\n'
                f.write(otvet)
                f.close()

            time.sleep(35)


for j in range(10000): #играем викторину условно 10к раз
    time.sleep(25)
    play()
    one_more = browser.find_elements_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[1]')
    one_more[0].click()
