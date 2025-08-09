import serial
import matplotlib.pyplot as plt
import time
import csv
from datetime import datetime

# Configurações da porta serial
porta = 'COM11'  # Altere para sua porta
baud_rate = 9600

# Parâmetros do material
Q = 0.5994       # Fluxo de calor (W)
L = 0.1       # Espessura (m)
A = 28.274e-6  # Área (m²)

# Inicialização da comunicação serial
ser = serial.Serial(porta, baud_rate)
time.sleep(2)  # Tempo para estabilização

# Variáveis para armazenamento
tempos = []
temps_sensor1 = []
temps_sensor2 = []
condutividades = []
inicio = time.time()  # Definindo a variável inicio aqui

# Configuração dos gráficos
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.tight_layout(pad=3.0)

# Arquivo CSV
nome_arquivo = f"dados_termicos_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(["Tempo (s)", "Sensor 1 (°C)", "Sensor 2 (°C)", "k (W/m·K)"])
    
    try:
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode(errors='ignore').strip()
                print(linha)
                
                tempo_atual = time.time() - inicio
                
                # Processamento Sensor 1
                if linha.startswith("Sensor 1:"):
                    try:
                        temp1 = float(linha.split(":")[1].replace("ºC", "").strip())
                        temps_sensor1.append(temp1)
                        temps_sensor2.append(None)
                        tempos.append(tempo_atual)
                    except (ValueError, IndexError):
                        continue
                
                # Processamento Sensor 2
                elif linha.startswith("Sensor 2:"):
                    try:
                        temp2 = float(linha.split(":")[1].replace("ºC", "").strip())
                        
                        if temps_sensor2 and temps_sensor2[-1] is None:
                            temps_sensor2[-1] = temp2
                            
                            # Cálculo da condutividade quando temos ambos os sensores
                            if temps_sensor1 and temps_sensor2[-1] is not None:
                                delta_T = temps_sensor1[-1] - temps_sensor2[-1]
                                if delta_T > 0.5:  # Threshold para evitar ruído
                                    k = (Q * L) / (A * delta_T)
                                    condutividades.append(k)
                                    writer.writerow([
                                        round(tempo_atual, 2),
                                        temps_sensor1[-1],
                                        temps_sensor2[-1],
                                        round(k, 4)
                                    ])
                                else:
                                    condutividades.append(None)
                        else:
                            temps_sensor1.append(None)
                            temps_sensor2.append(temp2)
                            tempos.append(tempo_atual)
                            condutividades.append(None)
                            
                    except (ValueError, IndexError):
                        continue
                
                # Atualização dos gráficos
                if len(tempos) > 1:
                    # Gráfico de Temperaturas
                    ax1.clear()
                    ax1.plot(tempos, temps_sensor1, 'ro-', label="Sensor 1 (Quente)")
                    ax1.plot(tempos, temps_sensor2, 'bs-', label="Sensor 2 (Frio)")
                    ax1.set_ylabel("Temperatura (°C)")
                    ax1.legend()
                    
                    # Gráfico de Condutividade
                    ax2.clear()
                    if condutividades:
                        # Filtra apenas valores válidos
                        valid_k = [k for k in condutividades if k is not None]
                        valid_times = [t for t, k in zip(tempos, condutividades) if k is not None]
                        if valid_k:
                            ax2.plot(valid_times, valid_k, 'g^-', label="Condutividade Térmica")
                            ax2.set_xlabel("Tempo (s)")
                            ax2.set_ylabel("k (W/m·K)")
                            ax2.legend()
                    
                    plt.pause(0.1)
    
    except KeyboardInterrupt:
        print("\nColeta de dados encerrada pelo usuário")
    finally:
        ser.close()
        print(f"Dados salvos em: {nome_arquivo}")
        plt.ioff()
        plt.show()