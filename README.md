# ChatGPT BOT 0.0.1

BOT para Discord que utilizar a api do [ChatGPT](https://chat.openai.com/chat) para responder perguntas

### Python (com [PIP](https://www.treinaweb.com.br/blog/gerenciando-pacotes-em-projetos-python-com-o-pip))
```py
python ^= 3.10
```
Caso queira instalar o python utilizando [**Anaconda**](https://www.anaconda.com/)
```py
conda create -n chatgpt_bot python=3.10
conda activate chatgpt_bot
```

### Dependências
No diretório clonado, envie o seguinte comando
```
python -m pip install -r requirements.txt
```


### Como utilizar

1. Configure as variáveis de ambiente com o Token Discord e a Chave de Acesso da API do OpenIA

    | Variável | Descrição |
    | ------ | ------ |
    | CHATGPT_BOT_TOKEN | Token obtido na [plataforma de desenvolvedores do Discord](https://discord.com/developers/applications)
    | CHATGPT_API_KEY | Chave da API gerada na [plataforma da OpenIA](https://beta.openai.com/account/api-keys)

2. Após criar as variáveis de ambiente, no diretório da aplicação, execute o seguinte comando:
    ```python
    python main.py
    ```

3. No discord escreva o que deseja que o BOT faça, utilizando o prefixo `/gpt` para que ele entenda que você está direcionando a mensagem para ele
    ![Imagemd e Exemplo](https://media.discordapp.net/attachments/979061713171251243/1057444342119284826/image.png)
