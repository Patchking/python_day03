#!/bin/bash

python3.11 get_ansible.py ../../materials/todo.yml
ansible-playbook deploy.yml -i ~/.ansible/hosts