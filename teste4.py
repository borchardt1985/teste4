import asyncio
from telegram import Bot
import requests
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
from io import StringIO

# Define a função scrape_tables
def scrape_tables(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table')
    extracted_tables = []

    for table in tables:
        df = pd.read_html(StringIO(str(table)), header=0)[0]
        extracted_tables.append(df)

    return extracted_tables

# Define a função get_value_from_table
def get_value_from_table(tables, row_index, col_index):
    table = tables[8]
    value = table.iloc[row_index, col_index]
    value = value.replace('%', '').replace(',', '.').strip()
    var_dx = float(value) if len(value) > 0 else 0.0
    return var_dx

def get_value_from_table_dolfut(tables, row_index, col_index):
    table = tables[8]
    value = table.iloc[row_index, col_index]
    value = value.replace('.', '').replace(',', '.')  # Remover vírgula e substituir ponto
    var_dolfut = float(value) if not pd.isnull(value) else 0.0
    return var_dolfut


# Defina a URL
url = 'https://br.investing.com/currencies/us-dollar-index'

# Chame a função scrape_tables e armazene a lista de tabelas na variável tables
tables = scrape_tables(url)

# Chame a função get_value_from_table, passe a lista de tabelas e os índices de linha e coluna,
# multiplique o resultado por 0.01 para mover o ponto decimal duas casas para a esquerda
var_dx = get_value_from_table(tables, 0, 4) * 0.01

# Defina a URL
url = 'https://br.investing.com/currencies/usd-brl-bmf-futures'

# Chame a função scrape_tables e armazene a lista de tabelas na variável tables
tables = scrape_tables(url)

# Chame a função get_value_from_table, passe a lista de tabelas e os índices de linha e coluna,
# multiplique o resultado por 0.01 para mover o ponto decimal duas casas para a esquerda
var_dolfut = get_value_from_table_dolfut(tables, 0, 2)

dol_justo = var_dolfut + (var_dx * var_dolfut)

# Imprima o valor final
'''print(var_dx)
print(type(var_dx))   
print(var_dolfut)
print(type(var_dolfut))   
print(dol_justo)
print(type(dol_justo))  '''

async def send_message(bot: Bot, chat_ids: list, message: str):
    """
    Sends a message to a list of chat IDs using a Telegram bot.

    Args:
        bot (Bot): The Telegram bot object.
        chat_ids (list): A list of chat IDs to send the message to.
        message (str): The message to send.

    Returns:
        None
    """
    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)

# Replace YOUR_API_TOKEN with the API token of your bot
bot = Bot(token='6730975506:AAFBR5zSTDzotp_Nk1L_5xDq6hxj-bDQNeE')

# Replace CHAT_IDS with a list of chat IDs to send the message to
#chat_ids = [681923185 (nelson), 801613218 (fabio), 1128000584 (flavio), 450950147 (paulo), 1437632669 (michael), 1302712719 (Rafael RT), 7065328528 (Luiz)]
#chat_ids = [681923185, 801613218, 1128000584, 450950147, 1437632669, 1302712719, 7065328528]
#chat_ids = [681923185]
from ids import chat_ids

# Replace MESSAGE with the message to send
message = "O valor do Dólar Justo agora é:  R$ {:.2f}".format(dol_justo)
#message = "Isto é apenas um teste, desconsidere. Valor: R$ {:.2f}".format(dol_justo)

# Call the send_message coroutine using the asyncio.run function
asyncio.run(send_message(bot, chat_ids, message))



