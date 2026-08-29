# TelemetryAPP

Um aplicativo multiplataforma (Desktop e Android) desenvolvido em Python utilizando o framework **Kivy**. Este projeto foi criado com propósitos educacionais para demonstrar o uso de threads, coleta de dados de sistema e comunicação HTTP em segundo plano.

O aplicativo utiliza a interface gráfica do Kivy para manter o processo ativo no sistema operacional, enquanto uma *thread* separada coleta metadados básicos (versão do sistema, modelo do dispositivo) e os transmite via HTTP POST para um endpoint de testes.

## 🚀 Funcionalidades

- **Coleta de Metadados:** Identifica o modelo do dispositivo e sistema operacional.
- **Multithreading:** O loop de rede roda independente da interface gráfica, evitando o congelamento da tela.
- **Multiplataforma:** Funciona no Windows para testes locais e pode ser compilado para Android.
- **Graceful Shutdown:** Encerramento seguro da thread de rede ao fechar o app.

## 📋 Pré-requisitos e Teste Local

Para testar o código no computador (Windows/Linux):
1. Python 3.10+
2. Instale as dependências:
   ```bash
   pip install kivy
