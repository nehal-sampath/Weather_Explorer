import socket
import json

def get_weather(city):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', 2344)
        client_socket.connect(server_address)
        client_socket.sendall(city.encode('utf-8'))
        data = client_socket.recv(1024)

        if not data:
            print("Server closed the connection unexpectedly.")
            return None

        weather_data = json.loads(data.decode('utf-8'))
        client_socket.close()

        return weather_data

    except ConnectionResetError:
        print("ConnectionResetError: Server closed the connection unexpectedly.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    city_name = input("Enter the city name: ")
    weather_info = get_weather(city_name)

    if weather_info is None:
        print("Failed to retrieve weather information.")
    elif 'error' in weather_info:
        print(f"Error: {weather_info['error']}")
    else:
        print("Weather Information:")
        print(f"Description: {weather_info['description']}")
        print(f"Temperature: {weather_info['temperature']} K")
        print(f"Humidity: {weather_info['humidity']}%")
        print(f"Weather Icon: http://openweathermap.org/img/w/{weather_info['icon']}.png")
