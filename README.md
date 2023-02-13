# Como começar

Requisitos:
  - Mininet Wifi
  - Hping3

Para a geração dos Fluxos de dados execute o main.py com os seguintes parâmetros:
  -> -f : gerar os fluxos
  -> -p : plotar posição dos access point
  -> -m : inicia mobilidade (ainda não implementado)

## TODO:
### Parte 1:
- [x] Implementar a topologia da rede no mininet-wifi;
- [x] Implementar a mobilidade dos dispositivos STA 1~4;
- [ ] Implementar a troca de pacotes entre os dispositivos STA, de maneira uniforme ou não, que represente a normalidade;
  - [ ] Variar o tamanho dos pacotes mices e elephants (matriz de count está igual matriz de bytes);
  - [ ] Melhorar a alaeatoriedade de escolha dos nós (matriz normal está desbalanceada); 
- [ ] Capturar os pacotes que trafegam nos switches SW 1~5 utilizando wireshark ou tcpdump;
- [ ] Gerar dataset de pacotes de normalidade com intervalos de tempo pré-definido;
- [ ] Gerar dataset de pacotes de anormalidade;

### Parte 2:
- [ ] Definir função hash de indexação (source, target);
- [ ] Gerar estruturas count-min com contagem de bytes;
- [ ] Gerar estruturas count-min com contagem de pacotes;

### Parte 3:
A definir: aplicação de técnicas de ML para identificação das anomalias.
