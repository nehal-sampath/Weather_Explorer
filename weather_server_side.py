import socket
import json
import threading
import requests

def get_weather_data(city):
    try:
        api_key = "4ca15b82fd9e8ea00b232bd29cecfd2d"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['cod'] == '404':
            return {'error': 'City not found'}

        weather = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'icon': data['weather'][0]['icon']
        }

        return weather

    except Exception as e:
        print(f"Error: {e}")
        return {'error': 'An error occurred while fetching weather data'}

def handle_client(client_socket):
    try:
        city = client_socket.recv(1024).decode('utf-8')
        print(f"Received request for weather in {city}")

        weather_data = get_weather_data(city)

        client_socket.sendall(json.dumps(weather_data).encode('utf-8'))

    except ConnectionResetError:
        print("ConnectionResetError: Client closed the connection unexpectedly.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('127.0.0.1', 2344)
    server_socket.bind(server_address)

    server_socket.listen(5)
    print(f"Server is listening on {server_address}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
