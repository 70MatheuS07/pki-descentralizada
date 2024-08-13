# Python DApp Template

This is a template for Python Cartesi DApps. It uses python3 to execute the backend application.
The application entrypoint is the `dapp.py` file.

Inicialmente, usando cryptography, foi feito a geração de chaves pública e privada, além da assinatura. Utilizando o código gera_chave_assinatura.py

Modifiquei o dapp.py, porém está dando alguns erros. O gera_chave_assinatura.py ainda permanece funcionando. Ao executar o comando:

ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 dapp.py

Há um monte de erro seu reportardo no terminal.