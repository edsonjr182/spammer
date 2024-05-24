
# Spammer via webhook

Este projeto em Python utiliza a biblioteca Tkinter para criar uma interface gráfica que facilita o envio de mensagens personalizadas para uma lista de contatos importada de um arquivo Excel. A aplicação suporta o envio de mensagens de texto e a inclusão de imagens, permitindo um envio altamente personalizado e automatizado.

## Funcionalidades

- **Carregar arquivo Excel**: Importa contatos e outros dados de um arquivo Excel para serem utilizados nas mensagens.
- **Carregar e redimensionar imagem**: Permite carregar uma imagem, que é automaticamente redimensionada e codificada em base64 para envio.
- **Enviar mensagens personalizadas**: Utiliza placeholders para personalizar mensagens baseadas nos dados dos contatos.
- **Interface gráfica amigável**: Fornece uma interface visual para fácil operação.
- **Relatório de status**: Exibe o status de cada envio na interface, permitindo acompanhamento em tempo real.

## Tecnologias Utilizadas

- Python
- Tkinter
- Pandas
- PIL (Python Imaging Library)
- Requests

## Como Usar

### Configuração Inicial

1. **Instalação de Dependências**: Antes de executar o aplicativo, instale as dependências necessárias usando o seguinte comando:
   ```bash
   pip install pandas Pillow requests
   ```

### Executando a Aplicação

1. **Inicie o Aplicativo**: Execute o script Python. A interface gráfica será exibida.
2. **Carregar Arquivo Excel**: Clique em "Carregar Excel" e selecione o arquivo Excel contendo os dados dos contatos. O arquivo deve estar no formato `.xlsx` ou `.xls`.
3. **Carregar Imagem (Opcional)**: Clique em "Carregar Imagem" para adicionar uma imagem que será enviada junto com as mensagens.
4. **Limpar Imagem (Opcional)**: Caso deseje remover a imagem selecionada, clique em "Limpar Imagem".
5. **Digite a Mensagem**: Insira a mensagem no campo de texto. Utilize chaves `{}` para indicar placeholders que serão substituídos pelos dados do Excel. Por exemplo, `{nome}`.
6. **Adicionar Placeholders**: Clique nos botões dos placeholders (ex: nome, valor, data) para inseri-los na mensagem.
7. **Configurar ID de Cliente e Intervalo**: Forneça o ID do cliente e o intervalo entre os envios de mensagens em milissegundos.
8. **Enviar Mensagens**: Clique em "Enviar Mensagens" para começar o processo de envio.

### Monitoramento

- **Barra de Progresso**: Uma barra de progresso e um rótulo de porcentagem mostrarão o progresso do envio das mensagens.
- **Log de Status**: O status de cada envio será exibido no campo "Status dos envios", onde você pode verificar informações sobre o sucesso ou falhas no envio.

## Estrutura do Código

- O código está dividido em funções específicas para cada operação, como carregar arquivos, enviar mensagens e atualizar o status.

## Contribuições

Contribuições para melhorar a aplicação são bem-vindas. Sinta-se à vontade para clonar o repositório, fazer suas alterações e enviar um pull request.
