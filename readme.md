# Projeto de Gerência de Redes 2024 B

## Integrantes

    - Maria 
    - Luís
    - Bento
    - Thierry

## Descrição

    Projeto de Gerência de Redes 2024 B

Projeto está sendo desenvolvido em Python 3.12, e utilizando Debian 12 para a execução.

É necessário estar com o GCC instalado na máquina.

    $ apt update
    $ apt-get install gcc && python3-dev -y
    $ pip install -r requirements.txt

### Compilação no Windows

Tentei no MSYS2 e cansei de tentar. Nem lembro o problema. Eu travava num `UnicodeDecodeError` por algum motivo besta.

Aí instalei Python 3.12 nativo, o oficial mesmo, nada de Anaconda, fiz o `venv` dentro do PowerShell bonitinho, deu tudo certo.

Eu tenho ferramentas de desenvolvimento de C/C++ do Visual Studio 2022, e Clang e GCC pelo MSYS2, imagino que o `pip install` tenha usado algum deles? Não sei.

### Compilação no Android (via Termux)

O `pip` tenta _buildar_ o `ninja` e `patchelf`, mas eles existem no Termux, então:

    $ pkg install ninja patchelf libpcap
