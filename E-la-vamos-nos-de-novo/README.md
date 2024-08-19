# Python DApp Template

This is a template for Python Cartesi DApps. It uses python3 to execute the backend application.
The application entrypoint is the `dapp.py` file.

INTEGRANTES DO GRUPO:
Lucas Gabriel de Oliveira Costa
Matheus de Oliveira Lima
Matheus Lopes Ferreira Lima

No diretório do projeto inicialmente é preciso dar 2 comandos para começar a rodar o Cartesi:

cartesi build
cartesi run

Esses 2 comandos vai colocar o servidor local dentro do Docker para funcionar. O terminal que foram executados esse comando ficará com ele rodando, para dar sequência a requisições é necessário abrir outro terminal no diretório do projeto.

Aberto este outro terminal é possível executar o script exec.sh.

Primeiramente será necessário informar o nome do documento que você vai querer salvar dentro do Cartesi. Logo após você seleciona as seguintes opções (somente para testar):

Aperte enter selecionando Foundy,
Aperte enter para selecionar a rota padrão entre parênteses,
Aperte enter para selecionar a Wallet Mnemonic,
Aperte enter para selecionar a entrada padrão do Mnemonic entre parênteses,
Aperte enter para selecionar a primeira opção de Account,
Aperte enter para selecionar a entrada padrão da Application adress,

Nisso ele vai gerar o Input sent e enviar o documento para o cartesi.

Vai aparecer no terminal a seguinte informação:

Nodes disponíveis:
- Node index: 0

Inputs disponíveis:
- Input index: 0
- Input index: 1

Como o trabalho é simples só teremos o Node 0, então sempre o payload que vc acabou de enviar é o Node = 0 e com o maior Input, no caso desse exemplo o Input = 1.

Então ao vir as perguntas do Node e Input vc irá preencher com 0 sempre e o index Input maior.

Digite o nome do arquivo de entrada (ex: doc_rtn_0_0.hex)

Digite o nome do arquivo .sig para verificar (ex: doc_rtn_0_0.sig)

Se der tudo certo, haverá a saida: Assinatura verificada com sucesso!

Caso queira limpar os documentos criados somente execute: ./clean.sh

