import serial
import matplotlib.pyplot as plt
import time
import csv
from datetime import datetime

# Parâmetros fixos do material (alumínio)
k = 237.0       # Condutividade térmica (W/m·K)
L = 0.1         # Distância entre sensores (10 cm em metros)
A = 44.2225e-6  # Área da seção transversal (44,2225 mm² → 44,2225×10⁻⁶ m²)

# Configuração da porta serial
porta = 'COM11'
taxa_bauds = 9600

ser = serial.Serial(porta, taxa_bauds)
time.sleep(2)  # Aguarda inicialização da comunicação

# Armazenamento de dados
tempos = []
temp_sensor1 = []
temp_sensor2 = []
fluxos_calor = []  # Para armazenar os valores calculados de Q

# Configuração do gráfico
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
fig.tight_layout(pad=3.0)

# Arquivo CSV para salvar os dados
nome_arquivo = f"dados_fluxo_calor_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerow(["Tempo (s)", "Temp1 (°C)", "Temp2 (°C)", "Fluxo de Calor (W)"])
    
    tempo_inicio = time.time()
    
    try:
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode(errors='ignore').strip()
                print(f"Recebido: {linha}")
                
                tempo_atual = time.time() - tempo_inicio
                
                # Processa Sensor 1
                if "Sensor 1:" in linha:
                    try:
                        t1 = float(linha.split(":")[1].replace("ºC", "").strip())
                        temp_sensor1.append(t1)
                        temp_sensor2.append(None)
                        tempos.append(tempo_atual)
                        print(f"Temp1: {t1} °C")
                    except (ValueError, IndexError) as erro:
                        print(f"Erro no Sensor 1: {erro}")
                        continue
                
                # Processa Sensor 2
                elif "Sensor 2:" in linha:
                    try:
                        t2 = float(linha.split(":")[1].replace("ºC", "").strip())
                        print(f"Temp2: {t2} °C")
                        
                        if temp_sensor2 and temp_sensor2[-1] is None:
                            temp_sensor2[-1] = t2
                            
                            # Calcula o fluxo de calor Q quando as duas temperaturas estão disponíveis
                            if temp_sensor1 and temp_sensor2[-1] is not None:
                                delta_T = temp_sensor1[-1] - temp_sensor2[-1]
                                if delta_T > 0.1:  # Evita ruído com limiar mínimo
                                    Q = (k * A * delta_T) / L
                                    fluxos_calor.append(Q)
                                    escritor.writerow([
                                        round(tempo_atual, 2),
                                        temp_sensor1[-1],
                                        temp_sensor2[-1],
                                        round(Q, 4)
                                    ])
                                    print(f"Q calculado: {Q:.4f} W")
                                else:
                                    fluxos_calor.append(None)
                        else:
                            temp_sensor1.append(None)
                            temp_sensor2.append(t2)
                            tempos.append(tempo_atual)
                            fluxos_calor.append(None)
                            
                    except (ValueError, IndexError) as erro:
                        print(f"Erro no Sensor 2: {erro}")
                        continue
                
                # Atualiza gráficos
                if len(tempos) > 1:
                    try:
                        # Gráfico de temperatura
                        ax1.clear()
                        ax1.plot(tempos, temp_sensor1, 'r-', label="Lado Quente (Sensor 1)")
                        ax1.plot(tempos, temp_sensor2, 'b-', label="Lado Frio (Sensor 2)")
                        ax1.set_ylabel("Temperatura (°C)")
                        ax1.legend()
                        
                        # Gráfico de fluxo de calor
                        ax2.clear()
                        if fluxos_calor:
                            Q_validos = [q for q in fluxos_calor if q is not None]
                            tempos_validos = [t for t, q in zip(tempos, fluxos_calor) if q is not None]
                            if Q_validos:
                                ax2.plot(tempos_validos, Q_validos, 'g-', label="Fluxo de Calor (Q)")
                                ax2.set_xlabel("Tempo (s)")
                                ax2.set_ylabel("Fluxo de Calor (W)")
                                ax2.legend()
                        
                        plt.pause(0.1)
                    except Exception as erro:
                        print(f"Erro ao atualizar gráfico: {erro}")
    
    except KeyboardInterrupt:
        print("\nExperimento interrompido pelo usuário")
    except Exception as erro:
        print(f"\nErro durante a execução: {erro}")
    finally:
        ser.close()
        print(f"Dados salvos em: {nome_arquivo}")
        plt.ioff()
        plt.show()
