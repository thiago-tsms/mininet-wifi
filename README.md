# Sobre
Simula uma troca de dados com diferentes fluxos

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
Parâmetros de entrada (-f)
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
