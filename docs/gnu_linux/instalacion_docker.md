# Instalación de Docker en Ubuntu Server 24 LTS

Una de las aplicaciones más comunes que suele usarse en servidores es Docker, una plataforma de contenedores
que permite empaquetar aplicaciones y sus dependencias en un entorno aislado. A continuación, se detallan 
los pasos para instalar Docker en Ubuntu Server 24 LTS.

## Paso 1: Actualizar el sistema

Antes de instalar cualquier software, es recomendable actualizar el sistema para asegurarse de que 
todos los paquetes estén al día:

```bash
apt update && apt upgrade
apt autoremove
apt autoclean
```

## Paso 2: Instalar dependencias

Docker requiere algunas dependencias para manejar repositorios y certificados. Instálalas con el siguiente comando:

```bash
apt install ca-certificates curl gnupg lsb-release
```

## Paso 3: Agregar el repositorio de Docker

Para que Ubuntu confíe en los paquetes de Docker, es necesario agregar su clave GPG y el repositorio oficial:

```bash
install -m 0755 -d /etc/apt/keyrings
```

Y descargar la clave GPG de Docker:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
```

Luego, agrega el repositorio de Docker a la lista de fuentes de APT:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
```

## Paso 4: Instalar Docker Engine

Ahora que el repositorio está configurado, actualizamos la base de datos de paquetes e instalamos 
Docker junto con **Docker Compose**:

```bash
apt update
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Paso 5: Configuración post-instalación

Para usar Docker sin necesidad de permisos de superusuario, es recomendable agregar tu usuario al grupo `docker`:

```bash
groupadd docker
usermod -aG docker $USER
```

!!! note "Nota"
    Se debe cerrar sesión y volver a entrar (o reiniciar) para que los cambios surtan efecto. También se puede usar 
    `newgrp docker` para aplicar los cambios sin necesidad de cerrar sesión.

---
📅 Documento escrito el 03/03/2026 · Última revisión: v1.0