import numpy as np
from pyproj import Transformer

lista = [(2766000, 2280700)]
listaA = [(-8.88230626,41.86407695,)]
def TransforInterfaz(lista):
    transformer = Transformer.from_crs('EPSG:3035', 'EPSG:4326',always_xy=True)

    cordsUTM = np.array(list(transformer.itransform(lista)))

    a= cordsUTM [:,0]
    b = cordsUTM [:, 1]

def TransforOpt(lista):
    transformer = Transformer.from_crs('EPSG:4326', 'EPSG:3035',always_xy=True, area_of_interest='Europe')

    cordsUTM = np.array(list(transformer.itransform(lista)))

    a= cordsUTM [:,0]
    b = cordsUTM [:, 1]

    print(a)
    print (b)

TransforOpt(listaA)