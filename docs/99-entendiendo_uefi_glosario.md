# Glosario

---

<span style="color: red; font-weight: bold;">
SIN REVISAR A PARTIR DE AQUÍ
</span>

---

## Formato / Formatear
<a name="formato"></a>

**Formatear** es el proceso de preparar una unidad o partición para almacenar datos creando un sistema de archivos.  
El **formato** determina la estructura de almacenamiento, compatibilidad y características del sistema de archivos.

> Ejemplo: Formatear una partición con FAT32 en Linux:
> ```bash
> mkfs.fat -F32 /dev/sda1
> ```

---

## Sistema de archivos
<a name="sistema-de-archivos"></a>

Un **sistema de archivos** es la forma en que un sistema operativo organiza y gestiona los datos en una unidad o partición.  
Incluye la manera de almacenar archivos, directorios, permisos, metadatos y cómo se accede a ellos.

Ejemplos comunes:  
- FAT32  
- NTFS  
- ext4  
- APFS

---

## Unidad
<a name="unidad"></a>

Una **unidad** es cualquier dispositivo de almacenamiento que puede contener datos y ser reconocido por un sistema operativo.  
Ejemplos de unidades incluyen discos duros (HDD), unidades de estado sólido (SSD), pendrives USB, tarjetas SD, etc.

> Nota: En el contexto de particiones, a veces se denomina "unidad lógica" a cada sección del disco.

---