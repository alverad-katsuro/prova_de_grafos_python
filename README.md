# Trabalho final - Grafos
## Descrição
  Este trabalho visa implementar algoritmos requisitados no documento _grafo_tfinal.pdf_ para realizar certas funções em um grafo simples, 
  e dispor os resultados visualmente, que podem ser valores booleanos, númericos ou grafos.
  
## Metodologia de desenvolvimento adotada
Para a implementação desse trabalho, foi selecionado a linguagem de programação Python,
utilizando o _framework_ do [Graphviz](https://graphviz.org/), 
que permite a criação e plotagem de grafos de forma gráfica, 
em conjunção com o _web framework_ [Django](https://www.djangoproject.com/), 
que permite a criação de uma interface em _web_,
o que faz com que seja possível a disposição dos grafos resultantes de forma visual em uma interface na qual seja possível a inserção do grafo e determinação de qual operação executar, além da visualização de determinados resultados.

### Dependências necessárias
 As dependências necessárias para a execução de todo o projeto são várias, sendo fundamental as seguintes:
  - Python 3.8 ou superior;
  - Django;
  - Pandas;
  - Graphviz;
   
  Contudo, existem outras dependências, todas reunidas em um arquivo denominado _requirements.txt_, e
  é possível instalar todas essas dependências citadas pelo seguinte comando:
  ```
  python3 -m pip install -r requirements.txt
  ```
  Note que pode ser necessário que ```python3``` seja substituído pela versão do Python utilizada na máquina em questão, 
  e recomenda-se a criação e utilização de uma máquina virtual para a instalação das dependências; e, posteriormente, execução desse repositório.
  
 ## Execução do servidor
  Tendo todas as dependências instaladas, para a execução do servidor na máquina em questão, é necessário executar o seguinte comanndo:
  ```
  python3 manage.py runserver
  ```
  O comando terá, por retorno, o endereço em que o servidor está sendo hospedado, além de permitir outras máquinas entrarem no endereço enquanto o servidor esteja sendo executado.

  
