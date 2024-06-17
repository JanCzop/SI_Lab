import reversio


def tests():
    # SI_HEURISTIC_DEPTH_ALFA_BETA_ALGORITHM

    DEFAULT_DEPTH = 4
    DEFAULT_ALFA = float('-inf')
    DEFAULT_BETA = float('inf')
    DEFAULT_ALGORITHM = 'AB'

   # x_nodes = []
  #  o_nodes = []
  #  results = []

    i = 4
    while not i==5:
        print('DEPTH==',i)
        SI_1 = ['DEFAULT',i, -40, 40, 'AB']
        SI_2 = ['DEFAULT', i, -2, 2, 'AB']
        x,o,r = reversio.start_game_si_vs_si(SI_1,SI_2)
       # x_nodes.append(x)
       # o_nodes.append(o)
       # results.append(o)
        i+=1
   # print_list(x_nodes)
   # print_list(o_nodes)
   # print_list(results)

def print_list(list):
    for elem in list:
        print(elem)