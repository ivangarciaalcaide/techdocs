---
title: "Seguridad en el Arranque (Secure Boot)"
---

# Entendiendo UEFI

---

## 4. Seguridad en el Arranque (Secure Boot)

El **Arranque Seguro** (**Secure Boot**) es una característica fundamental de la especificación 
[UEFI](99-glosario.md#firmware-uefi) diseñada para proteger
el proceso de arranque del sistema contra software malicioso de bajo nivel como _rootkits_ y _bootkits_.

En esencia, **Secure Boot** asegura que el **firmware UEFI** solo cargue y ejecute 
[cargadores de arranque](99-glosario.md#bootloader-cargador-de-arranque) (`.efi`) y 
**controladores de dispositivos** que estén firmados digitalmente y autorizados por una clave de confianza previamente 
aprobada.