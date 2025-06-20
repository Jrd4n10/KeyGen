# KeyGen  
Generador de contraseñas con cifrado integrado.  
Password generator with integrated encryption.

---

## Características / Features

- Genera contraseñas aleatorias de 16 caracteres (letras mayúsculas, minúsculas y números).
- Guarda las contraseñas con un nombre personalizado.
- Protege tus contraseñas con cifrado.
- Autenticación con usuario y contraseña para acceder al gestor.
- Lista con contraseñas guardadas, con opción para copiar o eliminar cada una.
- Elimina cuenta y datos de manera segura.
- Interfaz gráfica sencilla usando Tkinter.
- Ícono personalizado en la ventana.
<br>

- Generates random 16-character passwords (uppercase, lowercase letters, and numbers).  
- Saves passwords with a custom name.  
- Protects your passwords with encryption.  
- User and password authentication to access the manager.  
- List of saved passwords, with options to copy or delete each.  
- Securely deletes account and all data.  
- Simple graphical interface using Tkinter.  
- Custom icon in the window.  

---

## Requisitos / Requirements

- Python 3.7+  
- Módulos / Modules:  
  - `tkinter`  
  - `cryptography`  
  - `pyperclip`  

Puedes instalar los módulos con / You can install the modules with:

```bash
pip install cryptography pyperclip
```

---

## Nota Importante Sobre Seguridad y Respaldo de Archivos / Important Note About Security and File Backup

- Este programa protege tus contraseñas mediante cifrado, pero los archivos donde se guardan (password_data.json, languages.json y preferences.json) están en formato accesible en disco y pueden ser modificados o eliminados si alguien tiene acceso a tu computadora. 
- Por eso, si piensas usar esta herramienta para proteger información importante, te recomiendo mantener una copia de seguridad actualizada especialmente de password_data.json (que contiene tus contraseñas cifradas). Este archivo se actualiza cada vez que guardas o modificas una contraseña.
- El archivo languages.json generalmente no cambia, pero conviene tenerlo respaldado para evitar errores en la aplicación si llegara a perderse o modificarse. En cuanto a preferences.json, su contenido es menos crítico y puede ser recreado desde la interfaz si es necesario.  
- Ten en cuenta que, si alguien con acceso a tu equipo modifica o elimina estos archivos, podrías perder información o causar que el programa no funcione correctamente. Esta es una limitación de las aplicaciones locales que almacenan datos en archivos, y no un fallo específico de este proyecto.
<br>

- This program protects your passwords through encryption, but the files where they are stored (password_data.json, languages.json, and preferences.json) are in an accessible disk format and can be modified or deleted if someone has access to your computer. 
- Therefore, if you plan to use this tool to protect important information, I recommend keeping an up-to-date backup especially of password_data.json (which contains your encrypted passwords). This file updates every time you save or modify a password.
- The languages.json file generally does not change, but it is advisable to back it up to avoid application errors if it is lost or modified. As for preferences.json, its content is less critical and can be recreated from the interface if needed.
- Keep in mind that if someone with access to your device modifies or deletes these files, you could lose information or cause the program to malfunction. This is a limitation of local applications that store data in files, and not a specific flaw of this project.

---

## For those who speak English

Does anyone actually read all this? If you’ve read everything and found a translation mistake, I’m sorry. I'm a native Spanish speaker and I barely know the basics of English. The translation is here in case it helps someone, I hope it does. You can also learn Spanish if you want, it’s a very beautiful language :D
