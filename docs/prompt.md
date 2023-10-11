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
