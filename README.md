# OTP Verification System 🔐

Este proyecto implementa un sistema básico de **verificación mediante OTP (One-Time Password)** usando Python y el servicio de correo de Gmail. El programa genera un código aleatorio de 6 dígitos y lo envía al correo electrónico del usuario. Luego, solicita al usuario que ingrese el OTP recibido para validar su identidad.

---

## 🚀 Funcionalidades
- Generación de un **OTP aleatorio de 6 dígitos**.
- Envío del OTP al correo electrónico del usuario mediante **SMTP de Gmail**.
- Solicitud de ingreso del OTP recibido.
- Verificación de coincidencia entre el OTP generado y el ingresado.
- Mensajes de confirmación:
  - ✅ `OTP Verified` si el código es correcto.
  - ❌ `Invalid OTP` si el código no coincide.

---

## ⚙️ Requisitos
- Python 3.x  
- Librerías estándar:
  - `random`
  - `smtplib`
  - `email.message`  

- Una cuenta de Gmail con **contraseña de aplicación** habilitada (no funciona con la contraseña normal).

---

## 📥 Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/otp-verification.git
