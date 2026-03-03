# Personalización de Ubuntu Server 24 LTS desde cero

Tras instalar Ubuntu Server 24 LTS, hay algunas acciones que realizo para dejarlo a mi gusto. Aquí detallo las acciones 
que suelo llevar a cabo.

## Desinstalación de snap

Esto es lo primero que hago, ya que no uso snap y prefiero evitar tenerlo en el sistema.

#### Verificar los paquetes snap instalados:
```bash
snap list
```
#### Desinstalar todos los paquetes snap
```bash
snap remove <nombre_del_paquete>
```
!!! note "Nota"
     El último paquete que suelo desinstalar es `core` o `coreXX`, ya que otros paquetes pueden depender de él.
    
Quito todos los paquetes de aplicaciones y, si me interesa alguno, lo instalo después con `apt` o lo que sea.

#### Eliminar el servicio

Una vez eliminados los paquetes, desactivo y elimino el servicio snapd:

```bash
systemctl stop snapd.service
systemctl disable snapd.service
apt purge snapd
apt autoremove
```

#### Eliminar los archivos residuales

Aunque `apt purge` elimina los archivos binarios, deja algunos directorios y datos residuales. Los elimino 
manualmente:

```bash
rm -rf ~/snap
rm -rf /var/cache/snapd
rm -rf /var/lib/snapd
rm -rf /var/snap
```

#### Actualizar el sistema
Después de desinstalar snap, actualizo el sistema para asegurarme de que todo esté al día:

```bash
apt update
apt upgrade
apt autoremove
apt autoclean
```

## Instalar shell ZSH
**Bash** está muy bien, pero... **ZSH** está mejor :-)

```bash
apt install zsh
chsh -s $(which zsh)
```

La primera que se usa empezará a preguntar un montón de cosas para configurar ZSH. Yo suelo elegir las opciones por 
defecto y luego personalizarlo a mi gusto.

Después, instalo **Oh My Zsh** para gestionar la configuración de ZSH de forma más sencilla:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Luego, instalo algunos plugins y temas para ZSH. Para ello se edita el fichero `~/.zshrc`:

```text
ZSH_THEME="clean"
[...]
source $HOME/.bash_aliases
plugins=(z zsh-autosuggestions)
<EOF>
```

Después, se descargan los plugins:

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

Me gusta que salga el nombre de la máquina en el prompt porque si no me lío cuando tengo varios terminales contra 
distintos servidores. Así, edito el prompt en el fichero del tema correspondiente, en este caso 
`~/.oh-my-zsh/themes/clean.zsh-theme`:

```text
[...]
PROMPT='%{$fg[$NCOLOR]%}%B%m@%n%b%{$reset_color%}:%{$fg[blue]%}%B%c/%b%{$reset_color%} $(git_prompt_info)%(!.#.$) '
[...]
```
Por otro lado, está bien incrementar la capacidad del historial. Editamos `~/.bashrc`:
```text
[...]
HISTSIZE=10000
HISTFILESIZE=20000
[...]
```

## Personalizar VIM

Lo primero es asegurarse de que la versión _improved_ de **vi** está instalada:

```bash
apt install vim
```

Se instala **vim-plug** para gestionar los plugins de VIM:

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

!!! note "Nota"
    Cada usuario debe instalar **vim-plug** en su directorio personal antes de usar por primera vez que use **VIM**.

!!! note "Nota"
    Más información sobre cómo instalar plugins de **Vim** en: 
    [Victorhck](https://victorhckinthefreeworld.com/2020/02/19/como-instalar-plugins-de-vim)

Para que la personalización se aplique a todos los usuarios, edito el fichero `/etc/vim/vimrc` y añado lo siguiente 
al final:

```text
[...]
systax on
colorscheme desert
[...]
" INDENTATION
filetype plugin indent on
set autoindent
set expandtab
set tabstop=4
set shiftwidth=4
set softtabstop=4
set smarttab
" INTERFACE
set relativenumber
set ruler
set hlsearch
let g:airline_powerline_fonts = 1 
let g:airline_section_z = "%p%% : \ue0a1:%l/%L: Col:%c"
set t_Co=256
" MISC
set history=5000
" UNDO with undotree plugin configurtion
if has("persistent_undo")
   let target_path = expand('~/.vim/undodir')
    " create the directory and any parent directories
    " if the location does not exist.
    if !isdirectory(target_path)
        call mkdir(target_path, "p", 0700)
    endif
    let &undodir=target_path
    set undofile
endif
nnoremap <F5> :UndotreeToggle<CR>
let g:undotree_WindowLayout = 2
let g:undotree_SplitWidth = 40
let g:undotree_SetFocusWhenToggle = 1
call plug#begin()
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'mbbill/undotree'
call plug#end()
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab
```

Luego, abro **VIM** y ejecuto el comando `:PlugInstall` para instalar los plugins. Esto hace que se descarguen e instalen
los plugins especificados en `~/.vim`.

!!! note "Nota"
    Cada usuario debe ejecutar `:PlugInstall` la primera vez que use **VIM** para instalar los plugins en su
    directorio personal.

## Instalación de herramientas varias

Aparte de todo, está bien tener algunas herramientas básicas:

- **htop** para ver procesos y uso de CPU/memoria.
- **ncdu** para explorar discos y ver qué ocupa espacio.

```bash
apt install htop ncdu
```

## Configuración de SSH
Si voy a acceder remotamente al servidor, configuro SSH para poner las claves públicas de los usuarios autorizados:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
vi ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

!!! note "Nota"
    La clave pública mía y que se encuentra en el usuario `ivangarciaalcaide` en [GitHub](https://github.com) es:
    ```text
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCncDvx2IDHxk19PA/B7cTwf0/aPRkRZnoyi3ps1lBzIK+Z5J2Hikbw5YlTxr6r70n/fcdzElMY4i63aex2A2QCe7QbhWVmxJ8ptfiP4B+hhonAMnPub/iS7/ZDd5s/iGMRce0X1WBNfII++qCr9Yi0qHbNb1LAF0Vq3EXTVtRCvajnA2bGyy/Sy9YdvUr514wAR2lP6iNzINrqSGU1T8UUZSfgto1h7Akw4hKXr0ZMH2+vXAQHIoo1fnN9+Z/z2PJe5pwpQQz1RJin6LEo/egkV2oCQKtRJ0ZONbJKg0GR8iu66h+IDi+0PHZBJ05IUZrPM20PzaTOpzk9K/DG03nF ivangarciaalcaide@github/122454195 # ssh-import-id gh:ivangarciaalcaide
    ```

---
📅 Documento escrito el 31/10/2025 · Última revisión: v1.0