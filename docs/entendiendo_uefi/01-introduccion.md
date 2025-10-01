# Entendiendo UEFI

---
## 1. Introducción

### 1.1 Contexto: por qúe necesitamos UEFI

Cuando queremos ejecutar un programa, el ordenador **deberá** leer de algún lugar sus instrucciones (por ejemplo, desde
un disco duro o un pendrive) y cargarlas en la **memoria RAM**. La **CPU** ejecuta las instrucciones desde la RAM.

Pero la RAM es volátil, es decir, al apagar el ordenador, se vacía y pierde los datos almacenados. Así, cuando se
enciende un ordenador, debe haber un responsable capaz de subir a la memoria el **sistema operativo** y
lanzarlo para que todo empiece a funcionar.

---

### 1.2 Breve historia: BIOS → EFI → UEFI

Haciendo un poco de historia, de esto se encargaba la **BIOS** (desde 1975). Esto es un circuito integrado que se 
encontraba en las placas madre y que contenía, entre otras cosas, las instrucciones necesarias para:

1. Localizar un sistema operativo en alguno de los discos disponibles.
2. Cargarlo en memoria para que la **CPU** pueda ejecutarlo.

> **Nota:** La BIOS es _no volátil_, para que sus datos no se pierden al apagar el ordenador.

**BIOS**, según han ido avanzando los componentes de los
equipos, se ha quedado obsoleta. Tiene limitaciones importantes que si no se salvan,
hacen que los ordenadores modernos no puedan avanzar. Sin
entrar en detalles, pero a modo de ejemplo, **BIOS** no es capaz de
arrancar un sistema operativo que se encuentre instalado en un disco
cuya capacidad sea mayor de 2TB.

Así, *Intel* desarrolla **EFI** alrededor del año 2000 para
sus microprocesadores con la nueva arquitectura **Itanium**. **EFI**
pasó a sustituir **BIOS** en aquellas placas preparadas para estos
procesadores. Esto permitió una interfaz más moderna entre hardware y sistema operativo.

Pero el resto de jugadores no se querían quedar fuera así
que otras empresas con intereses al respecto (AMD, Lenovo, Dell, Apple y
Microsoft, además de Intel) formaron una alianza para crear la fundación
**UEFI** con el objetivo de desarrollar **EFI**, el trabajo iniciado por
Intel.

> **Nota:** UEFI es solo una **especificación**. Cada fabricante desarrolla su propia implementación.  
> La referencia más conocida es [EDK2](https://github.com/tianocore/edk2), escrita en C.

{%
    include-markdown "./footer.md"
%}

