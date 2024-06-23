import requests
from flask import Flask, request, jsonify
import logging
import random
import argparse
import json
import time
import os

app = Flask(__name__)
configuracion = {}
board = 0
juego = 'juego1'  # Verificar cómo hacer esto automático

def cargar_configuracion():
    parser = argparse.ArgumentParser(description='Script para CLIENTE')
    parser.add_argument('ruta_archivo', type=str, help='Ruta del archivo de configuración')
    args = parser.parse_args()
    ruta_configuracion = args.ruta_archivo
    print("LA RUTA: ", ruta_configuracion)
    with open(ruta_configuracion, 'r') as archivo:
        configuracion = json.load(archivo)
    configuracion['ruta_archivo'] = ruta_configuracion  # Añadido para usarlo en setup_logging
    return configuracion

def setup_logging(config_file):
    # Configura el logging para cada archivo de configuración
    log_filename = os.path.join('RMI', config_file.replace('.json', '.log'))
    logging.basicConfig(filename=log_filename, 
                        filemode='w', 
                        level=logging.INFO,
                        format='%(asctime)s, %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')

# Definir la URL base del servidor Flask
configuracion = cargar_configuracion()
SERVER_URL = configuracion["server"]
CLIENT_IP = configuracion["ip"]
CLIENT_PORT = configuracion["port"]
PLAYER_NAME = configuracion["nombre"]
TEAM_NAME = configuracion["team"]
setup_logging(configuracion['ruta_archivo'])
teams = {}

def register_team(team_name):
    url = f'{SERVER_URL}/register_team'
    data = {'team_name': team_name}
    response = requests.post(url, json=data)
    response2 = response.json()
    if response2['message'] == 'Limit of teams reached':
        print("ERROR, limit of teams reached, just join a team.")
    return response.json()

def join_team(team_name, player_name):
    url = f'{SERVER_URL}/join_team'
    data = {'team_name': team_name, 'player_name': player_name, 'ip': CLIENT_IP, 'port': CLIENT_PORT}
    response = requests.post(url, json=data)
    return response.json()

def start_game():   
    url = f'{SERVER_URL}/start_game'
    response = requests.post(url)
    return response.json()

def roll_dice():
    url = f'{SERVER_URL}/roll_dice'
    data = {'team name': TEAM_NAME}
    response = requests.post(url, json=data)
    response2 = response.json()
    if response2['total team'] >= board:
        print("YOUR TEAM WON!")
    return response.json()

def game_status():
    url = f'{SERVER_URL}/game_status'
    response = requests.get(url)
    return response.json()

def get_teams():
    url = f'{SERVER_URL}/get_teams'
    response = requests.get(url)
    return response.json()

def log_event(event_type, action, *args):
    #timestamp = int(time.time())
    log_message = f'{event_type}, {juego}, {action}, ' + ', '.join(map(str, args))
    logging.info(log_message)

def inicio():
    global configuracion, board
    global TEAM_NAME
    global PLAYER_NAME
    global juego
    log_event('ini', 'inicio-juego')
    teams = get_teams()
    log_event('ini', 'crea-jugador', TEAM_NAME, PLAYER_NAME)
    message_join = join_team(TEAM_NAME, PLAYER_NAME)
    log_event('fin', 'crea-jugador', TEAM_NAME, PLAYER_NAME)
    board = message_join['board']
    log_event('ini', 'inicio-partida')
    message_start = start_game()
    log_event('fin', 'inicio-partida')

@app.route('/game_ready', methods=['GET'])
def game_ready_message():
    print('game ready to start, waiting for your turn')
    return jsonify({'message': 'Ready'})

@app.route('/your_turn', methods=['GET'])
def play_turn():
    log_event('ini', 'lanza-dado', TEAM_NAME, PLAYER_NAME)
    response = roll_dice()
    time.sleep(1) #Hacemos un delay para que haya diferencia en los tiempos del log
    log_event('fin', 'lanza-dado', TEAM_NAME, PLAYER_NAME, response['value'])
    return jsonify({'message': 'correct throw', 'total team': response['total team']})

@app.route('/game_ended', methods=['POST'])
def game_ended():
    ganador = request.json['ganador']
    print("The winner is ", ganador)
    print("Thanks for playing!")
    log_event('fin', 'inicio-partida')
    log_event('fin', 'inicio-juego')
    return jsonify({'message': 'BYE'})

with app.app_context():
    inicio()


if __name__ == '__main__':
    app.run(host=CLIENT_IP, port=CLIENT_PORT, debug=True, use_reloader=False)
