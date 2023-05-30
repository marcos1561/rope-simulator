# rope-simulator
Simulação física para cordas ou cabos com as extremidades fixas, sob o efeito da gravidade.

No arquivo `main.py`, sete as propriedades da corda, as propriedades dos elementos que modelam a corda e sua condição inicial. Após rodar o arquivo, será gerado um gráfico contendo a corda sendo simulada conforme o tempo passa.

## Como usar

Primeiro é necessário instanciar um objeto da classe `Simulation` (que está em `simulation.py`), então, para iniciar a simulação apenas é necessário chamar o método `run` do objeto em questão.

Em sequência, segue com mais detalhamento o que deve ser feito para conseguir criar uma instância de `Simulation`.

### Setando as configurações

Primeiro é necessário setar as configurações da simulação, que estão contidas em classes.
As seguintes classes de configuração devem ser instanciadas e passadas para o construtor de `Simulation`:

- `RopeConfig`: Propriedades da corda a ser simulada.
- `RopeConfig`: Propriedades dos elementos que compõem o modelo da corda.
- `CreateConfig`: Configuração para a construção da corda.

> O arquivo `main.py` já possui essas classes instanciadas, então é possível apenas editá-lo para suas preferências.

### Formato inicial da corda

Deve ser fornecido uma curva paramétrica, cujo parâmetro é o comprimento da curva, para definir a posição inicial dos nodos da corda.

O módulo `curves.py` contém uma coletânea de curvas paramétricas prontas para serem utilizadas, mas é possível criar a sua própria curva, contanto que ela seja uma superclasse de `Curve`.

> O arquivo `main.py` possui uma instância de `Line`, ou seja, o formato inicial da corda é uma linha reta.

### Visualização da simulação
É possível configurar algumas coisas sobre a visualização da simulação como:

* Modo de visualização da corda:

  Existem dois modos:
  
    * **points**: Gráfico de linha com pontos nos nodos
    * **color_tension**: Gráfico de linha, em que a cor em cada ponto da linha representa a intensidade da tensão nesse ponto.
  
 * Mostra ou não o gráfico da intensidade da tensão da corda. 
 
 > O arquivo `main.py` está configurado com o modo **color_tension** e para mostrar o gráfico da tensão.  

### Resultado

Com a instância de `Simulation` criada, após chamar o método `run`, é criado um gráfico que possui a simulação sendo rodada. Se for rodado o arquivo `main.py` como ele está, o resultado é o seguinte:

![](https://github.com/marcos1561/rope-simulator/blob/main/example.gif)

## Modelagem matemática
A corda é modela por massas pontuais e molas sem massa, ligadas em série de forma intercalada. Após ser setado a condição inicial da corda, é utilizado um método de integração numérica para evoluir a posição da corda com o tempo, de acordo com as lei de Newton.

Para fazer com que eventualmente a corda entre em equilíbrio, em cada nodo da corda, é aplicada uma força que se opõem a sua velocidade relativa aos seus nodos vizinhos.
