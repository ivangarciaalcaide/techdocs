---
title: "Ansible: Introducción"
---

# Ansible

---

## 3. Módulos y comandos ad-hoc

Como se vio en el apartado anterior, Ansible puede ejecutar órdenes puntuales directamente desde la línea de
comandos sin necesidad de escribir ningún archivo. Estas órdenes se denominan **comandos ad-hoc** y son útiles
para tareas rápidas de administración o para comprobar el estado de los nodos gestionados.

### 3.1 Módulos de Ansible

Un **módulo** es la unidad de trabajo de Ansible: un pequeño programa que sabe cómo realizar una tarea concreta
de forma controlada e idempotente. Existe un módulo para casi cualquier tarea habitual de administración de
sistemas: instalar paquetes, gestionar servicios, copiar archivos, crear usuarios, modificar configuraciones...

La comunidad mantiene miles de módulos organizados en
[Ansible Collections](https://docs.ansible.com/ansible/latest/collections/index.html){ target="_blank" }, que 
además incluyen otros componentes como plugins, roles y documentación. A lo largo de este manual se irán viendo 
los más habituales.

### 3.2 Formato del comando ad-hoc

La forma más básica de un comando ad-hoc es:

```bash
ansible <hosts> -m <módulo>
```

Muchos módulos aceptan argumentos que concretan qué debe hacer:

```bash
ansible <hosts> -m <módulo> -a "<argumentos>"
```

Cuando interesa limitar la ejecución a un subconjunto de los hosts seleccionados, se añade `--limit`:

```bash
ansible <hosts> -m <módulo> -a "<argumentos>" --limit <filtro>
```

`--limit` acepta IPs, nombres de host, o patrones con comodines (`192.168.12.*`), lo que resulta muy útil
para probar una tarea sobre una sola máquina antes de aplicarla a todo el inventario:

```bash title="Ejemplo"
# ansible servidores_web -m ping --limit 192.168.12.11
```

???+ note "El módulo por defecto"
    Si se omite `-m`, Ansible utiliza el módulo `command` por defecto, que ejecuta un comando en los nodos
    remotos sin pasar por un shell. Por eso `ansible all -a "ls -l /home"` funciona sin especificar módulo.
    El módulo `command` no interpreta redirecciones (`>`), tuberías (`|`) ni variables de entorno; para eso
    existe el módulo `shell`.

### 3.3 Módulos habituales

#### `ping`

Comprueba que Ansible puede conectarse y operar correctamente en los nodos gestionados.

```bash title="Ejemplo"
# ansible all -m ping
```

???+ note "ping ≠ ICMP"
    El módulo `ping` no usa ICMP. Establece una conexión SSH real y verifica que Python está disponible
    en el nodo remoto. Es una comprobación de que Ansible puede trabajar, no solo de que la máquina responde.

---

#### `command` y `shell`

Ejecutan comandos arbitrarios en los nodos remotos. La diferencia entre ambos:

- `command` ejecuta el comando directamente, sin pasar por un shell. No interpreta redirecciones (`>`),
  tuberías (`|`) ni variables de entorno.
- `shell` ejecuta el comando a través de `/bin/sh`, por lo que sí admite redirecciones, tuberías y variables.

```bash title="Ejemplos"
# ansible all -a "ls -l /home"
# ansible all -m shell -a "who"
```

Algunas tareas no tienen un módulo específico en Ansible, como consultar qué usuarios hay conectados en el
sistema en este momento. Para eso solo queda recurrir a `shell`.

???+ warning "Idempotencia"
    Ninguno de estos dos módulos es idempotente: Ansible ejecutará el comando siempre, sin comprobar si
    el resultado ya es el deseado. Úsalos para consultas puntuales o tareas que no modifiquen estado, y
    cuando no exista un módulo específico para la tarea.

---

#### `setup`

Recopila información detallada sobre un nodo gestionado: sistema operativo, memoria, interfaces de red,
variables de entorno, etc. La información recopilada recibe el nombre de **facts** y la usa en playbooks para tomar
decisiones. También es muy útil para inspeccionar un nodo manualmente:

```bash title="Ejemplo"
# ansible 192.168.12.XX -m setup
```

La salida es extensa; en playbooks se puede filtrar con el argumento `filter`.

---

#### `copy` y `fetch`

El módulo `copy` copia un archivo desde el nodo de control hacia los nodos gestionados:

```bash title="Ejemplo"
# ansible all -m copy -a "src=/root/prueba.txt dest=/root/"
```

| Argumento | Descripción |
|-----------|-------------|
| `src`     | Ruta del archivo en el nodo de control |
| `dest`    | Ruta de destino en el nodo gestionado |
| `mode`    | Permisos del archivo resultante (p.ej. `0644`) |
| `owner`   | Usuario propietario del archivo |

El módulo `fetch` hace el recorrido inverso: trae un archivo desde un nodo gestionado al nodo de control.

---

#### `file`

Gestiona la existencia y los atributos de archivos y directorios en los nodos remotos. Es el equivalente
idempotente de operaciones como `touch`, `mkdir` o `chmod`.

Las dos órdenes siguientes crean el mismo archivo, pero de forma muy diferente:

```bash title="Con módulo file (idempotente)"
# ansible all -m file -a "path=/tmp/test_file state=touch"
```

```bash title="Con módulo shell (no idempotente)"
# ansible all -m shell -a "touch /tmp/test_file"
```

El resultado inmediato es idéntico, pero si se ejecuta dos veces, `file` comprueba si el archivo ya existe
y no hace nada; `shell` ejecuta `touch` de nuevo sin comprobación alguna.

Los valores más habituales para `state`:

| Valor       | Efecto |
|-------------|--------|
| `touch`     | Crea el archivo si no existe |
| `absent`    | Elimina el archivo o directorio |
| `directory` | Crea el directorio si no existe |
| `file`      | Verifica que el archivo existe y ajusta sus atributos |

---

#### `apt`

Gestiona paquetes en sistemas Debian y derivados. Es idempotente: si el paquete ya está en el estado
deseado, Ansible no hace nada.

```bash title="Ejemplo"
# ansible all -m apt -a "name=hollywood state=present update_cache=yes"
```

| Valor de `state` | Efecto |
|------------------|--------|
| `present`        | Instala el paquete si no está instalado |
| `absent`         | Desinstala el paquete si está instalado |
| `latest`         | Instala o actualiza a la última versión disponible |

???+ tip "update_cache"
    El argumento `update_cache=yes` equivale a ejecutar `apt update` antes de instalar. Es recomendable
    incluirlo para asegurarse de que se instala la versión más reciente disponible en los repositorios.

???+ note "Nota"
    **latest** resulta útil en determinados escenarios, pero en despliegues reproducibles suele preferirse **present**, 
    indicando explícitamente la versión cuando sea necesario. Así, no se producen actualizaciones inesperadas que en
    producción pueden ser un dolor de cabeza.

---

#### `lineinfile`

Garantiza que una línea concreta existe (o no existe) en un archivo de texto. Es uno de los módulos que
mejor ilustran el valor de la idempotencia.

```bash title="Con lineinfile (idempotente)"
# ansible all -m lineinfile -a "path=/tmp/test_file line='Hola!'"
```

```bash title="Con shell (no idempotente)"
# ansible all -m shell -a "echo 'Hola!' >> /tmp/test_file"
```

Si se ejecuta varias veces, `shell` añadirá la línea cada vez, generando duplicados. `lineinfile`, en
cambio, comprueba si la línea ya está presente y solo actúa si hace falta.

---

#### `service`

Gestiona servicios del sistema: arrancarlos, pararlos, reiniciarlos o habilitarlos en el arranque.

```bash title="Ejemplo"
# ansible all -m service -a "name=cron state=restarted enabled=yes"
```

| Argumento | Descripción |
|-----------|-------------|
| `name`    | Nombre del servicio |
| `state`   | `started`, `stopped`, `restarted`, `reloaded` |
| `enabled` | `yes` / `no`: si debe arrancar automáticamente con el sistema |

???+ note "Nota sobre idempotencia"
     Los estados **restarted** y **reloaded** en realidad no son idempotentes: se realizan siempre. En cambio,
     **started** y **stopped** sí lo son.
     
     Conviene tenerlo en cuenta al diseñar playbooks que se ejecuten de forma recurrente.

     

### 3.4 Consultar la documentación de los módulos

Ansible incorpora documentación completa accesible desde la línea de comandos mediante `ansible-doc`.
Antes de recurrir a búsquedas en Internet, merece la pena consultarla: la documentación instalada
corresponde exactamente a la versión de Ansible que se está utilizando, evitando confusiones entre versiones.

Para obtener información de un módulo concreto:

```bash title="Documentación de un módulo"
# ansible-doc <módulo>
# ansible-doc copy
```

La salida incluye descripción, parámetros disponibles y ejemplos de uso. Al ser extensa, se muestra en un
paginador: ++space++ para avanzar, ++b++ para retroceder y ++q++ para salir.

Para listar todos los módulos disponibles, o filtrar por nombre:

```bash title="Buscar módulos"
# ansible-doc -l
# ansible-doc -l | grep <expresión>
```

???+ tip "Antes de buscar en Internet"
    `ansible-doc` debería ser siempre el primer recurso. La documentación instalada corresponde exactamente
    a la versión en uso, evitando diferencias entre versiones que pueden llevar a errores difíciles de
    depurar.

### 3.5 Resumen de módulos

| Módulo | Para qué sirve | Idempotente |
|--------|----------------|-------------|
| `ping` | Verificar que Ansible puede operar en el nodo | ✅ |
| `command` | Ejecutar comandos simples (sin shell) | ❌ |
| `shell` | Ejecutar comandos con redirecciones y tuberías | ❌ |
| `setup` | Recopilar información del nodo (*facts*) | ✅ |
| `copy` | Enviar archivos del nodo de control al nodo gestionado | ✅ |
| `fetch` | Traer archivos del nodo gestionado al nodo de control | ✅ |
| `file` | Gestionar archivos y directorios | ✅ |
| `apt` | Gestionar paquetes en Debian y derivados | ✅ |
| `lineinfile` | Garantizar el contenido de una línea en un archivo | ✅ |
| `service` | Gestionar servicios del sistema | ✅ |

En la siguiente sección veremos los **playbooks**, donde estas mismas tareas se organizan en archivos YAML
reutilizables, con control sobre el orden de ejecución, condiciones y lógica.

{%
    include-markdown "./.includes/footer.md"
%}