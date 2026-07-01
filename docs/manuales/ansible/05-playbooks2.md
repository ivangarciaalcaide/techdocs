---
title: "Ansible: Introducción"
---

# Ansible

---

## 5. Escribir y ejecutar playbooks

### 5.1 Estructura de un playbook

Un playbook es un archivo YAML que contiene uno o varios **plays**. Cada play tiene al menos tres elementos
obligatorios: sobre qué hosts actuar, con qué permisos, y qué tareas ejecutar. 

Todo playbook es, en esencia, un archivo YAML. Lo que convierte un archivo YAML en un playbook es el uso de las 
palabras clave propias de Ansible (hosts, tasks, become, vars, etc.) y de los módulos que ejecutarán las tareas.

El esquema general es el siguiente:

```yaml
---
- name: <descripción del play>
  hosts: <hosts o grupo del inventario>
  become: <true | false>

  tasks:
    - name: <descripción de la tarea>
      <módulo>:
        <argumento>: <valor>
        <argumento>: <valor>

    - name: <descripción de la tarea>
      <módulo>:
        <argumento>: <valor>
```
En realidad, un playbook no es más que una lista de plays. Por eso el documento comienza con un guion (`-`), 
indicando el primer elemento de esa lista.

Las palabras clave principales de un play son:

| Palabra clave | Descripción |
|---------------|-------------|
| `name` | Descripción del play o la tarea. Aparece en la salida al ejecutar el playbook. |
| `hosts` | A qué hosts o grupos del inventario se aplica este play. |
| `become` | Si es `true`, Ansible ejecutará las tareas con privilegios elevados. |
| `tasks` | Lista de tareas que se ejecutarán en orden sobre los hosts indicados. |

Cada tarea tiene también su propio `name`, que ayuda a entender qué está haciendo Ansible en cada momento
durante la ejecución, y a localizar errores cuando algo falla.

???+ note "El orden importa"
    Las tareas de un play se ejecutan **en el orden en que están escritas**, una tras otra, y sobre todos
    los hosts del play antes de pasar a la siguiente. Si una tarea falla en un host, Ansible detiene la
    ejecución en ese host pero continúa con los demás.

### 5.2 Un primer playbook

El siguiente playbook realiza la actualización del sistema en todos los hosts del inventario, algo que ya
vimos con un comando ad-hoc en la sección anterior. Comparando ambas formas se aprecia bien la diferencia
de estructura:

```bash title="Ad-hoc equivalente"
# ansible all -m apt -a "upgrade=yes update_cache=yes cache_valid_time=600"
```

```yaml title="actualizar_sistema.yml"
---
- name: Actualizar el sistema
  hosts: all
  become: true

  tasks:
    - name: Actualizar la caché y los paquetes instalados
      apt:
        upgrade: yes
        update_cache: yes
        cache_valid_time: 600
```

Los argumentos del módulo `apt` son exactamente los mismos en ambos casos; la diferencia es que en el
playbook cada argumento ocupa su propia línea como clave-valor YAML, lo que resulta mucho más legible
cuando el número de argumentos crece.

El argumento `cache_valid_time` merece una explicación: indica a Ansible que solo actualice la caché de
`apt` si han pasado más de 600 segundos (10 minutos) desde la última actualización. Si la caché es
suficientemente reciente, no se vuelve a descargar.

Un segundo ejemplo, también relacionado con los ad-hoc vistos antes, que instala un paquete y asegura
que su servicio está arrancado y habilitado en el arranque:

```yaml title="instalar_apache2.yml"
---
- name: Instalar y arrancar Apache2
  hosts: servidores_web
  become: true

  tasks:
    - name: Instalar Apache2
      apt:
        name: apache2
        state: present
        update_cache: yes

    - name: Asegurarse de que Apache está arrancado y habilitado
      service:
        name: apache2
        state: started
        enabled: yes
```

Este playbook ilustra bien cómo varias tareas de un mismo play se encadenan de forma natural y legible.
Nótese que está dirigido solo al grupo `servidores_web`, no a `all`.

Puede comprobarse la sintaxis del playbook con:

```bash
# ansible-playbook --syntax-check instalar_apache2.yml
```

???+ tip "Nombres descriptivos"
    Vale la pena dedicar un momento a escribir buenos `name` en plays y tareas. Durante la ejecución,
    Ansible los muestra en tiempo real; unos nombres claros permiten saber de un vistazo qué está
    ocurriendo y localizar rápidamente cualquier error.

### 5.3 Ejecutar un playbook

Los playbooks se ejecutan con el comando `ansible-playbook`:

```bash
ansible-playbook <playbook.yml> [opciones]
```

Por ejemplo:

```bash title="Ejemplo"
# ansible-playbook instalar_apache2.yml
```

#### Niveles de detalle: `-v`

Por defecto, Ansible muestra un resumen de qué ha cambiado y qué no en cada host. Con la opción `-v` se
puede aumentar el nivel de detalle de la salida:

| Opción | Nivel de detalle |
|--------|-----------------|
| `-v` | Muestra el resultado de cada tarea |
| `-vv` | Añade información sobre los archivos y conexiones |
| `-vvv` | Añade detalles de la conexión SSH |
| `-vvvv` | Nivel máximo, incluye información de bajo nivel para depuración |

En el día a día, `-v` suele ser suficiente para entender qué ha hecho Ansible. Los niveles más altos son
útiles cuando algo falla y hay que depurar.

#### Modo de prueba: `--check`

La opción `--check` ejecuta el playbook en modo simulación: Ansible analiza qué cambios tendría que hacer
pero **no los aplica**. Es muy útil para revisar el efecto de un playbook antes de ejecutarlo de verdad:

```bash title="Ejemplo"
# ansible-playbook instalar_apache2.yml --check
```

???+ warning "Limitaciones de --check"
    No todos los módulos soportan `--check` de forma completa. Algunos módulos que dependen del resultado
    de tareas anteriores pueden producir resultados incorrectos en modo simulación, porque las tareas
    previas no se han ejecutado realmente. Úsalo como orientación, no como garantía absoluta.

#### Listar hosts

Si se quiere comprobar sobre qué hosts actuará un playbook antes de ejecutarlo, puede utilizarse:

```bash
# ansible-playbook play.yml --list-hosts
```

#### Limitar hosts: `--limit`

Al igual que con los comandos ad-hoc, `--limit` restringe la ejecución a un subconjunto de los hosts
que el playbook seleccionaría normalmente:

```bash
ansible-playbook <playbook.yml> --limit <filtro>
```

El filtro admite varias formas:

| Filtro | Efecto |
|--------|--------|
| `192.168.12.11` | Solo ese host |
| `servidores_web` | Solo ese grupo |
| `192.168.12.*` | Todos los hosts que coincidan con el patrón |
| `servidores_web:bases_de_datos` | Ambos grupos |
| `!192.168.12.11` | Todos los hosts del play excepto ese |
| `servidores_web:!192.168.12.11` | El grupo entero excepto ese host |

El operador `!` es especialmente útil cuando se quiere excluir un host concreto de una ejecución, por
ejemplo porque está en mantenimiento o porque se quiere aplicar un cambio de forma progresiva:

```bash title="Ejemplos"
# ansible-playbook instalar_apache2.yml --limit 192.168.12.11
# ansible-playbook instalar_apache2.yml --limit 'servidores_web:!192.168.12.12'
```

???+ note "Comillas con ! en bash"
    El carácter `!` tiene un significado especial en bash (historial de comandos). Al usarlo en `--limit`
    conviene entrecomillar el argumento con comillas simples para evitar comportamientos inesperados.

#### El resumen final

Al terminar la ejecución, Ansible muestra siempre un resumen por host con el resultado de las tareas:

```
PLAY RECAP *********************************************************************
192.168.12.11 : ok=2  changed=1  unreachable=0  failed=0  skipped=0
192.168.12.12 : ok=2  changed=0  unreachable=0  failed=0  skipped=0
```

| Campo | Significado |
|-------|-------------|
| `ok` | Tareas ejecutadas correctamente (incluye las que no cambiaron nada) |
| `changed` | Tareas que sí realizaron algún cambio en el sistema |
| `unreachable` | Hosts a los que Ansible no pudo conectarse |
| `failed` | Tareas que terminaron con error |
| `skipped` | Tareas que se saltaron por alguna condición |

Un `changed=0` en todos los hosts significa que el sistema ya estaba exactamente en el estado deseado:
la idempotencia en acción.

Si un host aparece como `failed` o `unreachable`, el resto de hosts continúan ejecutando el playbook 
de forma independiente.

{%
    include-markdown "./.includes/footer.md"
%}