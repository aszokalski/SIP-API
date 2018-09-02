#!/usr/bin/python
# import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
from urllib import parse
#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

#initial variables
app = Flask(__name__)
version = 1.1

#functions
def przystanek(id):
    try:
        browser = webdriver.Chrome('{path-to-chromedriver}')
        browser.set_window_size(1120, 550)
        browser.get('https://tw.waw.pl/sip/?#/przystanek/'+str(id))
        element = WebDriverWait(browser, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sip-timetable-content'))
        )
    except:
        browser.quit()
        print ("Selenium error:", sys.exc_info()[0])
        return -1
    else:
        try:
            array = '{"'+str(id)+'": [ '
            search = 1
            i = 1
            while(search):
                i += 1
                dir = "//div[@class='sip-timetable-content']/table[1]/tbody[1]/tr["+str(i)+"]"
                try:
                    linia = int(browser.find_element_by_xpath(dir+"/td[1]").text)
                except:
                    search = 0
                    array = array[:-1]
                else:
                    kierunek = browser.find_element_by_xpath(dir+"/td[2]").text
                    czas = browser.find_element_by_xpath(dir+"/td[5]").text
                    array += '{"linia": "'+str(linia)+'", "kierunek": "'+str(kierunek)+'", "czas_do_odjazdu": "'+str(czas)+'"}'
                    array += ','
            browser.quit()
            array += ' ] }'
        except:
            browser.quit()
            print ("Not found:", sys.exc_info()[0])
            return -1
        else:
            try:
                data = json.loads(array)
                return data
            except:
                print ("JSON error:", sys.exc_info()[0])
                return -2



#api
@app.route('/sip/api/v'+str(version)+'/przystanek/<int:task_id>', methods=['GET'])
def get_task(task_id):
    dat = przystanek(task_id)
    if type(dat) is int:
        if dat == -1:
            abort(404)
        elif dat== -2:
            abort(500)
    return jsonify(dat)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

if __name__ == '__main__':
    app.run(debug=True)
