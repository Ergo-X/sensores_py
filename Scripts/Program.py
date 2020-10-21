import os
import asyncio
import busio
import json
import time
import board
import adafruit_ahtx0
import adafruit_tsl2561
from Decibel import Decibel
from azure.iot.device.aio import IoTHubDeviceClient

# Declara a String de conexão do Device
connection_string = "HostName=Senai132IotRaspberry.azure-devices.net;DeviceId=rasp1;SharedAccessKey=+eFtg2cGnvbD5xM6HI7BKIoSBuZCJsrVBMiS4tP1LI0="
# Declara quais são as portas para os sensores i2c
i2c = busio.I2C(board.SCL, board.SDA)
# Declara o driver do sensor de temperatura e umidadade AHT10 como aht
aht = adafruit_ahtx0.AHTx0(i2c)
# Declara o driver do sensor de luminosidade TSL2561 como tsl
tsl = adafruit_tsl2561.TSL2561(i2c)
# Declara a variável lux como 0
lux = 0

async def main():
    # Pega a String de Conexão das variáveis de ambiente
    conn_str = os.getenv(str(connection_string))
    # Cria uma instância do Device com a String de Conexão
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    # Conecta ao Device
    await device_client.connect()
    # Enquanto for True ele vai mandar a mensagem para o Device no IotHub
    while True:
        # Confere se o valor do sensor de luminosidade não é None
        # Se for None ele declara o valor de lux como 0
        if tsl.lux == None:
            lux = 0
            print(lux)
        # Se não for None ele pega o valor de leitura do sensor e declara dentro da variável lux
        else:
            lux = tsl.lux
        
        # Instancia a classe de Decibéis
        db = Decibel()    
            
        # Monta em json a mensagem que vai ser enviada ao IotHub com as leituras dos sensores
        message = { "temperatura": str(round(float(aht.temperature),2)),
                    "umidade": str(round(float(aht.relative_humidity),2)),
                    "luminosidade": str(round(float(lux)),2),
                    "decibeis": str(round(float(db.medir_decibeis()),2))}
        #message = { "temperatura": str(round(float(aht.temperature),2)),
        #            "umidade": str(round(float(aht.relative_humidity),2)),
        #            "luminosidade": str(round(float(304),2)),
        #            "decibeis": str(round(float(db.medir_decibeis()),2))}
        
        # Envia para o Device a mensagem que foi montada
        await device_client.send_message(str(message))
        # Mostra a mensagem
        print(message)
        # Espera dois segundos
        time.sleep(2)

    # Desconecta do Device
    await device_client.disconnect()

# Diz para o código para rodar a função main() assim desde que roda a primeira vez
if __name__ == "__main__":
    asyncio.run(main())

