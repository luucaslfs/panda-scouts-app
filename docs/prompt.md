# Prompts

### Prompt Inicial

```
Estou criando uma aplicação para capturar dados de partidas de futebol de ligas especificas, filtrar partidas de acordo com algumas estatísticas e depois exibir dados dos confrontos e dos times envolvidos.

A principio, pensei em criar uma API com FastAPI para consumir outras APIs e processar os dados, retornando o que eu preciso. No futuro, quero exibir os dados das partidas em um bot no telegram ou em uma pagina iterativa utilizando streamlit. Porém, isso fica pra depois, vamos focar na nossa api.

A idéia é extrair de alguma api os dados dos próximos confrontos de diversos campeonatos e armazená-los em um csv (dataframe) ou em num banco como tinydb ou sqlite

Eis algumas Histórias de Usuário da aplicação:

## Dentre varias ligas, selecionar os jogos de top X vs ultimos Y
A idéia é: partindo dos dados dos próximos confrontos de diversos campeonatos, filtrar e retornar confrontos entre times do topo contra times do fundo da tabela.

##  Deve visualizar estatisticas detalhadas dos confrontos filtrados
Criar rota que recebe como parametro uma referencia para um confronto, e retorna um JSON com as estatisticas detalhadas do confronto.

### Estatísticas
Placar dos últimos confrontos;
Numero de cartões;
Média de cartões por time;
Média de cartões por mando de campo;
Média de gols por time no campeonato, por mando de campo;
Média de escanteios por time;
Win/Lose streak (a partir de 75% dos últimos 5 jogos);


Como poderiamos iniciar o desenvolvimento dessa aplicacao? No momento, ela possui um repositorio e ja inicializei um projeto de fastapi
```

<br><br>

### Resposta

```
Desenvolver uma aplicação como essa envolve várias etapas. Vou dividir o processo em partes menores para facilitar o entendimento e o desenvolvimento:

Configuração Inicial:

Você já tem um repositório e inicializou um projeto FastAPI, o que é um excelente começo.
Certifique-se de que seu ambiente de desenvolvimento esteja configurado corretamente (Python, FastAPI, etc.).
Pesquisa e Integração da API de Dados de Futebol:

Você precisará encontrar uma API de dados de futebol que forneça informações sobre jogos, equipes, resultados, estatísticas, etc. Alguns exemplos incluem a API-Football, Sportmonks, entre outras. Certifique-se de que a API escolhida tenha todos os dados necessários para suas estatísticas.
Depois de escolher a API, você precisará se familiarizar com a documentação dela para entender como fazer requisições e interpretar as respostas.
Modelagem de Dados e Armazenamento:

Decida sobre o modelo de dados que você usará internamente. Como você mencionou o uso de CSV, SQLite ou TinyDB, o modelo não precisa ser muito complexo, mas deve ser capaz de armazenar todas as informações necessárias.
Configure o método de armazenamento de dados escolhido. Se for um banco de dados, você precisará configurar tabelas e conexões; se for um CSV, precisará definir a estrutura do arquivo.
Desenvolvimento de Endpoints da API:

Crie endpoints para interagir com a API de dados de futebol e processar as informações. Isso pode incluir um endpoint para recuperar jogos futuros, outro para filtrar com base nas suas condições (top X vs. últimos Y), etc.
Implemente a lógica de filtragem para selecionar os jogos de interesse.
Crie um endpoint que aceite uma referência a um jogo e retorne estatísticas detalhadas.
Implementação de Estatísticas:

Desenvolva funções para calcular as várias estatísticas que você deseja acompanhar. Muitas dessas estatísticas podem exigir dados históricos, então certifique-se de que sua API de dados de futebol escolhida suporte o acesso a esses dados.
Testes:

Escreva testes para seus endpoints e lógica de cálculo de estatísticas para garantir que tudo esteja funcionando como esperado.
Documentação e Implantação:

Documente sua API, explicando o que cada endpoint faz, quais parâmetros aceita e o que retorna.
Prepare sua aplicação para implantação. Dependendo de onde você planeja hospedá-la, esse processo pode variar.
Iteração e Feedback:

Após ter uma versão inicial funcionando, compartilhe-a com usuários em potencial para obter feedback.
Faça melhorias e adicione novos recursos com base no feedback recebido.
Para o futuro, quando você quiser adicionar uma interface de bot do Telegram ou uma página interativa com Streamlit, você já terá uma base sólida para construir essas características, pois sua API já estará fornecendo os dados necessários.
```

<br><br>

### Resposta 2

```
Ótimo, você já tem uma fonte de dados específica em mente. Vamos elaborar um plano de ação com base nisso.

Integração com a API-Football:

Primeiro, você precisará se registrar na API-Football, se ainda não o fez, para obter uma chave de API que permitirá que você faça solicitações à API.
Familiarize-se com a documentação da API-Football para entender como recuperar as informações necessárias. Especificamente, você precisará entender os endpoints para recuperar as partidas do dia e a tabela de classificação.
Desenvolvimento dos Endpoints da FastAPI:

Endpoint para recuperar jogos do dia: Crie uma função que faça uma solicitação à API-Football para obter os jogos do dia para as ligas especificadas. Você precisará passar a lista de IDs das ligas como parâmetro para esta função.
Endpoint para recuperar a tabela de classificação: Similarmente, você precisará de uma função que possa recuperar a tabela de classificação atualizada para uma liga específica.
Armazenamento de Dados:

Após recuperar os dados da API-Football, você precisará decidir como quer armazená-los. Dependendo da sua escolha (SQLite, TinyDB, CSV), o processo será ligeiramente diferente, mas em geral, você precisará salvar os dados em um formato que preserve a estrutura e permita consultas fáceis mais tarde.
Lógica de Filtragem:

Com os dados armazenados, você precisará implementar a lógica para filtrar os jogos do dia. Por exemplo, se você quer confrontos entre times do topo e times do fundo da tabela, precisará consultar a tabela de classificação e os jogos do dia, e depois cruzar essas informações para encontrar as partidas que atendem aos seus critérios.
Testes e Depuração:

Certifique-se de escrever testes para suas novas funções e endpoints, e corrija quaisquer bugs que surgirem durante o processo de teste.
Agendamento e Atualizações Automáticas:

Dependendo de como você quer que sua aplicação funcione, você pode precisar implementar algum tipo de tarefa agendada que atualize automaticamente os jogos do dia e as tabelas de classificação em seu banco de dados.
Documentação:

Documente as funções e endpoints que você criou, explicando o que eles fazem, os parâmetros que aceitam e o formato dos dados que retornam.
```

<br><br>
