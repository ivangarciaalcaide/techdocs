# Entendiendo UEFI

Este manual está orientado a entender UEFI de manera práctica para poder trabajar con ello. No pretende ser exhaustivo
en cuanto a teoría y especificaciones se refiere más allá de lo necesario para administrar los arranques de las
máquinas.

## Índice
- [01 - Introducción](01-introduccion.md)
- [02 - Conceptos básicos](02-conceptos_basicos.md)
- [Glosario](99-glosario.md)

---

<span style="color: red; font-weight: bolder; font-size: 2em">PROBANDO...</span>

---

# Estructura Sugerida para los Capítulos Prácticos

Esta estructura prioriza las tareas fundamentales de gestión de arranque antes de pasar a temas más avanzados como PXE.

---

## Capítulo 3: Gestión del Registro de Arranque UEFI (NVRAM)

Este capítulo se enfoca en las herramientas nativas para manipular las entradas de arranque, aplicando directamente el concepto de la NVRAM (ver Punto 2.7).

### 3.1. Herramientas de Gestión en Sistemas Modernos

#### 3.1.1. `bcdedit` (Windows)  
Introducción y sintaxis básica.

#### 3.1.2. `efibootmgr` (Linux)  
Introducción y sintaxis básica.

### 3.2. Operaciones Fundamentales en la NVRAM

#### 3.2.1. Visualizar las entradas de arranque existentes  
(BootOrder, entradas BootXXXX).

#### 3.2.2. Modificar el orden de arranque

#### 3.2.3. Crear una nueva entrada de arranque  
(Apuntando a un `.efi` específico en la ESP).

#### 3.2.4. Eliminar entradas obsoletas

---

## Capítulo 4: Administrando Gestores de Arranque y Bootloaders

Este capítulo se centra en los archivos `.efi` que residen en la ESP (ver Puntos 2.5 y 2.6).

### 4.1. Instalación y Configuración del Gestor de Arranque

#### 4.1.1. GRUB2 en UEFI  
Instalación básica con `grub-install` y actualización de configuración.

#### 4.1.2. Windows Boot Manager  
Resumen de la creación de la estructura de arranque con `bcdboot`.

### 4.2. Arranque Dual y Multiboot

#### 4.2.1. El rol de la ESP en el arranque múltiple

#### 4.2.2. Configuración de GRUB para detectar y lanzar el Gestor de Windows

### 4.3. Arranque de Reserva (Fallback Boot)  
Explicación del archivo `\EFI\BOOT\BOOTX64.EFI`.

---

## Capítulo 5: Integración de la Seguridad (Secure Boot)

Aquí se introduce el concepto de *shim*, ya que el lector ahora entiende qué es un gestor de arranque y cómo se registra.

### 5.1. Introducción al Arranque Seguro (Secure Boot)

#### 5.1.1. Propósito y Cadena de Confianza

#### 5.1.2. Gestión de claves  
KEK, DB, DBX.

### 5.2. El Componente Shim (Pre-cargador de Linux)

#### 5.2.1. Función de Shim en la cadena de confianza

#### 5.2.2. Registro y gestión de la clave del propietario de la máquina (MOK)

---

## Capítulo 6: Arranque Avanzado y Red (PXE)

Este es el lugar natural para el arranque por red, representando un método alternativo y avanzado al arranque local.

### 6.1. Conceptos Fundamentales del Arranque por Red (PXE)

#### 6.1.1. Definición de PXE y sus requisitos  
(DHCP y TFTP).

#### 6.1.2. El rol del firmware UEFI en el arranque PXE

### 6.2. Arrancando UEFI a través de PXE (UEFI PXE Boot)

#### 6.2.1. El archivo `.efi` y el servidor TFTP

#### 6.2.2. Diferencias clave con el arranque BIOS/PXE

#### 6.2.3. Opcional: Uso de un gestor de arranque en red (ej., iPXE)

---

Esta estructura permite avanzar de forma lógica:

1. **Fundamentos (Cap. 2):** Qué es y dónde está.  
2. **Gestión (Cap. 3):** Cómo manipular el registro de arranque.  
3. **Archivos (Cap. 4):** Cómo instalar y configurar el software de arranque real.  
4. **Seguridad (Cap. 5):** Cómo se integra la seguridad en el proceso.  
5. **Avanzado (Cap. 6):** Arranque por red.

<!--
Estructura Sugerida para los Capítulos Prácticos

Esta estructura prioriza las tareas fundamentales de gestión de arranque antes de pasar a temas más avanzados como PXE.

Capítulo 3: Gestión del Registro de Arranque UEFI (NVRAM)

Este capítulo se enfoca en las herramientas nativas para manipular las entradas de arranque, aplicando directamente el concepto de la NVRAM (Punto 2.7).

    3.1. Herramientas de Gestión en Sistemas Modernos

        3.1.1. bcdedit (Windows): Introducción y sintaxis básica.

        3.1.2. efibootmgr (Linux): Introducción y sintaxis básica.

    3.2. Operaciones Fundamentales en la NVRAM

        3.2.1. Visualizar las entradas de arranque existentes (BootOrder, entradas BootXXXX).

        3.2.2. Modificar el orden de arranque.

        3.2.3. Crear una nueva entrada de arranque (apuntando a un .efi específico en la ESP).

        3.2.4. Eliminar entradas obsoletas.

Capítulo 4: Administrando Gestores de Arranque y Bootloaders

Este capítulo se centra en los archivos .efi reales que residen en la ESP (Punto 2.5 y 2.6).

    4.1. Instalación y Configuración del Gestor de Arranque

        4.1.1. GRUB2 en UEFI: Instalación básica con grub-install y actualización de configuración.

        4.1.2. Windows Boot Manager: Resumen de la creación de la estructura de arranque con bcdboot.

    4.2. Arranque Dual y Multiboot

        4.2.1. El rol de la ESP en el arranque múltiple.

        4.2.2. Configuración de GRUB para detectar y lanzar el Gestor de Windows.

    4.3. El Arranque de Reserva (Fallback Boot): Explicación del archivo \EFI\BOOT\BOOTX64.EFI.

Capítulo 5: Integración de la Seguridad (Secure Boot)

Aquí introduces el concepto de shim que mencionamos, ya que el lector ahora entiende qué es un gestor de arranque y cómo se registra.

    5.1. Introducción al Arranque Seguro (Secure Boot)

        5.1.1. Propósito y Cadena de Confianza.

        5.1.2. Gestión de claves: KEK, DB, DBX.

    5.2. El Componente Shim (Pre-cargador de Linux)

        5.2.1. Función de Shim en la cadena de confianza.

        5.2.2. Registro y gestión de la clave del propietario de la máquina (MOK).

Capítulo 6: Arranque Avanzado y Red (PXE)

Este es el lugar natural para el arranque por red, ya que representa un método alternativo y avanzado al arranque local.

    6.1. Conceptos Fundamentales del Arranque por Red (PXE)

        6.1.1. Definición de PXE y sus requisitos (DHCP y TFTP).

        6.1.2. El rol del firmware UEFI en el arranque PXE.

    6.2. Arrancando UEFI a través de PXE (UEFI PXE Boot)

        6.2.1. El archivo .efi y el servidor TFTP.

        6.2.2. Diferencias clave con el arranque BIOS/PXE.

        6.2.3. Opcional: Uso de un gestor de arranque en red (ej., iPXE).

Esta estructura te permite avanzar lógicamente:

    Fundamentos (Cap. 2): Qué es y dónde está.

    Gestión (Cap. 3): Cómo manipular el registro de arranque.

    Archivos (Cap. 4): Cómo instalar y configurar el software de arranque real.

    Seguridad (Cap. 5): Cómo se integra la seguridad en el proceso.

    Avanzado (Cap. 6): El arranque por red.
-->