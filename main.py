import os
import random
import time
import re
import pyperclip
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from constants import *
from progSetup import *

gen_text: str
s_text: list


def navigate_to_main_page():
    driver.get(MAIN_PAGE_LINK)
    # accept cookie policy
    perform_btn_click(ACCEPT_COOKIE_BTN)
    # scroll to text generator area
    do_scroll(TEXT_GENERATOR_WINDOW)


def close_add():
    time.sleep(2)
    wait.until(EC.element_to_be_clickable(driver.find_element(By.XPATH, CLOSE_ADD_BTN)))
    perform_btn_click(CLOSE_ADD_BTN)


def perform_btn_click(xpath):
    if driver.find_element(By.XPATH, xpath):
        actions.click(driver.find_element(By.XPATH, xpath)).perform()
        actions.release()


def do_scroll(xpath):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    s_block = driver.find_element(By.XPATH, xpath)
    cord = s_block.location.values()

    driver.execute_script(f"window.scroll({cord.mapping.get('x')}, {cord.mapping.get('y')});")


def generate_input_values():
    sen_arr = ['p', 's', 'w']
    n = random.randint(2, 10)
    x = sen_arr[random.randint(0, 2)]
    set_input_values(n, x)


def fill_input_field(name, value):
    try:
        actions.send_keys_to_element(driver.find_element(By.XPATH, name), value).perform()
        actions.release()
    except NoSuchElementException:
        print('Cant\'t find element by XPATH: ' + name)


def set_selector(x):
    sen_dropdown = driver.find_element(By.XPATH, X_INPUT)
    sen_dropdown.click()
    select = Select(sen_dropdown)
    select.select_by_value(x)


def set_input_values(n, x):
    close_add()
    driver.find_element(By.XPATH, N_INPUT).clear()
    perform_keyboard_press()
    fill_input_field(N_INPUT, n)
    set_selector(x)


def perform_keyboard_press(key=Keys.ENTER):
    actions.send_keys(key).perform()
    actions.release()


def get_gen_tex():
    global gen_text
    perform_btn_click(GENERATE_BTN)
    do_scroll(TEXT_GENERATOR_WINDOW)
    close_add()
    perform_btn_click(COPY_TEXT_BTN)
    gen_text = pyperclip.paste()


def handle_text():
    global s_text
    spec_res = let_res = u_let_res = c_words = 0
    s_text = gen_text.split()

    for word in s_text:
        a, b, c, d = check_word(word)
        spec_res += a
        let_res += b
        u_let_res += c
        c_words += d

    print_result(spec_res, let_res, u_let_res, c_words)


def kill_proc():
    os.system(KILL_PROC_CMD)


def print_result(a, b, c, d):
    print('Output result:\n'
          f'\tTotal number of words: {d}\n'
          f'\tTotal number of words that start with upper letter : {c}\n'
          f'\tAmount of letters in the text: {b}\n'
          f'\tAmount of special symbols: {a}')

    print(f'Original text:\n {gen_text}')


def check_word(word: str):
    spec_res = let_res = u_let_res = w_count = 0
    len_word = len(word)

    if word[0].isupper():
        u_let_res += 1

    for i in range(len_word):
        if word[i] in SPEC_SYM:
            spec_res += 1
        else:
            let_res += 1

    if len_word != spec_res:
        w_count += 1

    return spec_res, let_res, u_let_res, w_count


if __name__ == '__main__':
    navigate_to_main_page()
    generate_input_values()
    get_gen_tex()
    handle_text()
    kill_proc()
