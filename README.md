# Identifica_ai

<p align="center">
    <img alt="Badge em Desenvolvimento" src="https://img.shields.io/badge/status-em%20desenvolvimento-brightgreen">
    <img alt="Badge last commit" src="https://img.shields.io/github/last-commit/liviazampereti/Indentific.ai">
</p>

<h2 align="center"> Inteligência Artificial Embarcada </h2>

<p align="center">
    <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/gui/main.png" width=30% height=40%><a href="https://www.toradex.com/pt-br"><img src="https://docs.toradex.com/108455-toradex-logo-1200-630.png" width=70% height=80%></a>
</p>

### Índice
* [Sobre o projeto](#sobre-o-projeto)
    * [Materiais Necessários](#materiais-necessários)
* [Primeiros passos](#primeiros-passos)
    * [Conexão da placa com o computador](#conexão-da-placa-com-o-computador)
        * [Conexão serial](#conexão-serial)
        * [Conexão via network](#conexão-via-network)
    * [Utilização do Visual Studio Code](#utilização-do-visual-studio-code)

---

## 🧠 Sobre o projeto

Identific_ai é um projeto que visa aplicar inteligência artificial para realizar a classificação de imagens com auxílio de uma câmera USB, tudo isso utilizando a estrutura embarcada de uma placa de desenvolvimento Toradex.

### Materiais Necessários

Foram utilizados nesse projeto:
- Apalis IMX8 (Computer on Module);
- Ixora Carrier Board;
- Torizon (Computer on Module OS);
- Linux (Development PC OS).

Com essas informações, foi possível obter o [Quickstart da Toradex](https://developer-archives.toradex.com/getting-started?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux). Além disso, para possibilitar o uso do microcontrolador e a sua conexão com o computador de desenvolvimento, foram usados:
- Webcam USB Logitech C270;
- Teclado USB;
- Mouse USB;
- Monitor;
- Cabo Serial-DB9 e Serial-USB *ou* Conversor USB com 3 jumpers (Rx, Tx e GND);
- 2 cabos Ethernet (Placa e computador de desenvolvimento);
- Fonte 12V e 5A.

---

## 🛠 Primeiros passos

Inicialmente, é necessário preparar a estrutura, fazendo a montagem do hardware e conectando o computador de desenvolvimento à placa. Essa fase varia para cada modelo de placa utilizada, porém a Toradex fornece suporte para todos os modelos que a empresa trabalha em seu site para desenvolvedores.

Conforme citado, foi utilizada a placa **Apalis IMX8 - Ixora** e recomenda-se um sistema operacional Linux no computador de desenvolvimento. Para os primeiros passos, conectando a fonte e demais periféricos à placa recomenda-se a leitura da [primeira parte do módulo 1 do Quickstart](https://developer-archives.toradex.com/getting-started/module-1-from-the-box-to-the-shell/unboxing-and-setup-cables-ixora-imx8-torizon?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux).

### Conexão da placa com o computador

Um ponto importante é elaborar a comunicação da placa com o computador de desenvolvimento, para isso há dois caminhos possíveis: utilizar a conexão serial ou fazer a conexão via rede.

Essas duas formas podem apresentar certos problemas e dificuldades, os quais serão explicados adiante.

#### Conexão serial

* **Cabo Serial-DB9 e Serial-USB:**

    O cabo serial-DB9 possui uma linha vermelha, a qual indica o conector 1 do cabo, já a placa possui uma bolinha, indicando o 1 na porta X22. Quanto ao cabo Serial-USB, o USB vai conectado ao computador contendo o Linux.

    Abaixo estão algumas fotos do cabo serial-DB9 e de como a conexão deve ser feita com a placa, conforme descrito acima.

    <p align="center">
        <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/db9.jpeg" width=45% height=40%> <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/db9_conectado.jpeg" width=20.2% height=20%>
    </p>

* **Cabo USB com 3 jumpers (Rx, Tx e USB):**

    Para a ligação com o conversor USB, utilzando jumpers, é necessário conectá-los aos pinos da placa de maneira correta, na porta X22:
    - RxD - pino 3;
    - TxD - pino 5;
    - GND - pino 9;
    - Quanto ao conversor USB é só conectá-lo ao computador contendo o Linux.

    Para ilustrar, temos abaixo, à esquerda, imagens do conversor USB com os jumpers, indicando as cores de cada pino *(RxD - Cinza, TxD - Roxo, GND - Preto)* e também a conexão feita na placa.

    <p align="center">
    <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/jumpers.jpeg" width=50% height=50%>    <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/jumpers_conectados.jpeg" width=40% height=40%>
    </p>

    **Obs:** quando testamos esse modo de conexão, dependendo da maneira como conectássemos os cabos, a placa não ligava. Conversando com o suporte, foi levantada a dúvida sobre o problema estar no cabo, sugerindo trocá-lo. Outras vezes que a placa conseguiu ligar, foi observado muito ruído, acreditamos que a conexão estava errada.

* **Checagem da porta serial:**

    Para checar qual porta se encontra no computador, no terminal do Linux:
    ```
    ls /dev/ttyUSB*
    ```
    Possivelmente a porta conectada será: ```/dev/ttyUSB0```. Após isso, instalar o picocom e rodar o segundo comando:
    ```
    sudo apt install picocom
    sudo picocom -b 115200 /dev/ttyUSB0
    ```
    Caso o resultado do comando ```ls``` não tenha 0 como dígito final, altere no segundo comando acima. Com isso, será possível observar no terminal o que acontece no serial, permitindo a identificação da placa conectada.

#### Conexão via network

* **Descobrindo o IP:**

    No terminal Linux, do computador desenvolvedor:
    ```
    ip a
    ```
    Serão printadas várias redes, procurar por ```enp ``` ou ```eth ```, na imagem abaixo está localizado no número 2.

    <p align="center">
        <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/ip_a.png">
    </p>

    Em seguida, digite o seguinte comando, substituindo a rede encontrada. No caso da imagem: "enp2s0f1".

    ```
    sudo arp-scan --localnet --interface=<rede encontrada>
    ```
    **Obs:** Caso o computador não encontre o comando digitado, digite o código abaixo e repita os passos descritos:
    ```
    sudo apt-get install arp-scan
    ``` 
    Dessa maneira, o IP da placa vai estar no terminal após a execução do comando, conforme a imagem abaixo.

    <p align="center">
        <img src="https://raw.githubusercontent.com/liviazampereti/Indentific.ai/master/images/arpscan.png">
    </p>

    Um tutorial detalhado, fornecido pela Toradex, está localizado em [Find the board IP - Toradex](https://developer-archives.toradex.com/knowledge-base/scan-your-local-network-to-find-the-board-ip-and-mac-address).
 
* **Conectando com a placa**

    Executar o seguinte comando, substituindo o IP pelo endereço encontrado acima:
    ``` 
    ssh torizon@<IP>
    ``` 

    **Obs:** Após algum tempo ou caso hajam mudanças na rede conectada, esse endereço possivelmente será diferente, sendo necessário repetir o passo anterior de descobrir o IP a cada vez que o usuário trabalhe na placa.

    Confirmar a conexão com ```yes``` e insira o login e senha:
    > Login: toradex

    > Senha: 123

### Utilização do Visual Studio Code

O VS Code possui suporte para conexão com as placas de desenvolvimento da Toradex, para isso, é necessário instalar a extensão da empresa no programa e conectar com a placa via rede ou serial.

A Toradex fornece um guia bem completo para realizar essa operação na sua página de desenvolvedores, no seguinte link: [Visual Studio Code Extension for Torizon](https://developer.toradex.com/torizon/working-with-torizon/application-development/visual-studio-code-extension-for-torizon/)

---

## 📷 Conexão câmera

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
Veja quais videos aparecem, no nosso caso, foram ```video0``` e ```video1```, esse são os endereços da webcam embutida ao notebook. Agora repita os comandos com a camera ligada e veja quais novos videos aparecem, esse novos são referentes a webcam USB, um dos era o ```video3```.

##### Capturar imagem da camera usando OpenCV
Segue abaixo código em python para capturar a imagem da camera em Linux
```
python
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

## Primeiros passos com a interface da placa de desenvolvimento

Até então, tudo foi feito conectando-se remotamente a placa com o computador, porém, o microcontrolador já vem com o sistema operacional da Toradex, o **Torizon** e a aplicação utilizada para gerenciar seus containers é o **Portainer.io**. Ele já vem com alguns containers básicos e permite a instalação de outros, necessários para a aplicação do usuário. Informações de como utilizar o Portainer, iniciar, gerenciar e criar novos containers estão descritas no Módulo 2 do [Quickstart da Toradex](https://developer-archives.toradex.com/getting-started?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux), porém recomendamos aos usuários seguirem o tutorial desde o início para sanar quaisquer dúvidas.

Outra informação relevante é que, ao iniciar a placa, será necessário fornecer um login e senha para o Portainer, as credenciais utilizadas atualmente são:
> Login: identific_ai

> Senha: identificai

## 💻 Aplicação Embarcado
Uma das maneiras para transferir o código e uso da camera embarcado, é a criação de dois containers:
- Primeiro: responsável pela conexão com a camera 
- Segundo: responsável por realizar a interface

Alguns links importantes são:
- [Tutorial criação de container - Toradex](https://developer-archives.toradex.com/getting-started?som=apalis-imx8&board=ixora-carrier-board&os=torizon&desktop=linux)
- [Thread sobre acesso de camera USB no Torizon - Toradex](https://community.toradex.com/t/access-usb-camera-on-torizon-as-a-non-root-user/17054)
- [Uso do Open-CV no Torizon - Toradex](https://developer.toradex.com/torizon/how-to/machine-learning/torizon-sample-using-opencv-for-computer-vision/)


## Desenvolvimento da Inteligência Artificial

---

## Próximos passos

---

## ❗ Informações extras
- Se placa começar a reiniciar sozinha, checar a fonte, sua voltagem e o funcionamento da tomada;
- O Torizon trabalha com vários containers, inclusive o terminal é um container;
- A Toradex tem um suporte bem eficiente e com respostas bem rápidas para casos de dúvidas ou problemas técnicos, entre as possíveis formas de suporte estão:
  - [Página da comunidade](https://community.toradex.com/)
  - Email: support@toradex.com
  - Telefone: (19) 3327-3732
- A página de desenvolvedores da Toradex tem bastante informações úteis e que ajudam muito, mas elas ficam um pouco espalhadas, é preciso ter paciência e procurar bem.

---

## 👩‍💻 Autores

| [<img src="https://avatars.githubusercontent.com/u/93014017?v=4" width=115><br><sub>Ana Letícia Garcez</sub>](https://github.com/analeticiagarcez) |  [<img src="https://avatars.githubusercontent.com/u/69127118?v=4" width=115><br><sub>Lívia Zamperetti</sub>](https://github.com/liviazampereti) |  [<img src="https://avatars.githubusercontent.com/u/79988012?v=4" width=115><br><sub>Rafael Saud</sub>](https://github.com/Rafael-Saud) |
| :---: | :---: | :---: |