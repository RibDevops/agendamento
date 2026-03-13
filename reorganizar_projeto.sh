#!/bin/bash

echo "==== BACKUP DO PROJETO ===="

mkdir backup_projeto
cp -r agenda backup_projeto/
cp -r whatsapp backup_projeto/

echo "Backup criado em backup_projeto/"

echo "==== CRIANDO NOVA ESTRUTURA ===="

mkdir -p agenda/robots
mkdir -p agenda/integrations
mkdir -p agenda/tasks

echo "Pastas criadas."

echo "==== MOVENDO ARQUIVOS ===="

# scraper vira robot
mv agenda/scraper.py agenda/robots/agenda_robot.py

# execução do robô
mv agenda/services/executar_robo.py agenda/tasks/executar_robo.py

# serviços
mv agenda/services/eventos.py agenda/services/evento_service.py
mv agenda/services/enviar_tarefas.py agenda/services/envio_service.py

# integração whatsapp
mv agenda/services/whatsapp_mensagem.py agenda/integrations/whatsapp_client.py

echo "Arquivos movidos."

echo "==== REMOVENDO ARQUIVOS DUPLICADOS ===="

rm -f agenda/hash_utils.py
rm -f agenda/services/teste.py
rm -f agenda/services.py

echo "Arquivos desnecessários removidos."

echo "==== FINALIZADO ===="
echo "Agora revise os arquivos antes de rodar o sistema."