#!/bin/bash
divisor="\n\n==================================================================================================="
script='adyoutubedl.py'
nomedoinstalador='instalador.sh'
linkdoinstalador='https://cdn.fbsbx.com/hphotos-xfp1/v/t59.2708-21/12316689_1147835421901014_536093735_n.jpg/instalador.jpg?oh=3ebf5bdc311f872fc6cfe2846ef4f3d2&oe=56683501&dl=1'
echo -e "$divisor"
echo 'Baixando instalador...'
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
