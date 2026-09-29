def read(file_name):
    vuelos = []
    try:
        with open(file_name, "r") as f:
            for line in f:
                datos = line.strip().split(",")
                
                destino = datos[0]
                duracion = int(datos[1])
                aerolinea = datos[2]
                
                vuelos.append((destino, duracion, aerolinea))
                
    except FileNotFoundError:
        return []
    
    return vuelos


def extract(outputread):
    vuelos_dict = dict()
    
    for destino, duracion, aerolinea in outputread:
        
        if aerolinea not in vuelos_dict:
            vuelos_dict[aerolinea] = []
        
        es_largo = duracion >= 180
        
        info_tupla = (destino, duracion, es_largo)
        
        vuelos_dict[aerolinea].append(info_tupla)
    
    return vuelos_dict


def transform(outputread, outputextract):
    cantidad_largos = 0
    
    for aerolinea, vuelos in outputextract.items():
        for destino, duracion, es_largo in vuelos:
            if es_largo:
                cantidad_largos += 1
    
    cantidad_total = len(outputread)
    cantidad_aerolineas = len(outputextract)
    
    proporcion_largos = cantidad_largos / cantidad_total
    promedio_vuelos_aerolinea = cantidad_total / cantidad_aerolineas
    
    suma_duraciones = 0
    
    for destino, duracion, aerolinea in outputread:
        suma_duraciones += duracion
    
    duracion_promedio = suma_duraciones / cantidad_total
    
    mayor_aerolinea = ""
    mayor_cantidad = 0
    
    for aerolinea, vuelos in outputextract.items():
        if len(vuelos) > mayor_cantidad:
            mayor_cantidad = len(vuelos)
            mayor_aerolinea = aerolinea
    
    return [
        proporcion_largos,
        promedio_vuelos_aerolinea,
        duracion_promedio,
        mayor_aerolinea
    ]


def load(outputtransform, outputextract):
    
    print("Proporción de vuelos largos:", outputtransform[0])
    print("Promedio de vuelos por aerolínea:", outputtransform[1])
    print("Duración promedio de los vuelos:", outputtransform[2])
    print("Aerolínea con más vuelos:", outputtransform[3])
    
    print()
    
    for i, (aerolinea, vuelos) in enumerate(outputextract.items(), 1):
        print(i, "-", aerolinea + ":", len(vuelos), "vuelos")


# ============================================================
# USO DEL ETL
# ============================================================

file_name = "flights.txt"

outputread = read(file_name)
outputextract = extract(outputread)
outputtransform = transform(outputread, outputextract)
load(outputtransform, outputextract)


# ============================================================
# VERIFICACIÓN — NO TOCAR desde acá hasta el final del archivo
# ============================================================

with open("flights.txt", "w") as f:

    f.write(
        "Madrid,150,Iberia\n"
        "Roma,195,Ryanair\n"
        "Paris,110,Air France\n"
        "Barcelona,175,Iberia\n"
        "Berlin,210,Ryanair\n"
        "Lisboa,190,Iberia\n"
    )

file_name = "flights.txt"
outputread = read("flights.txt")