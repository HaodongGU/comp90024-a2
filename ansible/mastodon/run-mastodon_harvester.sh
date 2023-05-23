#!/bin/bash

. ../unimelb-comp90024-2023-grp-68-openrc.sh; ansible-playbook -i hosts -vv docker_harvester.yaml | tee output.txt