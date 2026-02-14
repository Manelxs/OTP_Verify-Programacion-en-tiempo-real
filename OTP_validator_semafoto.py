import random
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox
import threading

class SemaforoOTP:
    def __init__(self):
        self.otp = ""
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Verificación OTP")
        self.ventana.geometry("400x500")
        self.ventana.configure(bg='#2c3e50')
        
        self.crear_interfaz()
        self.generar_otp()
        
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.ventana, text="VERIFICACIÓN OTP", 
                         font=('Arial', 16, 'bold'), 
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=20)
        
        # Canvas para el semáforo
        self.canvas = tk.Canvas(self.ventana, width=120, height=280, 
                               bg='#34495e', highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Dibujar estructura del semáforo
        self.canvas.create_rectangle(20, 20, 100, 260, fill='black')
        
        # Luces del semáforo
        self.luz_roja = self.canvas.create_oval(30, 40, 90, 100, 
                                                fill='gray', outline='#555')
        self.luz_amarilla = self.canvas.create_oval(30, 110, 90, 170, 
                                                    fill='gray', outline='#555')
        self.luz_verde = self.canvas.create_oval(30, 180, 90, 240, 
                                                 fill='gray', outline='#555')
        
        # Estado actual
        self.estado_label = tk.Label(self.ventana, text="⚪ ESPERANDO", 
                                    font=('Arial', 12), 
                                    bg='#2c3e50', fg='white')
        self.estado_label.pack(pady=10)
        
        # Campo de email
        tk.Label(self.ventana, text="Correo electrónico:", 
                bg='#2c3e50', fg='white').pack()
        self.email_entry = tk.Entry(self.ventana, width=30, font=('Arial', 10))
        self.email_entry.pack(pady=5)
        
        # Botones
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
        
        # OTP generado (mostrado para pruebas)
        self.otp_label = tk.Label(self.ventana, text="", 
                                 bg='#2c3e50', fg='#f1c40f')
        self.otp_label.pack(pady=10)
        
    def cambiar_estado(self, estado):
        """Cambia el color del semáforo según el estado"""
        # Resetear colores
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
    
    def generar_otp(self):
        self.otp = ""
        for i in range(6):   
            self.otp += str(random.randint(0, 9))
        self.otp_label.config(text=f"OTP generado: {self.otp} (solo pruebas)")
    
    def enviar_otp(self):
        to_mail = self.email_entry.get()
        if not to_mail:
            messagebox.showerror("Error", "Ingresa un correo electrónico")
            return
        
        self.cambiar_estado("enviando")
        self.btn_enviar.config(state='disabled')
        self.ventana.update()
        
        # Enviar en segundo plano
        threading.Thread(target=self.enviar_correo, args=(to_mail,), daemon=True).start()
    
    def enviar_correo(self, to_mail):
        try:
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
            
            self.ventana.after(0, self.envio_exitoso)
        except Exception as e:
            self.ventana.after(0, self.envio_fallido, str(e))
    
    def envio_exitoso(self):
        messagebox.showinfo("Éxito", "OTP enviado correctamente")
        self.btn_verificar.config(state='normal')
        self.cambiar_estado("inicial")
    
    def envio_fallido(self, error):
        messagebox.showerror("Error", f"No se pudo enviar el OTP:\n{error}")
        self.btn_enviar.config(state='normal')
        self.cambiar_estado("inicial")
    
    def verificar_otp(self):
        input_otp = self.otp_entry.get()
        if input_otp == self.otp:
            self.cambiar_estado("verificado")
            messagebox.showinfo("Verificación", "✅ OTP Verificado correctamente")
        else:
            self.cambiar_estado("invalido")
            messagebox.showerror("Verificación", "❌ OTP Inválido")
    
    def iniciar(self):
        self.ventana.mainloop()

# Iniciar aplicación
if __name__ == "__main__":
    app = SemaforoOTP()

    app.iniciar()
