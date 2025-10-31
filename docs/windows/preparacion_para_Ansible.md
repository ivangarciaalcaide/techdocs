# Preparación de Windows 10/11 para Ansible

Para que **Ansible** pueda comunicarse con hosts Windows, es necesario habilitar **WinRM** (*Windows Remote 
Management*), una herramienta incluida en el sistema que permite la administración remota (especialmente 
la ejecución de comandos).

Por defecto, WinRM viene **deshabilitado**, por lo que debemos activarlo y configurarlo correctamente.

---

## Requitisos Previos

- Windows 10/11 con las últimas actualizaciones.
- **PowerShell 5.x** instalado (viene por defecto en Windows 10/11).
- **.NET Framework** actualizado (viene por defecto en Windows 10/11).
- Acceso de administrador local.

---

## Permisos de Ejecución de Scripts

Se va a necesitar ejecutar un script en **Powershell**, así que, hay que habilitar la ejecución de scripts:

```powershell
Set-ExecutionPolicy Unrestricted
```

!!! warning
    Esto puede suponer un riesgo de seguridad, ya que permite la ejecución de cualquier script.  
    Se recomienda volver a poner la política de ejecución a `Restricted` una vez se haya terminado la configuración:
   
    ```powershell
    Set-ExecutionPolicy Restricted
    ```

## Configuración de WinRM para Ansible

Ejecuta el siguiente script en una **consola de PowerShell como administrador**.  
Este script sigue la recomendación oficial de Ansible y habilita WinRM permitiendo conexiones no cifradas (solo en redes de confianza).

```powershell
$url = "https://raw.githubusercontent.com/AlbanAndrieu/ansible-windows/master/files/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"
Invoke-WebRequest -Uri $url -OutFile $file
# (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file
Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true
```

Se puede descargar de [aquí](http://barcena.etsisi.upm.es/sc.ps1).

## Configuración del Firewall de Windows
Abre los **puerto 5985** y **5986** en el firewall de Windows (reglas de entrada) y habilita ICMPv4 (ping).

```powershell
# Abrir puerto 5985 (HTTP - WinRM)
New-NetFirewallRule -Name "WINRM-HTTP" -DisplayName "WinRM (HTTP)" -Protocol TCP -LocalPort 5985 -Direction Inbound -Action Allow

# Abrir puerto 5986 (HTTPS - WinRM)
New-NetFirewallRule -Name "WINRM-HTTPS" -DisplayName "WinRM (HTTPS)" -Protocol TCP -LocalPort 5986 -Direction Inbound -Action Allow

# Permitir ICMPv4 (ping)
New-NetFirewallRule -Name "ICMPv4-In" -DisplayName "Permitir ICMPv4 Echo Request" -Protocol ICMPv4 -IcmpType 8 -Direction Inbound -Action Allow
```

## Solución de Problemas de perfil de Red

Si WinRM no se activa correctamente, puede deberse al tipo de perfil de red.
Windows no permite habilitar WinRM en redes públicas.

```powershell
Set-NetConnectionProfile -NetworkCategory "Private"
Enable-PSRemoting -Force -SkipNetworkProfileCheck
```

---

✅ Con esto, el sistema Windows quedará listo para recibir órdenes de Ansible mediante WinRM.

---
📅 Documento escrito el 31/10/2025 · Última revisión: v1.0

