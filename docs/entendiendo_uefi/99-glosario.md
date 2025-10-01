# Glosario

---

<span style="color: red; font-weight: bold;">
SIN REVISAR 
</span>

---

Este glosario recoge conceptos clave relacionados con UEFI, BIOS, particiones, sistemas de archivos y arranque, con explicaciones ampliadas, ejemplos y diagramas simplificados.

---

## Arranque
El **arranque** es el proceso por el cual un ordenador pasa de estar apagado a ejecutar un sistema operativo.  
Incluye varias fases:

1. **POST (Power-On Self Test):** comprobaciones de hardware (RAM, CPU, dispositivos básicos).  
2. **Firmware (BIOS/UEFI):** inicializa hardware y busca un medio de arranque válido.  
3. **Gestor de arranque:** programa que indica qué sistema operativo o kernel cargar.  
4. **Carga del kernel:** el sistema operativo toma el control del hardware.  

```
[Encendido] → [POST] → [Firmware] → [Gestor de arranque] → [Kernel] → [Sistema operativo]
```

Ejemplo: En un PC moderno con UEFI, el firmware busca en la **partición EFI (ESP)** un archivo `.efi` (por ejemplo, `grubx64.efi`) y lo ejecuta.

---

## BIOS
La **BIOS** (Basic Input/Output System) es el firmware tradicional en PCs (desde 1975).  
Funciones principales:
- Inicializa el hardware.  
- Localiza un dispositivo de arranque.  
- Carga el MBR y transfiere el control.  

**Limitaciones:**
- Máx. discos de 2 TB (por usar direcciones de 32 bits en MBR).  
- Solo 4 particiones primarias.  
- Interfaz básica y lenta.  

Ejemplo visual de arranque BIOS:  
```
[BIOS] → [MBR (primer sector de disco)] → [Bootloader] → [Sistema operativo]
```

---

## BCD (Boot Configuration Data)
El **BCD** es la base de datos de configuración de arranque de Windows, que sustituye al antiguo `boot.ini`.  
Se guarda en la partición EFI y es gestionado por `Windows Boot Manager`.  

Herramientas:
- `bcdboot`: genera los ficheros de arranque.  
  ```bash
  bcdboot C:\Windows /s S: /f UEFI
  ```
- `bcdedit`: permite inspeccionar y modificar las entradas del BCD.  

Ejemplo de consulta con `bcdedit`:
```
Windows Boot Loader
-------------------
identifier              {current}
device                  partition=C:
path                    \Windows\system32\winload.efi
description             Windows 10
```

---

## EFI (Extensible Firmware Interface)
Desarrollada por Intel en 2000 para Itanium, reemplazó la BIOS clásica.  
Ventajas frente a BIOS:
- Soporte para discos grandes (GPT).  
- Entorno modular y extensible.  
- Drivers cargables en tiempo de arranque.  

Ejemplo: Apple usó EFI antes de la estandarización como UEFI.

---

## ESP (EFI System Partition)
La **partición del sistema EFI** (ESP) es obligatoria en discos con GPT para sistemas que usen UEFI.  

Características:
- Formato: FAT32.  
- Tamaño habitual: 100-550 MB.  
- Contiene bootloaders, drivers y ficheros `.efi`.  

Ejemplo de estructura de ESP:
```
/EFI
 ├── Microsoft/Boot/bootmgfw.efi
 ├── Boot/bootx64.efi
 └── grub/grubx64.efi
```

---

## Gestor de arranque
Un **gestor de arranque** permite seleccionar y cargar sistemas operativos.  

Ejemplos:
- **GRUB2**: usado en Linux.  
- **Windows Boot Manager**: carga Windows.  
- **rEFInd**: alternativo y multiplataforma.  

Ejemplo visual:  
```
UEFI → grubx64.efi → menú de GRUB → elegir Ubuntu → cargar kernel Linux
```

---

## GPT (GUID Partition Table)
Tabla de particiones moderna, usada con UEFI.  

Características:
- Identifica particiones con GUID (identificadores únicos).  
- Soporta discos de hasta 9.4 ZB.  
- Hasta 128 particiones en Windows (sin necesidad de particiones extendidas).  

Ejemplo visual de disco GPT (3 particiones):
```
[ ESP | Partición Linux | Partición Datos ]
```

---

## MBR (Master Boot Record)
Tabla de particiones tradicional usada con BIOS.  

Características:
- Usa 32 bits → discos hasta 2 TB.  
- 4 particiones primarias.  
- Primer sector del disco (512 bytes) contiene: código de arranque + tabla de particiones.  

Ejemplo visual de disco MBR:
```
[ MBR | Partición 1 | Partición 2 | Partición 3 | Partición 4 ]
```

---

## Partición
Una **partición** es una división lógica de un disco físico.  
Permite tener distintos sistemas operativos o separar datos.  

Ejemplo:  
- Disco de 1 TB:  
  - 200 GB → Windows  
  - 200 GB → Linux  
  - 600 GB → Datos compartidos  

---

## Sistema de archivos
El **sistema de archivos** define cómo se organizan y almacenan los datos dentro de una partición.  

Ejemplos:  
- **FAT32:** usado en ESP por compatibilidad.  
- **NTFS:** Windows.  
- **ext4:** Linux.  

Diagrama simplificado de un archivo en un FS:  
```
[Tabla de inodos] → [Bloques de datos]
archivo.txt → apunta a → bloque #123, bloque #124...
```

---

## Unidad
El término **unidad** puede referirse a:

1. Un dispositivo físico de almacenamiento (ej. disco duro, SSD, pendrive).  
2. Una partición lógica identificada por el sistema operativo (ej. C:, /dev/sda1).  

Ejemplo en Linux:
```
Dispositivo físico: /dev/sda
Particiones: /dev/sda1, /dev/sda2
```

Ejemplo en Windows:
```
Disco físico 0
  C: → Sistema
  D: → Datos
```

---

## UEFI (Unified Extensible Firmware Interface)
Estandarización de EFI (2005 en adelante).  
Especificación que reemplaza BIOS con un entorno modular y moderno.  

Características:  
- Interfaz gráfica posible (mouse y drivers).  
- Soporte para GPT.  
- Entorno de prearranque con aplicaciones `.efi`.  

Ejemplo: instalar Linux en modo UEFI requiere crear una partición ESP.

---
