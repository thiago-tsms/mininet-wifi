# Sobre
Simula uma troca de dados com diferentes fluxos coletando informações dos pacotes em cada switch e armazenando em um PCAP.


#### Topologia:

|--- [SW1] --- [AP1] --- [STA1] <br>
|--- [SW2] --- [AP2] --- [STA2] <br>
|--- [SW3] --- [AP3] --- [STA3] <br>
|--- [SW4] --- [AP4] --- [STA4] <br>
| <br>
|-- [SW5] <br>


## Como começar

Requisitos:
  - Mininet Wifi
  - Hping3
  - tcpdump

Para a geração dos Fluxos de dados execute o main.py com os seguintes parâmetros:
  - -f : gerar os fluxos
  - -p : plotar posição dos access point
  - -m : inicia mobilidade (ainda não implementado)

## Funcionamento:

#### Parâmetros de entrada (-f)
- Tempo de execução
- Número de mice flow
- Número de elephant flows

#### mice flow: são gerados com:
- fluxos simultâneos: 2-8
- size: 20-500
- port: 1025-65536
- interval: {500,625,714,833,1000}

#### flood flow: são gerados com:
- size: 500-1400
- port: 1025-65536
