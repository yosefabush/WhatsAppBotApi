#!/bin/sh
gunicorn --chdir app whatsapp_server:app -w 2 --threads 2 -b 0.0.0.0:80
