---
title: "Ansible: Introducción"
---

# Ansible

---
## 1. Introducción

### 1.1 Conceptos y requisitos para este manual

Para poder utilizar **Ansible**, como cualquier otra aplicación o servicio, debe ser instalado y configurado 
convenientemente en alguna máquina. Para ello se necesitan una serie de requisitos previos y tomar algunas
decisiones. Se ha procurado simplificar al máximo el entorno de trabajo para poder centrarse en Ansible sin 
renunciar a utilizar una arquitectura similar a la que puede encontrarse en un entorno real..

Por esta razón, se debe estar familiarizado con los siguientes conceptos y herramientas que, igualmente, se irán
viendo y explicando en este manual:

- Conocimiento básico de **GNU/Linux** (usaremos Debian o derivados)
- **YAML**
- **Máquinas virtuales** y **Contenedores**
- Autenticación con **clave pública y privada**
- **SSH** / **WinRM**

### 1.2 Introducción a DevOps e IaC

**DevOps** es una cultura y un conjunto de prácticas que busca unir el trabajo de desarrollo (*Dev*) y operaciones
(*Ops*), tradicionalmente separados, con el objetivo de entregar software de forma más rápida, frecuente y fiable.
Una de las piezas centrales de DevOps es la integración y entrega continuas (**CI/CD**, *Continuous
Integration / Continuous Delivery*): cada cambio de código se integra, se prueba y se despliega de forma automatizada,
reduciendo el tiempo entre que algo se desarrolla y llega a producción. Para que esto sea posible, no basta con
automatizar el código de la aplicación; también es necesario automatizar la infraestructura sobre la que se ejecuta.

Ahí es donde entra **Infrastructure as Code (IaC)**: en lugar de crear y configurar servidores manualmente, la
infraestructura se describe mediante archivos de texto (código), que se versionan en un repositorio igual que el
resto del software. Esto encaja de forma natural en DevOps, ya que permite que la infraestructura forme parte del
mismo flujo de CI/CD: un cambio en la infraestructura puede revisarse, probarse y desplegarse automáticamente,
igual que un cambio en la aplicación. Además, aporta _trazabilidad_ (se sabe quién cambió qué y cuándo),
_repetibilidad_ (el mismo código produce siempre el mismo resultado) y la posibilidad de _recrear entornos completos_
desde cero en caso de fallo.

Dentro de **IaC** conviene distinguir dos tipos de herramientas según lo que automatizan:

- **Aprovisionamiento (*provisioning*)**: se encargan de crear y destruir los recursos de infraestructura en sí
  (máquinas virtuales, redes, discos, balanceadores...). Ejemplos típicos son **Terraform**, que define en archivos
  declarativos qué recursos deben existir en un proveedor cloud y se encarga de gestionarlos, o
  **AWS CloudFormation**, que hace algo similar pero de forma nativa a AWS.
- **Configuración (*configuration management*)**: una vez que el servidor existe, se encargan de instalar software,
  ajustar archivos de configuración, crear usuarios o levantar servicios. Aquí se sitúan herramientas como
  **Ansible**, **Chef** o **Puppet**.

???+ note "Nota"
    La frontera entre ambos tipos de herramientas no siempre es estricta (Ansible, por ejemplo, también puede
    aprovisionar recursos en la nube), pero la distinción ayuda a entender qué problema resuelve cada una: una cosa es
    que el servidor exista, y otra que esté configurado tal y como se necesita.

### 1.3 ¿Dónde encaja Ansible y en qué ayuda?

**Ansible** se sitúa precisamente en la categoría de **_configuración_**, aunque con algo más de flexibilidad que sus
alternativas. Frente a herramientas como **Chef** o **Puppet**, que tradicionalmente requieren instalar un agente 
en cada máquina gestionada y suelen depender de un servidor central, **Ansible** se conecta directamente por 
**SSH** (o **WinRM** en el caso de Windows) sin necesidad de instalar ningún agente, describe el estado deseado en 
archivos **YAML** en lugar de un lenguaje de programación propio, y es **idempotente**: ejecutar varias veces el
mismo **playbook** produce siempre el mismo estado final, realizando únicamente los cambios que todavía sean 
necesarios.

Estas características han convertido a **Ansible** en una de las herramientas de configuración más extendidas dentro
de flujos **DevOps**, especialmente entre _administradores de sistemas_ que buscan una curva de entrada suave: no exige
montar una infraestructura cliente-servidor para empezar a usarlo, ni aprender un lenguaje específico, lo que
permite automatizar tareas de configuración con relativamente poco esfuerzo inicial.

A lo largo de este manual veremos cómo instalar Ansible, cómo está organizado un proyecto típico (inventarios,
playbooks, roles) y cómo escribir tareas que automaticen la configuración de los servidores.

{%
    include-markdown "./.includes/footer.md"
%}