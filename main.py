# Archivo prinicipal del temporizador

from pomodoro import temporizador_pomodoro

def main():
    try:
        app_pomodoro = temporizador_pomodoro() # se crea una instancia del pomodoro
        app_pomodoro.run()
    except Exception as e:
        print("LA APLICACION NO SE EJECUTO")

if __name__ == "__main__":
    main()