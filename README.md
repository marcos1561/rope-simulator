# rope-simulator
Simulação física para cordas ou cabos. 

Sete as propriedades da corda, as propriedades dos elementos que modelam a corda, a condição inicial e rode o arquivo `main.py` para ver um gráfico contendo a corda sendo simulada conforme o tempo passa.

## Modelagem matemática
A corda é modela por massas pontuais e molas sem massa, ligadas em série de forma intercalada. Após ser setado a condição inicial da corda, é utilizado um método de integração numérica para evoluir a posição da corda com o tempo, de acordo com as lei de Newton.

Para fazer com que eventualmente a corda entre em equilíbrio, em cada nodo da corda, é aplicada uma força que se opõem a sua velocidade relativa aos seus nodos vizinhos.