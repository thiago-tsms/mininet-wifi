# Como começar
Para rodar o sflow é necessário java installado
sudo apt install default-jre

o download do sflow pode ser feito com
wget https://inmon.com/products/sFlow-RT/sflow-rt.tar.gz
tar -xvzf sflow-rt.tar.gz
cd sflow-rt

para inciá-lo, rode
./start.sh

a partir disso, o a topologia mobilidade.py pode ser iniciada

# Trabalho Laboratório de Redes

Este trabalho tem como objetivo aplicar técnicas de aprendizado de máquinas para detecção de anomalias em redes de computadores a partir da medição de tráfego por meio de estruturas de dados probabilísticas (sketches), utilizando para isso simulações através do mininet-wifi.

## TODO:
### Parte 1:
- [x] Implementar a topologia da rede no mininet-wifi;
- [ ] Implementar a mobilidade dos dispositivos STA 1~4;
- [ ] Implementar a troca de pacotes entre os dispositivos STA, de maneira uniforme ou não, que represente a normalidade;
- [ ] Capturar os pacotes que trafegam nos switches SW 1~5 utilizando wireshark ou tcpdump;
- [ ] Gerar dataset de pacotes de normalidade com intervalos de tempo pré-definido;
- [ ] Gerar dataset de pacotes de anormalidade;

### Parte 2:
- [ ] Definir função hash de indexação (source, target);
- [ ] Gerar estruturas count-min com contagem de bytes;
- [ ] Gerar estruturas count-min com contagem de pacotes;

### Parte 3:
A definir: aplicação de técnicas de ML para identificação das anomalias.
