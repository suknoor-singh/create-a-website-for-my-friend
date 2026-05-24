#!/usr/bin/env bash
set -euxo pipefail

sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git

sudo mkdir -p /var/www/ajmaniandlawpartners
sudo chown "$USER":"$USER" /var/www/ajmaniandlawpartners
