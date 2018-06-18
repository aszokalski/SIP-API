# import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
#!flask/bin/python
from flask import Flask, jsonify, abort, make_response

#initial variables
app = Flask(__name__)

#functions
def przystanek(id):
    browser = webdriver.Chrome('{path-to-chromedriver}')
    browser.set_window_size(1120, 550)
    browser.get('https://tw.waw.pl/sip/?#/przystanek/'+str(id))
    element = WebDriverWait(browser, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, 'sip-timetable-content'))
    )
    array = '{"'+str(id)+'": [ '
    for i in range(2,8):
        dir = "//div[@class='sip-timetable-content']/table[1]/tbody[1]/tr["+str(i)+"]"
        linia = int(browser.find_element_by_xpath(dir+"/td[1]").text)
        kierunek = browser.find_element_by_xpath(dir+"/td[2]").text
        czas = browser.find_element_by_xpath(dir+"/td[5]").text
        array += '{"linia": "'+str(linia)+'", "kierunek": "'+str(kierunek)+'", "czas_do_odjazdu": "'+str(czas)+'"}'
        if (i != 7):
            array += ','
    browser.quit()
    array += ' ] }'
    data = json.loads(array)
    return data

#api
@app.route('/sip/api/v1.0/przystanek/<int:task_id>', methods=['GET'])
def get_task(task_id):
    dat = przystanek(task_id)
    if len(dat) == 0:
        abort(404)
    return jsonify(dat)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
