import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
from PIL import Image
import io
import base64
import requests
import json
import time

# Função para carregar o arquivo Excel
def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        global df
        df = pd.read_excel(file_path)
        messagebox.showinfo("Informação", "Arquivo Excel carregado com sucesso!")
        update_status("Arquivo Excel carregado com sucesso!")

# Função para carregar uma imagem
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        global img_base64, img_filename
        img_base64 = resize_image(file_path)  # Redimensiona e codifica em base64
        img_filename = file_path.split("/")[-1]  # Captura o nome do arquivo
        messagebox.showinfo("Informação", "Imagem carregada e redimensionada com sucesso!")
        update_status(f"Imagem {img_filename} carregada.")

# Função para limpar a imagem carregada
def clear_image():
    global img_base64, img_filename
    img_base64 = None
    img_filename = None
    messagebox.showinfo("Informação", "Imagem removida.")
    update_status("Imagem removida.")

def resize_image(image_path, base_width=600, quality=70):
    try:
        img = Image.open(image_path)
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.LANCZOS)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=quality)
        img_byte_arr = img_byte_arr.getvalue()

        base64_size = len(base64.b64encode(img_byte_arr).decode('utf-8'))
        update_status(f"Tamanho da imagem em base64: {base64_size} bytes")

        return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao redimensionar a imagem: {e}")
        update_status(f"Erro ao redimensionar a imagem: {e}")
        return None

# Função para atualizar o status
def update_status(message):
    status_text.insert(tk.END, f"{message}\n")
    status_text.see(tk.END)

# Função para inserir placeholders no texto da mensagem
def insert_placeholder(placeholder):
    message_text.insert(tk.INSERT, f"{{{placeholder}}}")

# Função para enviar mensagens
def send_messages():
    if 'df' not in globals():
        messagebox.showerror("Erro", "Por favor, carregue um arquivo Excel antes de enviar.")
        return
    if not message_text.get("1.0", tk.END).strip():
        messagebox.showerror("Erro", "Por favor, digite a mensagem antes de enviar.")
        return
    if not client_id_entry.get().strip():
        messagebox.showerror("Erro", "Por favor, insira o ID de Cliente antes de enviar.")
        return

    client_id = client_id_entry.get().strip()
    message_template = message_text.get("1.0", tk.END).strip()
    try:
        interval = float(interval_entry.get()) / 1000  # Converter de milissegundos para segundos
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um intervalo de tempo válido.")
        return

    url = "https://[URL DO SERVIDOR]/websocket/send-bulk-messages-with-file"
    headers = {
        "api-key": "e3cbd314-f0ea-4160-bcb8-bfedd1db79ec",
        "Content-Type": "application/json"
    }

    total_messages = len(df)
    for index, row in df.iterrows():
        try:
            mensagem_personalizada = message_template.format(**row)
            data = {
                "clientId": client_id,
                "messages": mensagem_personalizada,
                "numeros": [str(row['numero'])],
                "intervalPerMessage": 5000,
                "intervalPerBatch": 10000,
            }

            if 'img_base64' in globals() and img_base64:
                data['fileBase64'] = img_base64
                data['fileName'] = img_filename if img_filename.endswith('.jpg') or img_filename.endswith('.jpeg') else "arquivo.jpg"

            payload_size = len(json.dumps(data))
            update_status(f"Tamanho do payload: {payload_size} bytes")

            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code in [200, 201]:
                update_status(f"Mensagem enviada com sucesso para: {row['nome']}")
            else:
                update_status(f"Erro ao enviar mensagem para: {row['nome']}; Status Code: {response.status_code}; Response: {response.text}")

            # Atualizar barra de progresso
            progress['value'] = (index + 1) / total_messages * 100
            progress_label.config(text=f"{progress['value']:.2f}%")
            root.update_idletasks()

            time.sleep(interval)
        except Exception as e:
            update_status(f"Erro ao processar o envio para {row['nome']}: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Envio de Mensagens")

# Cores do WhatsApp
whatsapp_green = "#25D366"
whatsapp_dark_green = "#128C7E"
whatsapp_light_gray = "#ECE5DD"
whatsapp_white = "#FFFFFF"
whatsapp_gray = "#3C3C3C"

style = ttk.Style()
style.theme_use('clam')  # Escolha o tema
style.configure("TButton", padding=6, relief="flat", background=whatsapp_dark_green, foreground=whatsapp_white)
style.configure("TLabel", padding=6, background=whatsapp_light_gray, foreground=whatsapp_gray)
style.configure("TEntry", padding=6, fieldbackground=whatsapp_white, foreground=whatsapp_gray)
style.configure("TText", padding=6, background=whatsapp_white, foreground=whatsapp_gray)
style.configure("TFrame", background=whatsapp_light_gray)

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Botões e labels
load_excel_btn = ttk.Button(main_frame, text="Carregar Excel", command=load_excel)
load_excel_btn.grid(row=0, column=0, pady=5, sticky="ew")

load_img_btn = ttk.Button(main_frame, text="Carregar Imagem", command=load_image)
load_img_btn.grid(row=0, column=1, pady=5, sticky="ew")

clear_img_btn = ttk.Button(main_frame, text="Limpar Imagem", command=clear_image)
clear_img_btn.grid(row=0, column=2, pady=5, sticky="ew")

message_label = ttk.Label(main_frame, text="Digite a mensagem com placeholders:")
message_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")

# Adicionar botões de placeholders
placeholders = ['nome', 'valor', 'data']
for i, placeholder in enumerate(placeholders):
    ttk.Button(main_frame, text=placeholder, command=lambda p=placeholder: insert_placeholder(p)).grid(row=2, column=i, pady=5, padx=5)

message_text = scrolledtext.ScrolledText(main_frame, height=5, wrap=tk.WORD)
message_text.grid(row=3, column=0, columnspan=3, pady=5, sticky="nsew")

client_id_label = ttk.Label(main_frame, text="ID de Cliente:")
client_id_label.grid(row=4, column=0, pady=5, sticky="w")

client_id_entry = ttk.Entry(main_frame)
client_id_entry.grid(row=4, column=1, pady=5, sticky="ew")

interval_label = ttk.Label(main_frame, text="Intervalo entre envios (ms):")
interval_label.grid(row=5, column=0, pady=5, sticky="w")

interval_entry = ttk.Entry(main_frame)
interval_entry.grid(row=5, column=1, pady=5, sticky="ew")

send_msg_btn = ttk.Button(main_frame, text="Enviar Mensagens", command=send_messages)
send_msg_btn.grid(row=5, column=2, pady=5, sticky="ew")

status_label = ttk.Label(main_frame, text="Status dos envios:")
status_label.grid(row=6, column=0, columnspan=3, pady=5, sticky="w")

status_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD)
status_text.grid(row=7, column=0, columnspan=3, pady=5, sticky="nsew")

# Adicionar barra de progresso
progress = ttk.Progressbar(main_frame, orient="horizontal", length=100, mode="determinate")
progress.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
progress_label = ttk.Label(main_frame, text="0%")
progress_label.grid(row=8, column=2, pady=10, sticky="ew")

# Configurar redimensionamento
main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_rowconfigure(7, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
