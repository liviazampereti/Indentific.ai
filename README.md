# Identifica_ai
### Inteligência Artificial Embarcada

[![N|Solid](https://docs.toradex.com/108455-toradex-logo-1200-630.png)](https://www.toradex.com/pt-br)

Identific_ai é um projeto que visa aplicar inteligência artificial de maneira embarcada.

Para este projeto foi necessário:
- Apalis IMX8 (Computer on Module)
- Ixora Carrier Board
- Torizon (Computer on Module OS)
- Linux (Development PC OS)

Com essas informações, foi possível obter o [Quickstart da Toradex](https://developer-archives.toradex.com/getting-started?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux)

Além disso, foi usado:
- Webcam USB Logitech
- Cabo Serial-DB9 e depois Serial-USB - ou - Cabo USB com 3 jumpers (Rx, Tx e USB)
- Cabo Ethernet

### Conexão Serial

##### Cabo Serial-DB9 e depois Serial-USB
O cabo serial-DB9 possui uma linha vermelha que indica o conector 1 do cabo, e a placa possui uma bolinha indicando o 1 na porta X22. Quanto ao cabo Serial-USB, o USB vai conectado ao computador contendo o Linux.

##### Cabo USB com 3 jumpers (Rx, Tx e USB)
Para a ligação com os jumpers, é necessário conecta-los nos pinos da placa de maneira correta na porta X22:
- RxD - pino 3
- TxD - pino 5
- GND - pino 9
- quanto ao USB é só conectá-lo ao computador contendo o Linux

Obs: quando testamos esse modo de conexão, dependendo da maneira como conectassemos os cabos, a placa não ligava. Conversando com o suporte, foi levantado a dúvida sobre o problema estar no cabo. Outras vezes que a placa conseguiu ligar, foi observado muito ruido, acreditamos que a conexão estava errada.

##### Checagem da Porta Serial
Para checar qual porta se encontra no computador, no terminal do Linux:
```
ls /dev/ttyUSB*
```
Possivelmente a porta conectada será: ```/dev/ttyUSB* ```
Após isso instalar o picocom através do seguinte comando e após instalado, rodar o segundo comando:
```
sudo apt install picocom
sudo picocom -b 115200 /dev/ttyUSB0
```
Com isso, será possível observar o que acontece no serial do terminal.

### Descobrir IP

[Find the board IP - Toradex](https://developer-archives.toradex.com/knowledge-base/scan-your-local-network-to-find-the-board-ip-and-mac-address)
 
No terminal do Linux no computador desenvolvedor:
```
ip a
```
Será printada várias redes, procurar por ```enp ``` ou ```eth ```
```
sudo arp-scan --localnet --interface=<rede encontrada>
```
 Se por acaso a rede não aparecer:
```
sudo apt-get install arp-scan
``` 
Dessa maneira, o IP vai estar no terminal após a execução do comando.
 
### Conexão via Network

Exercutar o seguinte comando, substituindo o IP, pelo endereço encontrado acima:
``` 
 ssh torizon@<IP>
``` 
Confirmar a conexão com ```yes``` e insira o login e senha:
> Login: toradex
> Senha: 123

### Conexão Linux - Camera USB
##### Testar Camera
No terminal Linux, para instalar o gucview:
``` 
sudo add-apt-repository ppa:pj-assis/testing
sudo apt-get update
sudo apt-get install guvcview
``` 
Com isso, é so procurar por Visualizador de Vídeo.

##### Encontrar Camera
No terminal Linux, sem conectar a camera:
```
cd /dev
ls video
```
Veja quais videos aparecem, no nosso, foram ```video0 ``` e ```video1 ```, esse são os endereços da webcam embutida no notebook.
Agora repita os comandos com a camera ligada e veja quais novos videos aparecem, esse novos são referentes a Webcam USB, um dos era o ```video3```.

##### Capturar imagem da camera usando OpenCV
Segue abaixo código em python para capturar a imagem da camera em Linux
```python
import cv2

cap = cv2.VideoCapture("/dev/video3") # check this
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
```

### Aplicação Embarcado
Uma das maneiras para transferir o código e uso da camera embarcado, é a criação de dois containers:
- Primeiro: responsável pela conexão com a camera 
- Segundo: responsável por realizar a interface

Dois links importantes são:
- [Tutorial criação de container - Toradex](https://developer-archives.toradex.com/getting-started?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux)
- [Thread sobre acesso de camera USB no Torizon - Toradex](https://community.toradex.com/t/access-usb-camera-on-torizon-as-a-non-root-user/17054)
- [Uso do Open-CV no Torizon - Toradex](https://developer.toradex.com/torizon/how-to/machine-learning/torizon-sample-using-opencv-for-computer-vision/)

### Informações extras
- Se placa começar a inicializar sozinha checar tomada (220v e se a mesma está funcionando bem)
- O Torizon trabalha com vários containers, inclusive o terminal é um container
