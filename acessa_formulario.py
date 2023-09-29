from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd


data = pd.read_csv('atualizar_ipca.csv',  sep=';')

data['dPostagem'] = data['dPostagem'].astype(str)
data['dPagto'] = data['dPagto'].astype(str)
print(data.info())

result = ''

driver = webdriver.Chrome()
driver.get("https://www3.bcb.gov.br/CALCIDADAO/publico/exibirFormCorrecaoValores.do?method=exibirFormCorrecaoValores&aba=1")

for index, row in data.iterrows():
        dPostagem = row['dPostagem'][-6:]
        dPagto = row['dPagto'][-6:]
        valor = row['valor']

        dPagto = '092023'

        select_element = driver.find_element(By.NAME, "selIndice")
        select = Select(select_element)
        select.select_by_value('10764IPC-E')

        driver.find_element(By.NAME, "dataInicial").send_keys(dPostagem)
        driver.find_element(By.NAME, "dataFinal").send_keys(dPagto)
        driver.find_element(By.NAME, "valorCorrecao").send_keys(valor)

        driver.find_element(By.CLASS_NAME, "botao").click()

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        valor = driver.find_element(By.XPATH,"/html/body/div[6]").text

        result = result + valor

        driver.find_element(By.CLASS_NAME,"botao").click()

with open('resultado.txt', 'a') as f:
    f.write(result)



driver.quit()






