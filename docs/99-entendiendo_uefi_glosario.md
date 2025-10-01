# Glosario

---

<span style="color: red; font-weight: bold;">
SIN REVISAR A PARTIR DE AQUÍ
</span>

---

## Arranque
<a name="arranque"></a>

El **arranque** es el proceso por el cual un ordenador carga el sistema operativo desde una unidad de almacenamiento hasta la memoria RAM y empieza su ejecución.

---

## BIOS
<a name="bios"></a>

La **BIOS** (Basic Input/Output System) es el firmware tradicional de los ordenadores que inicializa el hardware y carga el sistema operativo desde un dispositivo de arranque.

---

## Cabecera GPT
<a name="cabecera-gpt"></a>

Parte de la **tabla de particiones GPT** que contiene información sobre las particiones del disco y su integridad mediante CRC32. Existe una cabecera principal al inicio y una de respaldo al final del disco.

---

## Disco
<a name="disco"></a>

Un **disco** es un dispositivo de almacenamiento permanente, como un HDD o SSD, que contiene una o varias particiones donde se guardan datos.

---

## EFI
<a name="efi"></a>

**EFI** (Extensible Firmware Interface) es la interfaz desarrollada por Intel alrededor del año 2000 que sustituyó a la BIOS en placas Itanium, proporcionando un arranque más moderno y flexible.

---

## ESP (EFI System Partition)
<a name="esp"></a>

Partición obligatoria en sistemas UEFI que contiene ficheros de arranque `.efi`. Normalmente en **FAT32**, con tamaño entre 100–512 MB, y usada por sistemas operativos y gestores de arranque como GRUB2 o Windows Boot Manager.

---

## Formato / Formatear
<a name="formato"></a>

**Formatear** es preparar una unidad o partición para almacenar datos creando un **sistema de archivos**.  
El **formato** determina la estructura de almacenamiento, compatibilidad y características del sistema de archivos.

---

## Gestor de arranque
<a name="gestor-arranque"></a>

Programa que se ejecuta desde la BIOS o UEFI para cargar un sistema operativo.  
Ejemplos: **GRUB2**, **Windows Boot Manager**.

---

## MBR
<a name="mbr"></a>

**MBR** (Master Boot Record) es un esquema de particionamiento antiguo usado en discos compatibles con BIOS.  
Contiene un pequeño código de arranque y una tabla de particiones (máx. 4 primarias).

---

## Partición
<a name="particion"></a>

Sección de un disco que se comporta como una unidad independiente, con su propio sistema de archivos. Permite almacenar datos y arrancar sistemas operativos.

---

## Sistema de archivos
<a name="sistema-de-archivos"></a>

Forma en que un sistema operativo organiza y gestiona los datos en una unidad o partición.  
Ejemplos: **FAT32**, **NTFS**, **ext4**, **APFS**.

---

## Tabla de particiones
<a name="tabla-particiones"></a>

Estructura que indica cómo está dividido un disco y qué contiene cada partición: tipo de sistema de archivos, tamaño, bandera de arranque, etc. Puede ser **MBR** o **GPT**.

---

## UEFI
<a name="uefi"></a>

**UEFI** (Unified Extensible Firmware Interface) es la especificación de interfaz de firmware que reemplaza a la BIOS en la mayoría de los equipos modernos, permitiendo un arranque más flexible y seguro.

---

## Unidad
<a name="unidad"></a>

Cualquier dispositivo de almacenamiento que pueda contener datos y ser reconocido por un sistema operativo.  
Ejemplos: discos duros, SSD, pendrives, tarjetas SD.

---

## Windows Boot Manager / BCD
<a name="bcd"></a>

Gestor de arranque de Windows que se apoya en la **partición EFI**.  
Incluye herramientas como `bcdboot` y `bcdedit` para configurar entradas de arranque y ficheros de arranque `.efi`.
