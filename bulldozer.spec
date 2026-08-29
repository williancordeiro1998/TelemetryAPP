[app]
# (str) Título do seu aplicativo
title = Telemetry App

# (str) Nome do pacote
package.name = telemetryapp

# (str) Domínio do pacote (necessário para android/ios)
package.domain = org.willian

# (str) Pasta onde está o código fonte (o ponto significa a pasta atual)
source.dir = .

# (list) Extensões de arquivos que farão parte do app
source.include_exts = py,png,jpg,kv,atlas

# (str) Versão do aplicativo
version = 0.1

# (list) Bibliotecas necessárias para o app rodar
requirements = python3, kivy, pyjnius, urllib3

# (str) Orientação da tela (portrait = em pé)
orientation = portrait

# (list) Permissões necessárias no Android (MUITO IMPORTANTE PARA SEU CÓDIGO)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (list) Arquiteturas de processadores Android suportadas
android.archs = arm64-v8a, armeabi-v7a

# (int) Versão mínima da API do Android (Geralmente 21)
android.minapi = 21

# (int) Versão alvo da API do Android (Geralmente 33 ou 34)
android.api = 33

[buildozer]
# (int) Nível de log (2 = debug)
log_level = 2