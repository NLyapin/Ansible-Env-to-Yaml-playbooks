# Ansible Env-to-YAML Playbooks

Python скрипт для конвертации переменных окружения в YAML формат с Ansible playbook'ами для автоматизации.

## Файлы

- `env-to-yaml.py` - Python скрипт для конвертации переменных окружения
- `env-playbook-from-file.yml` - Playbook для чтения переменных из .env файла
- `env-playbook-from-shell.yml` - Playbook для чтения переменных из shell окружения  
- `env-playbook-to-file.yml` - Playbook для сохранения переменных в YAML файл
- `env.template` - Пример .env файла

## Использование

### Python скрипт

```bash
# Конвертация .env файла в YAML
python3 env-to-yaml.py -in .env

# Конвертация shell переменных в YAML
python3 env-to-yaml.py

# Сохранение в файл
python3 env-to-yaml.py -in .env -out variables.yaml

# С опциями преобразования
python3 env-to-yaml.py -in .env -l -p "app"
```

### Ansible playbook'и

```bash
# Чтение из .env файла
ansible-playbook env-playbook-from-file.yml

# Чтение из shell окружения
ansible-playbook env-playbook-from-shell.yml

# Сохранение в YAML файл
ansible-playbook env-playbook-to-file.yml
```

## Пример .env файла

```bash
# CI/CD переменные
CI_PROJECT_DIR=/opt/projects/crm-integration
CI_COMMIT_BRANCH=main

# SSH подключение
ANSIBLE_RUN_SSH_USER=deploy
ANSIBLE_RUN_SSH_PASSWORD=secure_password_123

# Container Registry
CONTAINER_REGISTRY=registry.example.com
CONTAINER_REGISTRY_USER=deploy_user
CONTAINER_REGISTRY_PASSWORD=registry_password_123

# PHP конфигурация
PHP_VERSION=8.2
NGINX_HOST=crm.example.com

# База данных
POSTGRES_DB=crm_integration
POSTGRES_USER=crm_user
POSTGRES_PASSWORD=db_password_456
```

## Требования

- Python 3.6+
- Ansible 2.9+
- PyYAML