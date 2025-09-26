#!/usr/bin/env python3

import os
import sys
import yaml
import argparse
from pathlib import Path

def parse_env_file(env_file_path):
    env_vars = {}

    with open(env_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith('#'):
            i += 1
            continue

        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Check if this is a multiline value (starts with quotes but doesn't end with quotes on same line)
            if (value.startswith('"') and not value.endswith('"')) or (value.startswith("'") and not value.endswith("'")):
                # This is a multiline value
                multiline_value = value[1:]  # Remove opening quote
                i += 1

                while i < len(lines):
                    next_line = lines[i].strip()

                    if next_line and '=' in next_line and not next_line.startswith(' '):
                        break

                    if next_line and not next_line.startswith('#'):
                        if next_line.endswith('"') or next_line.endswith("'"):
                            multiline_value += '\n' + next_line[:-1]  # Remove closing quote
                            break
                        else:
                            multiline_value += '\n' + next_line

                    i += 1

                env_vars[key] = multiline_value
                continue
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            if value.startswith('-----BEGIN') or value.startswith('-----END'):
                multiline_value = value
                i += 1

                while i < len(lines):
                    next_line = lines[i].strip()

                    if next_line and '=' in next_line and not next_line.startswith(' '):
                        break

                    if next_line and not next_line.startswith('#'):
                        multiline_value += '\n' + next_line

                    i += 1

                env_vars[key] = multiline_value
                continue
            else:
                env_vars[key] = value

        i += 1

    return env_vars

def parse_shell_env():
    env_vars = {}
    for key, value in os.environ.items():
        clean_value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')
        env_vars[key] = clean_value
    return env_vars

def convert_to_yaml(env_vars):
    yaml_vars = {}

    for key, value in env_vars.items():
        if '\n' in value and (value.startswith('-----BEGIN') or value.startswith('-----END')):
            yaml_vars[key] = value
        else:
            yaml_vars[key] = value

    return yaml_vars

def main():
    parser = argparse.ArgumentParser(description="Конвертирует .env файл или переменные окружения в YAML")
    parser.add_argument("-in", "--input", help="Путь к .env файлу (если не указан, читает из переменных окружения)")
    parser.add_argument("-out", "--output", help="Путь к выходному YAML файлу (если не указан, выводит в stdout)")
    parser.add_argument("-l", "--lowercase", action="store_true", help="Преобразовать все имена переменных в нижний регистр")
    parser.add_argument("-p", "--prefix", help="Добавить префикс к именам переменных (например: -p 'env' даст env_VARIABLE)")
    args = parser.parse_args()

    if args.input:
        env_file = args.input
        if not os.path.exists(env_file):
            print(f"Ошибка: файл {env_file} не найден")
            sys.exit(1)
        env_vars = parse_env_file(env_file)
    else:
        env_vars = parse_shell_env()

    yaml_vars = convert_to_yaml(env_vars)

    if args.prefix:
        yaml_vars = {f"{args.prefix}_{key}": value for key, value in yaml_vars.items()}

    if args.lowercase:
        yaml_vars = {key.lower(): value for key, value in yaml_vars.items()}

    yaml_lines = []
    for key, value in yaml_vars.items():
        if '\n' in value and (value.startswith('-----BEGIN') or value.startswith('-----END')):
            yaml_lines.append(f'"{key}": |-')
            for line in value.split('\n'):
                yaml_lines.append(f"  {line}")
        else:
            escaped_value = str(value).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            yaml_lines.append(f'"{key}": "{escaped_value}"')

    yaml_output = '\n'.join(yaml_lines)

    if args.output:
        output_file = args.output
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(yaml_output)
            print(f"YAML сохранен в файл: {output_file}")
        except Exception as e:
            print(f"Ошибка при записи в файл {output_file}: {e}")
            sys.exit(1)
    else:
        print(yaml_output)

if __name__ == "__main__":
    main()