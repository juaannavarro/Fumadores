import threading, time, random

papel = threading.Semaphore(0)
tabaco = threading.Semaphore(0)
filtros = threading.Semaphore(0)
green = threading.Semaphore(0)
cerillas = threading.Semaphore(0)
mesa = threading.Semaphore(1)
ingredientes_suficientes = threading.Semaphore(0)


def agente():
    while True:
        ingredientes = [papel, tabaco, filtros, green, cerillas]
        ingredientes_seleccionados = random.sample(ingredientes, 2)
        
        mesa.acquire()
        for i in ingredientes_seleccionados:
            i.release()
            
        print("Agente: ingredientes en la mesa")
        
        if ingredientes_seleccionados[0]._value > 0 or ingredientes_seleccionados[1]._value > 0:
            ingredientes_suficientes.release()
        
def fumador(nombre, ing1, ing2):
    while True:
        ingredientes_suficientes.acquire()
        ing1.acquire()
        ing2.acquire()
        print("Fumador " + nombre + " fumando")
        time.sleep(2)
        print("Fumador " + nombre + " termina de fumar")
        mesa.release()
        

hilos = []

hilo_agente = threading.Thread(target=agente)
hilos.append(hilo_agente)
hilo_agente.start()


fumador1 = threading.Semaphore(0)
fumador2 = threading.Semaphore(0)
fumador3 = threading.Semaphore(0)
fumador4 = threading.Semaphore(0)
fumador5 = threading.Semaphore(0)


hilo_fumador1 = threading.Thread(target=fumador, args=["Papel", papel, tabaco])
hilos.append(hilo_fumador1)
hilo_fumador1.start()

hilo_fumador2 = threading.Thread(target=fumador, args=["Tabaco", tabaco, filtros])
hilos.append(hilo_fumador2)
hilo_fumador2.start()

hilo_fumador3 = threading.Thread(target=fumador, args=["Filtros", filtros, green])
hilos.append(hilo_fumador3)
hilo_fumador3.start()

hilo_fumador4 = threading.Thread(target=fumador, args=["Green", green, cerillas])
hilos.append(hilo_fumador4)
hilo_fumador4.start()

hilo_fumador5 = threading.Thread(target=fumador, args=["Cerillas", cerillas, papel])
hilos.append(hilo_fumador5)
hilo_fumador5.start()

for hilo in hilos:
    hilo.join()
    
print("Fin")