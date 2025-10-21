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

!!! Nota    
    Los discos siempre deben tener al menos una partición para poder ser utilizados por un sistema operativo.

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

**GNU/Linux** y **macOS**:

Lo típico es hacer referencia a las particiones como `/dev/sda1`, `/dev/sda2`, etc., donde `sda` es el disco y el 
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

!!! Nota
    La tabla de particiones normalmente se encuentra al principio del disco y permite al sistema operativo conocer
    la ubicación y características de cada partición.

---

### 2.3 Tipos de tablas de particiones: MBR, GPT

**MBR (Master Boot Record)**
Es el esquema de particiones más antiguo, que se utilizaba en [BIOS](99-glosario.md#bios) heredado del IBM PC original.
La tabla de particiones MBR (Registro de Arranque Maestro) es un esquema de particionamiento que se encuentra en el 
primer sector de un disco y que contiene el código para iniciar el sistema operativo y el mapa de las particiones del 
disco.

- El primer sector del disco (512 bytes) contiene:
    - El [bootloader](99-glosario.md#bootloader-cargador-de-arranque) (código de arranque)
    - Tabla de particiones (máx. 4 entradas de 16 bytes c/u)

Así, al encender el ordenador, la BIOS lee este sector para localizar el bootloader. Este bootloader usa la información
de la tabla de particiones para encontrar la partición activa y cargar el sistema operativo. El bootloader ha de ser
pequeño (menos de 446 bytes) para dejar espacio a la tabla de particiones (64 bytes).

Tiene algunas limitaciones importantes:

- Solo 4 particiones primarias (o 3 primarias + 1 extendida para hasta 7 en total, aunque puede depender del sistema operativo)
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
| LBA final-33 - LBA final - 2 | **Tabla de Particiones secundaria** (Backup)                               | Copia de la tabla de particiones para redundancia (copia de seguridad con mismo contenido que **LBA 2 a LBA 33**)                                                                                                                            |
| LBA final-1                  | **Cabecera Secundaria de GPT** (Backup)                                    | Copia del GPT Header primario, permite recuperación en caso de corrupción                                                                                                                                                                    |
| LBA final                    | No utilizado                                                               | El último sector físico del disco; no forma parte de la estructura GPT.                                                                                                                                                                      |

!!!Nota
    Típicamente, la Tabla de Particiones Primaria comienza en el LBA 2 y, por defecto, se extiende hasta el LBA 33, 
    utilizando 32 sectores. Este tamaño estándar permite hasta 128 entradas de partición, ya que cada entrada requiere 
    128 bytes y cada sector (LBA) es comúnmente de 512 bytes (32 sectores×512 bytes/sector=16.384 bytes total, 
    lo que equivale a 128 entradas×128 bytes/entrada).

    Aunque este rango es el más común y el utilizado por sistemas como Windows, la especificación GPT permite 
    flexibilidad. El número de entradas puede ser mayor o menor (ampliando o reduciendo el rango de LBAs),
    un valor que se define explícitamente en la Cabecera GPT Primaria (LBA 1).

Resumiendo las ventajas de GPT frente a MBR:

- Número de particiones primarias casi ilimitado (Windows: hasta 128)
- Soporta discos > 2 TB
- Información más segura (copias de cabecera + CRC32)
- Arranque más flexible

**Diagrama visual esquemático**

```text
GPT
+-------------------------+
| Cabecera primaria GPT   |
+-------------------------+
| Partición 1 (GUID)      |
| Partición 2 (GUID)      |
| Partición 3 (GUID)      |
| [...]                   |
| Partición n (GUID)      |
+-------------------------+
| Cabecera Secundaria GPT |
+-------------------------+
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

### 2.5 Partición EFI (ESP)

La **partición EFI**, también conocida como **ESP** (*EFI System Partition*), es una pequeña área del disco donde 
el firmware **UEFI** guarda los ficheros necesarios para iniciar el sistema operativo. Podemos imaginarla como una 
**zona común de arranque**: un espacio que el firmware entiende y desde el cual puede leer directamente los archivos 
ejecutables que inician los sistemas instalados.

En los sistemas modernos, la ESP es **imprescindible**: sin ella, el equipo no sabría desde dónde arrancar.

- **Tipo de partición:** `EFI System Partition`
- **Identificador GPT:** `GUID de tipo EFI Partition` (alias `EF00` - en MBR se usa el tipo `0xEF`-)
- **Sistema de archivos:** FAT32 (por compatibilidad universal con todos los firmwares UEFI)
- **Tamaño habitual:** entre **100 y 550 MB**
- **Etiqueta recomendada:** `ESP` o `EFI System Partition`
- **Punto de montaje habitual (Linux):** `/boot/efi`

El propósito de esta partición es servir de **punto de encuentro** entre el firmware UEFI y los sistemas operativos instalados.

El firmware UEFI puede **leer directamente** el sistema de archivos FAT32 de la ESP.  
Dentro de ella busca los ficheros **`.efi`**, que son pequeños programas ejecutables que el propio firmware puede lanzar sin necesidad de ningún otro sistema.

Estos ficheros pueden corresponder a:

- El **gestor de arranque** (por ejemplo, `grubx64.efi`, `bootmgfw.efi`, `refind.efi`…)
- Herramientas del fabricante (diagnóstico, actualización, etc.)
- Otros sistemas operativos instalados (si hay arranque dual o múltiple)

La **estructura de directorios** dentro de la ESP suele seguir un estándar definido por la especificación UEFI:

```text
/EFI
├── BOOT
│  └── BOOTX64.EFI ← Arranque genérico (fallback)
├── Microsoft
│  └── Boot
│    ├── bootmgfw.efi ← Gestor de arranque de Windows
│    └── BCD ← Base de datos de configuración del arranque
├── ubuntu
│  └── grubx64.efi ← Cargador de Linux (GRUB)
└── tools
└── shellx64.efi ← Consola UEFI opcional
```

!!! Nota
    La carpeta `EFI/BOOT` es especial. Si el firmware no encuentra otra entrada de arranque válida, intenta arrancar automáticamente desde `EFI/BOOT/BOOTX64.EFI` (en sistemas de 64 bits).

Así, un **diagrama típico** de las particiones de un disco preparado para arranque dual Windows y GNU/Linux podría ser: 

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

!!! Nota
    Nunca se debe borrar ni formatear la ESP sin conocer las implicaciones, ya que los sistemas operativos no
    arrancarán correctamente.

Y una **tabla de equivalencias** a modo de ilustración...

| Sistema       | Ruta del gestor EFI                | Herramienta de gestión        |
| ------------- | ---------------------------------- | ----------------------------- |
| Windows       | `\EFI\Microsoft\Boot\bootmgfw.efi` | `bcdboot`, `bcdedit`          |
| Ubuntu/Debian | `\EFI\ubuntu\grubx64.efi`          | `grub-install`, `efibootmgr`  |
| Fedora        | `\EFI\fedora\shimx64.efi`          | `grub2-install`, `efibootmgr` |

!!! Nota
    Las herramientas de gestión se detallan más adelante.

---

### 2.6 Definición de gestor de arranque (Bootloader)

Un **gestor de arranque** (bootloader) es un pequeño programa cuya única misiónes cargar un sistema operativo más grande
y complejo (Windows, macOS, GNU/Linux, ...) en la memoria principal del ordenador (_RAM_) y cederle el control.

En el contexto de **UEFI/GPT**, el gestor de arranque se materializa como un archivo ejecutable `.efi` que reside en la 
**Partición EFI** (ESP). El **firmware UEFI** (es decir, la implementación UEFI dispuesta en la placa base) lo lanza 
directamente, y el gestor de arranque se encarga de:

1. Leer archivos de **configuración y opciones de arranque**.
2. **Presentar el menú** de selección de sistema operativo (si procede).
3. **Cargar los archivos esenciales del kernel** en la memoria RAM antes de cederle el control.

Los dos ejemplos más comunes son **GRUB** (usado por la mayor parte de distribuciones de GNU/Linux) y el **Windows
Boot Manager** empleado por Microsoft para sus sistemas Windows.

!!! Nota
    A diferencia de **UEFI**, el sistema **BIOS** dependía del **Registro de Arranque Maestro** (MBR) que se ubicaba 
    en el primer sector del disco (_LBA 0_ usando el direccionamiento lógico de bloques). Este sector solo reservaba **446 
    bytes** para el código de arranque. Este espacio tan limitado solo podía contener un **cargador de primera fase**
    (first-stage bootloader), que se limitaba a localizar y pasar el control a un gestor de arranque más completo (de
    **segunda fase**), como pueda ser _GRUB_ o _Windows Boot Manager_, ubicado en otra parte del disco. **UEFI** elimina 
    esta limitación de tamaño, permitiendo que el **gestor de arranque completo** (el fichero `.efi`) se ejecute directamente
    en una sola fase.

---

### 2.7 Registro de arranque UEFI: **NVRAM**

Pero no basta con que la Partición EFI (ESP) contenga los archivos de arranque (`.efi`), 
el **firmware UEFI** necesita saber qué archivos cargar 
y en qué orden. Esta información se almacena en la **NVRAM** (_Non-Volatile Random-Access Memory_), que es una pequeña
memoria no volátil, típicamente ubicada en la placa base, que guarda la configuración de UEFI y las entradas del gestor de arranque (la ubicación de cada
fichero `.efi`).

Así, la **NVRAM** contiene registros que, básicamente, son pares de identificador/valor que contienen el **nombre de 
una entrada** y la **ubicación del fichero `.efi`** correspondiente. Así, el _firmware UEFI_ puede generar un menú de
arranque o dar a elegir al usuario, en cada caso, qué se va a iniciar.

**Ejemplo**:

| Nombre de entrada    |                                  |
|----------------------|----------------------------------|
| Windows Boot Manager | \EFI\Microsoft\Boot\bootmgfw.efi |
| Ubuntu               | \EFI\ubuntu\grubx64.efi          |

Se debe tener en cuenta que cuando un sistema operativo se instala o se repara, no solo se modifica el contenido de 
la **ESP**, sino que también se actualiza la NVRAM para registrar la nueva ruta de arranque. 
Herramientas como **efibootmgr** (en Linux) o **bcdedit** (en Windows) son las que se utilizan para manipular 
directamente estas entradas de la **NVRAM**.

{%
    include-markdown "./.includes/footer.md"
%}
