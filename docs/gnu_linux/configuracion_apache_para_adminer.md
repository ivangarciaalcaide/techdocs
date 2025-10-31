Configuración de Apache para Adminer
====================================

Adminer es una aplicación web para administrar el gestor de
base de datos **MySQL**. 

Tal y como dice su [web oficial](https://www.adminer.org/):

> *Replace phpMyAdmin with Adminer and you will get a tidier user interface, better support for* ***MySQL*** *features, 
> higher performance and more security.*

Es un único fichero **PHP** que se puede descargar desde su
[web oficial](https://www.adminer.org/#download): 

Versiones:

- `Completa`: Soporte para varios idiomas varios SSGGD.
- `MySQL`: Soporte sólo para MySQL y varios idiomas.
- `MySQL en inglés`: Soporte sólo para MySQL y en inglés.

Yo utilizo la versión **MySQL en inglés** que es la más ligera y funciona perfectamente. Se trata de un único fichero
**PHP** que descargo y pongo en el servidor web. Por ejemplo:

```bash
mkdir -p /var/www/adminer
wget  https://www.adminer.org/latest-mysql-en.php -O /var/www/adminer/index.php
chown -R www-data:www-data /var/www/adminer
```
Esta es la configuración que utilizo en **Apache2** para ponerlo en una **URL** terminada en `/adminer`:

📂 ***/etc/apache2/conf-available/adminer.conf***

```apacheconf
Alias /adminer /var/www/adminer/

<Directory "/var/www/adminer/">
    SSLRequireSSL
    Options FollowSymlinks
    AllowOverride None
    Require all granted
    AddDefaultCharset off
    
    # Restringir a un único fichero ('index.php')
    <FilesMatch "\.php$">
        Require all denied
    </FilesMatch>
    <Files "index.php">
        Require all granted
    </Files>
</Directory>
```

Para activarlo:

```bash
a2enconf adminer
systemctl reload apache2
```

---
📅 Documento escrito el 01/10/2025 · Última revisión: v1.0
