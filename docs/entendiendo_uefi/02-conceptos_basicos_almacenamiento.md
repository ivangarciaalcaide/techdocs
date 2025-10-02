# Entendiendo UEFI

---

## 2. Conceptos básicos de almacenamiento

### 2.1 Qué es una partición

Un disco duro puede dividirse en varias **particiones**. Es más, al menos debe tener una partición para que un sistema 
operativo pueda utilizarlo.

Una partición es una _sección del disco que se comporta como una [unidad](99-glosario.md#unidad) 
independiente_. Para que pueda almacenar archivos y directorios, debe contener un 
**[sistema de archivos](99-glosario.md#sistema-de-archivos)** [formateado](99-glosario.md#formato-formatear). 
Así, contendrá datos del usuario o un sistema operativo con todo lo necesario para que este pueda arrancar.

> **Nota:** Los discos siempre deben tener al menos una partición para poder ser utilizados por un sistema operativo.

**Ejemplo de partición:**

```text
Disco completo: /dev/sda
+---------------------------+
| Partición 1               |
| Sistema de archivos: ext4 |
+---------------------------+
| Partición 2               |
| Sistema de archivos: NTFS |
+---------------------------+
```

De esta forma, el sistema operativo puede gestionar cada partición de forma independiente y se comportará como si cada
una fuera un disco diferente.

**GNU/Linux** y **macOs**:

Lo típico es hacer referenica a las particiones como `/dev/sda1`, `/dev/sda2`, etc. donde `sda` es el disco y el 
número indica la partición. Para los discos NVMe, se usa `nvme0n1p1`, `nvme0n1p2`, etc.

**Windows**:

En Windows, las particiones se identifican con letras del alfabeto, `C:`, `D:`, etc.

### 2.2 Tabla de particiones

La **tabla de particiones** es la estructura que indica cómo está dividido un disco y qué información contiene cada
[partición](99-glosario.md#particion).

- Tipo de [sistema de ficheros](99-glosario.md#sistema-de-archivos) (FAT32, NTFS, ext4, etc.)
- Inicio y fin de la partición (sectores)
- Si es arrancable (es decir, desde qué partición el sistema debe iniciar)
- Información adicional según el esquema de particionamiento (MBR o GPT)

> **Nota**: La tabla de particiones normalmente se encuentra al principio del disco y permite al sistema operativo conocer
> la ubicación y características de cada partición.

---

### 2.3 Tipos de tablas de particiones: MBR, GPT

**MBR (Master Boot Record)**
Es el esquema de particiones más antiguo, que se utilizaba en [BIOS](99-glosario.md#bios) heredado del IBM PC original.
La tabla de particiones MBR (Registro de Arranque Maestro) es un esquema de particionamiento que se encuentra en el 
primer sector de un disco y que contiene el código para iniciar el sistema operativo y el mapa de las particiones del 
disco.

- El primer sector del disco (512 bytes) contiene:
    - El [bootloader](99-glosario.md#bootloader-cargador-de-arranque) (código de arranque)
    - Tabla de particiones (máx. 4 entradas)

Así, al encender el ordenador, la BIOS lee este sector para localizar el bootloader. Este bootloader usa la información
de la tabla de particiones para encontrar la partición activa y cargar el sistema operativo. El bootloader ha de ser
pequeño (menos de 446 bytes) para dejar espacio a la tabla de particiones (64 bytes).

Tiene algunas limitaciones importantes:

- Solo 4 particiones primarias (o 3 primarias + 1 extendida para hasta 7 en total)
- No puede gestionar discos > 2 TB
- Solo permite una partición arrancable

**Diagrama visual**:

```text
MBR (sector 0)
+----------------------------+
| Código de arranque         |
+----------------------------+
| Partición 1 (Primaria)     |
| Partición 2 (Primaria)     |
| Partición 3 (Primaria)     |
| Partición 4 (Primaria/Ext) |
+----------------------------+
```

**GPT (GUID Partition Table)**

Es el esquema de particiones moderno que reemplaza a MBR en sistemas con UEFI. Utiliza identificadores únicos (GUID) 
para cada partición. Utiliza el direccionamiento de por 
[Bloques de Dirección Lógica (LBA)](99-glosario.md#lba-logical-block-addressing) y reserva espacio al 
principio y al final del disco para la tabla de particiones y su copia de seguridad.

Permite, en la práctica, un número ilimitado de particiones (aunque Windows solo permite 128).

Permite gestionar discos de gran tamaño (hasta 9.4 ZB teóricos) y mejora la seguridad de la información de la tabla de
particiones mediante copias de seguridad y sumas de verificación (CRC32).

| LBA                          | Contenido                                                                  | Detalles principales                                                                                                                                                                                                                         |
|------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0                            | **Protector de MBR** (*Protective Master Boot Record*)                     | Ocupa el primer sector (512 bytes), evita que discos antiguos vean el disco como vacío, contiene una partición tipo 0xEE que cubre todo el disco. También evita que las herramientas MBR antiguas sobrescriban accidentalmente el disco GPT. |
| 1                            | **Cabecera Primaria de GPT**                                               | El punto de inicio real de GPT. Contiene firma "EFI PART", el GUID del disco, primer LBA de la tabla de particiones, primer LBA de la tabla de particiones secundaria, CRC32 de la tabla de particiones                                      |
| 2 - 33                       | **Tabla de Particiones primaria**                                          | Cada entrada ocupa 128 bytes aprox. e incluye: GUID de tipo de partición, GUID único de partición, LBA inicial/final, atributos y nombre de la partición (hasta 36 caracteres)                                                               |
| 34 ... LBA final-34          | **Particiones de Datos** (Particiones reales de ESP, Windows, Linux, etc.) | Espacio utilizable del disco donde se almacenan los sistemas operativos y los archivos. Cada partición apunta a un rango de LBAs con los datos del usuario.                                                                                  |
| LBA final-33 - LBA final - 2 | **Tabla de Particiones secundaria** (Backup)                               | Copia de la tabla de particiones para redundancia (copia de seguridad con mismo contenido que LBA 2 a LBA N)                                                                                                                                 |
| LBA final-1                  | **Cabecera Secundaria de GPT** (Backup)                                    | Copia del GPT Header primario, permite recuperación en caso de corrupción                                                                                                                                                                    |
| LBA final                    | No utilizado                                                               | El último sector físico del disco; no forma parte de la estructura GPT.                                                                                                                                                                                                                     |

> NOTA: Típicamente, la Tabla de Particiones Primaria comienza en el LBA 2 y, por defecto, se extiende hasta el LBA 33, 
> utilizando 32 sectores. Este tamaño estándar permite hasta 128 entradas de partición, ya que cada entrada requiere 
> 128 bytes y cada sector (LBA) es comúnmente de 512 bytes (32 sectores×512 bytes/sector=16.384 bytes total, 
> lo que equivale a 128 entradas×128 bytes/entrada).
>
> Aunque este rango es el más común y el utilizado por sistemas como Windows, la especificación GPT permite 
> flexibilidad. El número de entradas puede ser mayor o menor (ampliando o reduciendo el rango de LBAs),
> un valor que se define explícitamente en la Cabecera GPT Primaria (LBA 1).

Resumiendo las ventajas de GPT frente a MBR:

- Número de particiones primarias casi ilimitado (Windows: hasta 128)
- Soporta discos > 2 TB
- Información más segura (copias de cabecera + CRC32)
- Arranque más flexible

**Diagrama visual esquemático**

```text
GPT
+------------------------+
| Cabecera GPT           |
+------------------------+
| Partición 1 (GUID)     |
| Partición 2 (GUID)     |
| Partición 3 (GUID)     |
| [...]                  |
| Partición n (GUID)     |
+------------------------+
| Cabecera Backup GPT    |
+------------------------+
```

---

### 2.4 Comparación rápida: MBR vs GPT

| Característica      | MBR                                                          | GPT                        |
|---------------------|--------------------------------------------------------------|----------------------------|
| Compatibilidad      | BIOS legacy                                                  | UEFI                       |
| Particiones máximas | 4 primarias (o 3 + 1 extendida que da lugar a un total de 7) | Prácticamente ilimitadas   |
| Tamaño máximo disco | 2 TB                                                         | Muy superior (ZB teóricos) |
| Arranque            | Código de arranque MBR / BIOS (512 bytes)                    | Arranque directo EFI/GRUB  | 
| Seguridad           | Baja                                                         | Copia cabecera + CRC32     |                     


---

<span style="color: red; font-weight: bold;">
SIN REVISAR A PARTIR DE AQUÍ
</span>

---

---

### 2.5 Partición EFI (ESP)

La **ESP (EFI System Partition)** es una partición especial obligatoria en sistemas UEFI:

- Contiene los ficheros EFI necesarios para arrancar sistemas operativos
- Normalmente formateada en FAT32
- Tamaño habitual: 100–512 MB
- Propósito:
    - Permitir que el firmware UEFI cargue directamente los ficheros .efi
    - Servir como espacio común para gestores de arranque como GRUB2 o Windows Boot Manager

**Diagrama ejemplo ESP en disco GPT**:

```text
Disco /dev/sda (GPT)
+---------------------------+
| Partición 1: EFI System   |
| Formato: FAT32            |
| Tamaño: 512 MB            |
+---------------------------+
| Partición 2: Linux ext4   |
+---------------------------+
| Partición 3: Windows NTFS |
+---------------------------+
```

> **Nota**: Nunca se debe borrar ni formatear la ESP sin conocer las implicaciones, ya que los sistemas operativos no 
> arrancarán correctamente.

{%
    include-markdown "./.includes/footer.md"
%}
