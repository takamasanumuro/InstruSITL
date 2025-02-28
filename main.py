import tkinter as tk  # Biblioteca usada para criar a interface gráfica (GUI)
from tkinter import ttk  # Módulo que contém widgets com temas (melhor aparência)
import threading  # Usado para rodar tarefas em paralelo (threads)
from pymavlink import mavutil  # Biblioteca para comunicação com MAVLink
from pymavlink.dialects.v20 import ardupilotmega  # Dialeto MAVLink específico do ArduPilot

'''
Exemplo do mecanismo de roteamento Mavlink e recepção de mensagens
Sempre use as anotações de tipo para poder ter acesso às funções e variáveis de cada módulo e objeto
Algumas funções construtoras como o mavlink_connection returnam tipos de objetos diferentes de acordo com o tipo de conexão, 
então cheque a implementação e use a anotação de tipo apropriada.

Cheque o link abaixo para mais detalhes sobre a biblioteca pymavlink
https://mavlink.io/en/mavgen_python/
'''

# Criação da janela principal
root = tk.Tk()
root.title("Mavlink voltage monitor")  # Define o título da janela

# Inicializa a variável de tensao
voltage = 10.0  

# Função chamada ao alterar o slider de tensao
def update_voltage(value):
    """Atualiza o rótulo da interface gráfica com a nova tensao."""
    voltage_label.config(text=f"Voltage: {float(value):.2f}V")  # Exibe a tensao com 2 casas decimais
    global voltage
    voltage = float(value)  # Atualiza a variável global

# Cria um controle deslizante (slider) para ajustar a tensao
voltage_slider = ttk.Scale(root, from_=10, to=14.4, orient="horizontal", length=300, command=update_voltage)
voltage_slider.pack(pady=20)  # Adiciona um espaçamento vertical

# Rótulo para exibir a tensao atual
voltage_label = tk.Label(root, text="Voltage: 10.00V")
voltage_label.pack(pady=10)

# Rótulo para exibir a localização
location_label = tk.Label(root, text="Location: ")
location_label.pack(pady=10)

# Função para rodar em uma thread separada e enviar mensagens MAVLink
def mavlink_thread():
    """Estabelece conexão MAVLink, envia status da bateria e exibe a localização."""
    
    # Documentação do SITL (Software In The Loop) do ArduPilot
    # https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html

    # Conecta ao veículo simulado no SITL usando as portas TCP. 5760 = Serial1, 5761 = Serial2, 5762 = Serial3)
    connection: mavutil.mavfile = mavutil.mavlink_connection(device='tcp:localhost:5762', source_system=1, source_component=ardupilotmega.MAV_COMP_ID_BATTERY)
    # A função mavlink_connection configura um canal de comunicação por meio de porta serial, UDP ou TCP
    # O objeto retornado tem uma função recv_match() para capturar mensagens recebidos com base em filtros
    # Também possui uma propriedade mav que pode ser usada para encodificar e enviar mensagens

    # Aguarda um heartbeat (sinal de vida) do veículo
    connection.wait_heartbeat()
    print(f"Heartbeat recebido do sistema {connection.target_system}")

    while True:
        mav: ardupilotmega.MAVLink = connection.mav  # Objeto MAVLink para enviar mensagens
        #ardupilotmega é o módulo compilado baseado no xml e contém enumerações e funções Mavlink

        # Envia o status da bateria para o veículo
        mav.battery_status_send(
            id=0,
            battery_function=ardupilotmega.MAV_BATTERY_FUNCTION_ALL, 
            type=ardupilotmega.MAV_BATTERY_TYPE_LIPO,
            temperature=-1,  # Sem temperatura
            voltages=[int(voltage * 1000), 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Converte volts para milivolts
            current_battery=-1, # Sem informação sobre corrente
            current_consumed=-1, # Sem informação sobre corrente consumida 
            energy_consumed=-1, # Sem informação sobre energia consumida
            battery_remaining=-1  # Sem informação sobre carga restante
        )

        # Obtém a localização do veículo
        location: mavutil.location = connection.location()
        location_label.config(text=f"Location: {location.lat}, {location.lng}")  # Atualiza a interface gráfica

        import time
        time.sleep(0.1)  # Pequena pausa para evitar uso excessivo de CPU

# Inicia a thread MAVLink como daemon (finaliza quando o programa fecha)
threading.Thread(target=mavlink_thread, daemon=True).start()

# Inicia o loop principal da interface gráfica (mantém a janela aberta)
root.mainloop()
