screen -dmS "A" python3 COMP3221_DiVr.py A 6000 Aconfig.txt
screen -dmS "B" python3 COMP3221_DiVr.py B 6001 Bconfig.txt
screen -dmS "C" python3 COMP3221_DiVr.py C 6002 Cconfig.txt
screen -dmS "D" python3 COMP3221_DiVr.py D 6003 Dconfig.txt
screen -dmS "E" python3 COMP3221_DiVr.py E 6004 Econfig.txt
screen -dmS "F" python3 COMP3221_DiVr.py F 6005 Fconfig.txt
screen -dmS "G" python3 COMP3221_DiVr.py G 6006 Gconfig.txt
screen -dmS "H" python3 COMP3221_DiVr.py H 6007 Hconfig.txt
screen -dmS "I" python3 COMP3221_DiVr.py I 6008 Iconfig.txt
screen -dmS "J" python3 COMP3221_DiVr.py J 6009 Jconfig.txt
#{'A': 0,
# 'B': 2.4000000000000004
# 'C': 4.200000000000001
# 'D': 3.1000000000000005,
#  E': 4.6000000000000005,
# 'F': 2.3,
# 'G': 2.2,
#  'H': 5.1000000000000005,
#  'I': 4.6000000000000005,
##  'K': 7.7}
#alias        pkill SCREEN

# kill -9 $(ps -A | grep python | awk '{print $1}')

#{'H': 0,
#'E': 0.5,
#\'D': 2.0,
#\'B': 2.7,
#\'G': 2.9000000000000004,
#'C': 3.1,
# 'I': 3.5,
# 'F': 5.0,
# 'A': 5.1000000000000005,
# 'K': 7.0}

#Least cost path from A to B: GB, link cost: 2.4
#Least cost path from A to C: GBDC, link cost: 4.2
#Least cost path from A to D: GBD, link cost: 3.1
#Least cost path from A to E: GBDE, link cost: 4.6
#Least cost path from A to F: F, link cost: 2.3
#Least cost path from A to G: G, link cost: 2.2
#Least cost path from A to H: GBDEH, link cost: 5.1
#Least cost path from A to I: GBDI, link cost: 4.6
#Least cost path from A to J: FJ, link cost: 7.7