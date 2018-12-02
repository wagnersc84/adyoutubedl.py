#!/bin/bash
divisor="\n\n================================================================================"
script='adyoutubedl.py'
nomedoinstalador='instalador.sh'
linkdoinstalador='https://raw.githubusercontent.com/wagnersc84/adyoutubedl.py/master/instalador'
echo -e "$divisor"
echo 'Baixando instalador...'
sudo apt install curl
curl "$linkdoinstalador" -o ./$nomedoinstalador
chmod a+rx ./$nomedoinstalador
echo -e "$divisor"
echo 'Iniciando instalador...'
./$nomedoinstalador
echo -e "$divisor"
rm ./$nomedoinstalador
echo 'fim :)'
echo "Agora já é possivel chamar o $script pelo terminal digitando $script"
echo 'Pressione enter para sair'
read -n 1
