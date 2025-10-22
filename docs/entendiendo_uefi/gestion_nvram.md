---
title: "Entendiendo UEFI: Gestión del registro de arranque UEFI (NVRAM)"
---

# Entendiendo UEFI

---

## 3. Gestión del registro de arranque UEFI (NVRAM)

Como hemos visto anteriormente, la [**NVRAM**](99-glosario.md#nvram-non-volatile-random-access-memory) es una memoria,
normalmente integrada en la placa base y de naturaleza no volátil, que almacena las **entradas de arranque** (_boot
entries_).

Cuando se instala un sistema operativo, este crea una entrada en la NVRAM que le indica al 
[**firmware UEFI**](99-glosario.md#firmware-uefi) lo siguiente:

- **Ruta** del [**cargador de arranque**](99-glosario.md#bootloader-cargador-de-arranque) (`.efi` dentro de la 
[**ESP**](99-glosario.md#esp-efi-system-partition)).
- **Nombre de la entrada** que aparecerá en el menú de arranque.

La **gestión de la NVRAM** se centra en manipular esa lista de entradas para poder _añadir_, _eliminar_ y _reordenar_ estos
registros permitiendo al usuario controlar el arranque de sus sistemas sin necesidad de reinstalarlos.

Este capítulo se enfoca en el uso de las herramientas más comunes para este fin, tanto dentro del mundo Windows como del
mundo GNU/Linux.

<div style="text-align: center">

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '14px', 'fontFamily': 'Inter'}}}%%
flowchart TD
    %% Nodos verticales con información interna
    NVRAM["
        <b>NVRAM</b> (Boot Entries)<hr><div style='text-align: left; padding-left: 10px; line-height: 1.8' >Boot0001: Windows
        Boot0002: GNU/Linux</div>
    "]
    
    ESP["""<div style='width:240px; text-align:center; line-height:1.2; margin:0; padding:2px;'><b>ESP (EFI System Partition)</b>
<hr style='margin: 4px'><div style='text-align: left; padding-left: 10px; padding-top: 5px; line-height: 1.8'>/EFI/BOOT/BOOTX64.EFI
/EFI/Microsoft/Boot/bootmgfw.efi
/EFI/ubuntu/grubx64.efi
</div>
</div>"""]

    BOOT["<b>Bootloaders</b> (.efi files)<hr><div style='text-align: left; padding-left: 10px; line-height: 1.8' >Windows Boot Manager
    GRUB2
    Shim</div>"]
    
    FALLBACK["<b>Fallback</b> (.efi file)<hr><div style='text-align: left; padding-left: 10px; line-height: 1.8' >\EFI\BOOT\bootx64.efi
    </div>"]
    
    OS["<b>Sistema Operativo</b><hr><div style='text-align: left; padding-left: 10px; line-height: 1.8' >Windows 
     Linux</div>"]
    
    %% Conexiones con etiquetas
    NVRAM -->|Apunta a| ESP
    ESP -->|Contiene| BOOT
    BOOT -->|Inicia| OS
    ESP -->|Si no hay entradas válidas| FALLBACK
    FALLBACK -->|Arranca| OS

    %% Estilo minimalista y monocromo
    classDef default fill:#eeeeee,stroke:#333,stroke-width:1px; font-size: 10px

```
</div>

{%
    include-markdown "./.includes/footer.md"
%}
