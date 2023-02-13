# Objetivo
Simular a detecção de anomalias no fluxo de informações com auxílio do Mininet Wifi e Aprendizado de Máquina.

# Sobre
São empregadas estruturas probabilísticas, estruturas fazem uso da um indexação baseada em hashing, com intuito de reduzir o espaço em memória e a complexidade dos dados representados. 
O tipo de estrutura probabilística usado é o Counter-Min, consistindo de uma matriz cujas posições são incrementadas a cada retorno de um hash. O hash é aplicado aos elementos de um fluxo de dados obtidos em um intervalo de tempo.

#### Metodologia:
- Desenvolver a topologia de rede no Mininet Wifi;
- Similar tráfegos normalidade entre os dispositivos;
- Adicionar anomalias ao tráfego;
- Capturar os pacotes da rede;
- Gerar as estruturas probabilísticas;
- Extrair métricas probabilísticas;
- Aplicar Aprendizado de Máquina às métrica para identificar intervalos de tempo.

# Mininet Wifi
Simula uma troca de dados com diferentes fluxos coletando e armazenando informações dos pacotes de cada um dos switchs em um respectivo PCAP.


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
- interval: [500,625,714,833,1000]

#### flood flow: são gerados com:
- size: 500-1400
- port: 1025-65536
