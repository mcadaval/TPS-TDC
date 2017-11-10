import matplotlib.pyplot as plt
import geoip2.database
import gmplot

example = [{'rtt': 1}, {'rtt': 2}]


def rtt_between_jumps_graph(hops):
    x = [hop.hop_numb for hop in hops]
    y = [hop.rtt for hop in hops]

    plt.title('Gráfico de RTT entre saltos')
    plt.xlabel('Número de salto')
    plt.xticks(range(0, hops[-1].hop_numb + 1))
    plt.ylabel('RTT de salto (milisegundos)')    
    plt.plot(x, y, '-o')
    plt.show()


# TODO falta ver como deberia hacerse este grafico
def rtt_between_jumps_vs_zrtt_graph(hops, z_rtt_values):
    x_rtt = [hop.hop_numb for hop in hops]
    y_rtt = [hop.rtt for hop in hops]

    x_z_rtt = z_rtt_values
    y_z_rtt = [hop.rtt for hop in hops]

    plt.title('Gráfico de RTT entre saltos')
    plt.xticks(range(0, hops[-1].hop_numb + 1))
    plt.xlabel('Número de salto')
    plt.ylabel('RTT en milisegundos')    
    plt.plot(x_rtt, y_rtt, '-o')
    plt.plot(x_z_rtt, y_z_rtt, '-o')
    plt.show()


def no_reponse_percentage(hops):
    max_ttl = len(hops)
    ttl_responses = [False] * max_ttl

    for hop in hops:
        if hop.ip_address != None:
            ttl_responses[hop.hop_numb-1] = True
    
    responses_number = 0
    for value in ttl_responses:
        if value == True: 
            responses_number += 1

    percentage = 100 * responses_number / max_ttl
    return percentage

def build_map(hops):

    # saco null hops
    hops = [hop for hop in hops if hop.ip_address != None]

    # abro db
    db_reader = geoip2.database.Reader('../database/GeoLite2-City.mmdb')

    # saco toda la info sobre cada ip de la db
    latitudes = []
    longitudes = []
    countries = []
    for hop in hops:
        if hop.ip_address != None:
            try:
                response = db_reader.city(hop.ip_address)
                latitudes.append(response.location.latitude)
                longitudes.append(response.location.longitude)
                countries.append(response.country.names['es'])
            except geoip2.errors.AddressNotFoundError:
                # si caemos aca es que no encontro la ip en la db. Sigue con el siguiente hop
                pass 

    # creo mapa centrado en el punto inicial del camino
    mymap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], 5)
    
    # dibujo camino
    mymap.plot(latitudes, longitudes, "green", edge_width=10)

    # dibujo todos los puntos en el camino
    for i in range(0, len(latitudes)):
        title = "IP: " + hops[i].ip_address + "\\nTTL: " + str(hops[i].hop_numb) + "\\nPais: " + countries[i]
        if i == 0:
            color = 'red'
            title = title + "\\nPunto inicial" 
        else:
            color = 'blue'
        mymap.marker(latitudes[i], longitudes[i], color, None, title)
    
    # genero mapa html
    mymap.draw('./mymap.html')
