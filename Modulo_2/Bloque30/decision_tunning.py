def estimar_costo_de_etiquetar(num_ejemplos, minutos_por_ejemplo, costo_por_hora):
	horas = (num_ejemplos * minutos_por_ejemplo) / 60
	costo = horas * costo_por_hora
	return horas, costo

# el dataset de 8 ejemplos del Bloque 29, a 5 minutos por ejemplo bien etiquetado
horas, costo = estimar_costo_de_etiquetar(8, 5, 25)
print(f"{horas:.2f} horas, aprox ${costo:.2f}")
 
# el mismo calculo, para un dataset de produccion de 200 ejemplos
horas2, costo2 = estimar_costo_de_etiquetar(200, 5, 25)
print(f"{horas2:.2f} horas, aprox ${costo2:.2f}")
print(f"factor de crecimiento en horas: {horas2 / horas:.1f}x, para 25x mas ejemplos")

horas3, costo3 = estimar_costo_de_etiquetar(10000, 2.5, 14)
print(f"{horas3:.2f} horas, aprox ${costo3:.2f}")
print(f"factor de crecimiento en horas: {horas3 / horas:.1f}x, para 25x mas ejemplos")

horas4, costo4 = estimar_costo_de_etiquetar(500, 4, 20)
print(f"{horas4:.2f} horas, aprox ${costo4:.2f}")
print(f"factor de crecimiento en horas: {horas4 / horas:.1f}x, para 500 ejemplos")

horas5, costo5 = estimar_costo_de_etiquetar(100, 2, 20)
print(f"{horas5:.2f} horas, aprox ${costo5:.2f}")
print(f"factor de crecimiento en horas: {horas5 / horas:.1f}x, para 100 ejemplos")

costo_total = costo4 + costo5
print(f"Costo total para 500 ejemplos a 4 minutos y 100 ejemplos a 2 minutos: ${costo_total:.2f}")

