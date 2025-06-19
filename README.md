# KeyGen
Generador de contraseñas con cifrado integrado.

---

## Características

- Genera contraseñas aleatorias de 16 caracteres (letras mayúsculas, minúsculas y números).
- Guarda las contraseñas con un nombre personalizado.
- Protege tus contraseñas con cifrado.
- Autenticación con usuario y contraseña para acceder al gestor.
- Lista con contraseñas guardadas, con opción para copiar o eliminar cada una.
- Elimina cuenta y datos de manera segura.
- Interfaz gráfica sencilla usando Tkinter.
- Ícono personalizado en la ventana (requiere archivo `key_icon.ico` en la carpeta `images`).

---

## Requisitos

- Python 3.7+
- Módulos:
  - `tkinter`
  - `cryptography`
  - `pyperclip`

Puedes instalar los módulos con:

```bash
pip install cryptography pyperclip
