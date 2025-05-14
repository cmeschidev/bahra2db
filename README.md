# bahra2db

Convierte a tablas normalizadas la información de la Base de Asentamientos de la República Argentina (BAHRA)

## Tablas normalizadas

1. Provincias
2. Departamentos
3. Gobiernos Locales
4. Aglomerados
5. Localidades ( Simples y componentes de localidad compuesta )
6. Entidades
7. Parajes
8. Bases antárticas

### Provincias

TODO: Agregar la region a la que pertenece

### Gobiernos locales

Los gobiernos locales pueden ejercer su jurisdicción sobre diferentes departamentos

### Localidades

Incluye a las *localidades simples* y a los *componentes de localidades compuestas*

### Aglomerados

Los aglomerados pueden extenderse a través de varias jurisdicciones provinciales, abarcando en cada una varios gobiernos locales y departamentos.
TODO: Agregar si se releva EPH



Divisón geografica 	Divisón política	Relación	
Provincias	Provincia		1 a 1
Departamentos		En 4 provincias coinciden con el gobierno local (Bs.As, Mendoza, La Pampa, 	1 a N
Localidad compuestas	Gobierno local		
Entidades	Gobierno local	Hereda la de la localidad compuesta	
Localidades	Gobierno local		
Parajes		Salvo en las provincias donde los departamentos cubren todo el territorio dependen del gobierno provincial	
Aglomerados		Generalmente abarcan varios gobiernos locales y departamentos	



### Glosario

Consultar http://www.bahra.gob.ar/descargas/glosario.pdf