import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# Funções do gerenciador

def listar_programas():
    """Lista programas instalados usando Winget"""
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "📦 Listando programas instalados...\n\n")
    os.system("winget list > temp_list.txt")
    with open("temp_list.txt", "r", encoding="utf-8") as f:
        output_text.insert(tk.END, f.read())
    os.remove("temp_list.txt")

def atualizar_programas():
    """Atualiza todos os programas usando Winget"""
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "🔄 Atualizando todos os programas...\n\n")
    os.system("winget upgrade --all --silent > temp_update.txt")
    with open("temp_update.txt", "r", encoding="utf-8") as f:
        output_text.insert(tk.END, f.read())
    os.remove("temp_update.txt")
    messagebox.showinfo("Atualização", "✅ Atualização concluída!")


def remover_programa():
    """Remove um programa usando Winget"""
    programa = simpledialog.askstring("Remover Programa", "Digite o ID ou Nome do programa:")
    if programa:
        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover '{programa}'?")
        if confirm:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, f"🗑 Removendo {programa}...\n\n")
            os.system(
                f"winget uninstall --id \"{programa}\" --silent || winget uninstall \"{programa}\" --silent > temp_remove.txt")

            # Corrige Unicode
            try:
                with open("temp_remove.txt", "r", encoding="utf-8", errors="replace") as f:
                    output_text.insert(tk.END, f.read())
            except Exception as e:
                output_text.insert(tk.END, f"❌ Erro ao ler saída: {e}")

            os.remove("temp_remove.txt")
            messagebox.showinfo("Remoção", f"✅ Programa '{programa}' removido com sucesso!")
        else:
            messagebox.showinfo("Remoção", "❌ Remoção cancelada.")
    else:
        messagebox.showwarning("Remoção", "⚠️ Nenhum programa informado.")

# Criando a interface
root = tk.Tk()
root.title("Gerenciador de Programas - Windows")
root.geometry("800x600")

# Botões
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_listar = tk.Button(frame_buttons, text="Listar Programas", width=20, command=listar_programas)
btn_listar.grid(row=0, column=0, padx=5)

btn_atualizar = tk.Button(frame_buttons, text="Atualizar Todos", width=20, command=atualizar_programas)
btn_atualizar.grid(row=0, column=1, padx=5)

btn_remover = tk.Button(frame_buttons, text="Remover Programa", width=20, command=remover_programa)
btn_remover.grid(row=0, column=2, padx=5)

# Caixa de texto para mostrar saída
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
