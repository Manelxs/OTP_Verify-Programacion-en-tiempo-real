import random
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
import threading
from supabase import create_client, Client 

# --- CONFIGURACIÓN DE SUPABASE ---
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_KEY = "tu-anon-key-aqui"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SemaforoOTP:
    def __init__(self):
        self.otp = ""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Verificación OTP + Supabase")
        self.ventana.geometry("400x550")
        self.ventana.configure(bg='#2c3e50')
        
        self.crear_interfaz()
        self.generar_otp()
        
    def crear_interfaz(self):
        titulo = tk.Label(self.ventana, text="VERIFICACIÓN OTP", 
                         font=('Arial', 16, 'bold'), 
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=20)
        
        self.canvas = tk.Canvas(self.ventana, width=120, height=280, 
                               bg='#34495e', highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.create_rectangle(20, 20, 100, 260, fill='black')
        
        self.luz_roja = self.canvas.create_oval(30, 40, 90, 100, fill='gray', outline='#555')
        self.luz_amarilla = self.canvas.create_oval(30, 110, 90, 170, fill='gray', outline='#555')
        self.luz_verde = self.canvas.create_oval(30, 180, 90, 240, fill='gray', outline='#555')
        
        self.estado_label = tk.Label(self.ventana, text="⚪ ESPERANDO", 
                                    font=('Arial', 12), 
                                    bg='#2c3e50', fg='white')
        self.estado_label.pack(pady=10)
        
        tk.Label(self.ventana, text="Correo electrónico:", 
                bg='#2c3e50', fg='white').pack()
        self.email_entry = tk.Entry(self.ventana, width=30, font=('Arial', 10))
        self.email_entry.pack(pady=5)
        
        self.btn_enviar = tk.Button(self.ventana, text="📤 ENVIAR OTP", 
                                   command=self.enviar_otp,
                                   bg='#3498db', fg='white', 
                                   font=('Arial', 11, 'bold'))
        self.btn_enviar.pack(pady=10)
        
        self.otp_entry = tk.Entry(self.ventana, width=20, font=('Arial', 14))
        self.otp_entry.pack(pady=10)
        
        self.btn_verificar = tk.Button(self.ventana, text="✅ VERIFICAR", 
                                      command=self.verificar_otp,
                                      bg='#27ae60', fg='white', 
                                      font=('Arial', 11, 'bold'))
        self.btn_verificar.pack(pady=10)
        self.btn_verificar.config(state='disabled')
        
        self.otp_label = tk.Label(self.ventana, text="", 
                                 bg='#2c3e50', fg='#f1c40f')
        self.otp_label.pack(pady=10)

    def cambiar_estado(self, estado):
        self.canvas.itemconfig(self.luz_roja, fill='gray')
        self.canvas.itemconfig(self.luz_amarilla, fill='gray')
        self.canvas.itemconfig(self.luz_verde, fill='gray')
        
        if estado == "enviando":
            self.canvas.itemconfig(self.luz_amarilla, fill='yellow')
            self.estado_label.config(text="🟡 ENVIANDO...", fg='yellow')
        elif estado == "verificado":
            self.canvas.itemconfig(self.luz_verde, fill='green')
            self.estado_label.config(text="🟢 VERIFICADO ✓", fg='green')
        elif estado == "invalido":
            self.canvas.itemconfig(self.luz_roja, fill='red')
            self.estado_label.config(text="🔴 INVÁLIDO ✗", fg='red')
        else:
            self.estado_label.config(text="⚪ ESPERANDO", fg='white')

    def generar_otp_recursivo(self, longitud):
        if longitud == 0: return ""
        return str(random.randint(0,9)) + self.generar_otp_recursivo(longitud-1)

    def generar_otp(self):
        self.otp = self.generar_otp_recursivo(6)
        #self.otp_label.config(text=f"OTP generado: {self.otp} (solo pruebas)")

    def validar_otp_recursivo(self, otp, index=0):
        if index == len(otp): return True
        if not otp[index].isdigit(): return False
        return self.validar_otp_recursivo(otp, index + 1)

    def parpadear_rojo(self, veces):
        if veces == 0: return
        self.canvas.itemconfig(self.luz_roja, fill='red')
        self.ventana.after(300, lambda: self.canvas.itemconfig(self.luz_roja, fill='gray'))
        self.ventana.after(600, lambda: self.parpadear_rojo(veces-1))

    def enviar_otp(self):
        to_mail = self.email_entry.get()
        if not to_mail:
            messagebox.showerror("Error", "Ingresa un correo electrónico")
            return
        
        self.cambiar_estado("enviando")
        self.btn_enviar.config(state='disabled')
        self.ventana.update()
        
        threading.Thread(target=self.enviar_correo, args=(to_mail,), daemon=True).start()

    def enviar_correo(self, to_mail):
        try:
            # Primero generamos un nuevo OTP para esta sesión
            self.generar_otp()
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            from_email = 'Coloca tu correo @gmail.com'
            server.login(from_email, 'Coloca tu contraseña de aplicacion creada en myaccount.google.com/apppasswords')
            
            msg = EmailMessage()
            msg['Subject'] = "OTP Verification"
            msg['From'] = from_email
            msg['To'] = to_mail
            msg.set_content("Your OTP is: " + self.otp)
            
            server.send_message(msg)
            
            # --- REGISTRO EN SUPABASE (Punto clave de la rúbrica) ---
            datos_otp = {
                "email": to_mail,
                "otp_code": self.otp,
                "is_used": False
            }
            supabase.table("otps").insert(datos_otp).execute()
            # -------------------------------------------------------
            
            self.ventana.after(0, self.envio_exitoso)
            
        except Exception as e:
            self.ventana.after(0, self.envio_fallido, str(e))

    def envio_exitoso(self):
        messagebox.showinfo("Éxito", "OTP enviado y registrado en la nube")
        self.btn_verificar.config(state='normal')
        self.cambiar_estado("inicial")

    def envio_fallido(self, error):
        messagebox.showerror("Error", f"No se pudo completar el proceso:\n{error}")
        self.btn_enviar.config(state='normal')
        self.cambiar_estado("inicial")

    def verificar_otp(self):
        input_otp = self.otp_entry.get()
        email = self.email_entry.get()

        if not self.validar_otp_recursivo(input_otp):
            messagebox.showerror("Error", "El OTP solo debe contener números")
            return

        # --- VERIFICACIÓN CONTRA SUPABASE (Tiempo Real) ---
        try:
            res = supabase.table("otps").select("*").eq("email", email).eq("otp_code", input_otp).eq("is_used", False).execute()
            
            if res.data:
                # Marcar como usado en la BD
                supabase.table("otps").update({"is_used": True}).eq("id", res.data[0]['id']).execute()
                self.cambiar_estado("verificado")
                messagebox.showinfo("Verificación", "✅ OTP Validado en Supabase")
            else:
                self.cambiar_estado("invalido")
                self.parpadear_rojo(4)
                messagebox.showerror("Verificación", "❌ OTP Inválido o ya usado")
        except Exception as e:
            messagebox.showerror("Error de red", f"No se pudo conectar con la BD: {e}")

    def iniciar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = SemaforoOTP()
    app.iniciar()