# Entendiendo UEFI

---

## 2. Conceptos básicos de almacenamiento

---

### 2.1 Qué es una partición

Un disco duro puede dividirse en varias **particiones**. Es más, al menos debe tener una partición para que un sistema 
operativo pueda utilizarlo.

Una partición es una _sección del disco que se comporta como una [unidad](99-glosario.md#unidad) 
independiente_. Para que pueda almacenar archivos y directorios, debe contener un 
**[sistema de archivos](99-glosario.md#sistema-de-archivos)** [formateado](99-glosario.md#formato). 
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

Lo típico es hacer referenica a las particiones como `/dev/sda1`, `/dev/sda2`, etc. donde `sda` es el disco y el 
número indica la partición. Para los discos NVMe, se usa `nvme0n1p1`, `nvme0n1p2`, etc. Y en Windows, `C:`, `D:`, etc.

---

<span style="color: red; font-weight: bold;">
SIN REVISAR A PARTIR DE AQUÍ
</span>

---

### 2.2 Tabla de particiones

La **tabla de particiones** es la estructura que indica cómo está dividido un disco y qué información contiene cada
partición:

- Tipo de sistema de archivos
- Inicio y fin de la partición (sectores)
- Bandera de arranque
- Información adicional según el esquema de particionamiento (MBR o GPT)

> **Nota**: La tabla de particiones normalmente se encuentra al principio del disco y permite al sistema operativo conocer
> la ubicación y características de cada partición.

---

### 2.3 Tipos de tablas de particiones: MBR, GPT

**MBR (Master Boot Record)**

- Antiguo, compatible con BIOS.
- Primer sector del disco (512 bytes) contiene:
    - Código de arranque
    - Tabla de particiones (máx. 4 entradas)
- Limitaciones:
    - Solo 4 particiones primarias (o 3 primarias + 1 extendida para hasta 7)
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

- Moderno, compatible con UEFI.
- Cabecera principal + cabecera de backup al final del disco
- Cada partición tiene un identificador único (GUID)
- Ventajas:
    - Número de particiones primarias casi ilimitado (Windows: hasta 128)
    - Soporta discos > 2 TB
    - Información más segura (copias de cabecera + CRC32)
    - Arranque más flexible

**Diagrama visual**

```text
GPT
+------------------------+
| Cabecera GPT           |
+------------------------+
| Partición 1 (GUID)     |
| Partición 2 (GUID)     |
| Partición 3 (GUID)     |
| Partición n (GUID)     |
+------------------------+
| Cabecera Backup GPT    |
+------------------------+
```

---

### 2.4 Comparación rápida: MBR vs GPT

| Característica      | MBR                    | GPT                        |
|---------------------|------------------------|----------------------------|
| Compatibilidad      | BIOS legacy            | UEFI                       |
| Particiones máximas | 	4 primarias         | Prácticamente ilimitadas   |
| Tamaño máximo disco | 2 TB                   | Muy superior (ZB teóricos) |
| Arranque            | Código de arranque MBR | Arranque directo EFI/GRUB  | 
| Seguridad           | Baja                   | Copia cabecera + CRC32     |                     

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
    include-markdown "./footer.md"
%}
