import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import datetime
import webbrowser
import os
import socket
import sys
from typing import Optional, List, Tuple
import threading

try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except ImportError:
    messagebox.showerror(
        "Erro",
        "A biblioteca PyDrive não está instalada.\nUse o comando:\npip install pydrive"
    )
    sys.exit(1)


class AssistenteVirtual:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.drive: Optional[GoogleDrive] = None
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface gráfica do usuário"""
        self.root.title("Assistente Virtual Avançado")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.root.minsize(450, 350)

        # Configuração do tema
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        self.titulo = ttk.Label(
            self.main_frame,
            text="Assistente Virtual",
            font=("Arial", 16, "bold"),
            anchor="center"
        )
        self.titulo.pack(pady=10)

        # Entrada de comando
        self.entrada_frame = ttk.Frame(self.main_frame)
        self.entrada_frame.pack(fill=tk.X, pady=10)

        self.entrada = ttk.Entry(
            self.entrada_frame,
            font=("Arial", 12),
            width=40
        )
        self.entrada.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entrada.bind("<Return>", lambda e: self.processar_comando())
        self.entrada.focus()

        # Botão de enviar
        self.botao = ttk.Button(
            self.entrada_frame,
            text="Executar",
            command=self.processar_comando
        )
        self.botao.pack(side=tk.LEFT, padx=5)

        # Área de resposta
        self.resposta_frame = ttk.LabelFrame(
            self.main_frame,
            text="Resposta",
            padding="10"
        )
        self.resposta_frame.pack(fill=tk.BOTH, expand=True)

        self.resposta = tk.Text(
            self.resposta_frame,
            font=("Arial", 11),
            fg="blue",
            wrap=tk.WORD,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.resposta.pack(fill=tk.BOTH, expand=True)

        # Barra de status
        self.status_bar = ttk.Label(
            self.root,
            text="Pronto",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Menu
        self.setup_menu()

    def setup_menu(self):
        """Configura o menu da aplicação"""
        menubar = tk.Menu(self.root)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Sincronizar com Google Drive",
            command=lambda: self.processar_comando("sincronizar google")
        )
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.destroy)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Comandos disponíveis", command=self.mostrar_ajuda)
        help_menu.add_command(label="Sobre", command=self.mostrar_sobre)
        menubar.add_cascade(label="Ajuda", menu=help_menu)

        self.root.config(menu=menubar)

    def mostrar_ajuda(self):
        """Mostra uma janela com os comandos disponíveis"""
        comandos = [
            ("Hora", "Mostra a hora atual"),
            ("Abrir navegador", "Abre o Google no navegador padrão"),
            ("Abrir spotify", "Abre o Spotify no navegador"),
            ("Sincronizar google", "Sincroniza arquivos com o Google Drive"),
            ("Sair/Fechar", "Fecha o aplicativo")
        ]

        ajuda_janela = tk.Toplevel(self.root)
        ajuda_janela.title("Comandos Disponíveis")
        ajuda_janela.geometry("400x300")

        frame = ttk.Frame(ajuda_janela, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Comandos disponíveis:", font=("Arial", 12, "bold")).pack(pady=5)

        for cmd, desc in comandos:
            frame_cmd = ttk.Frame(frame)
            frame_cmd.pack(fill=tk.X, pady=2)

            ttk.Label(frame_cmd, text=f"• {cmd}:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            ttk.Label(frame_cmd, text=desc, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        ttk.Button(ajuda_janela, text="Fechar", command=ajuda_janela.destroy).pack(pady=10)

    def mostrar_sobre(self):
        """Mostra uma janela com informações sobre o aplicativo"""
        sobre_janela = tk.Toplevel(self.root)
        sobre_janela.title("Sobre")
        sobre_janela.geometry("300x200")

        frame = ttk.Frame(sobre_janela, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Assistente Virtual", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(frame, text="Versão 2.0", font=("Arial", 10)).pack()
        ttk.Label(frame, text="Desenvolvido com Python e Tkinter", font=("Arial", 10)).pack(pady=10)
        ttk.Label(frame, text="© 2023 - Todos os direitos reservados", font=("Arial", 8)).pack(side=tk.BOTTOM)

        ttk.Button(sobre_janela, text="Fechar", command=sobre_janela.destroy).pack(pady=10)

    def atualizar_status(self, mensagem: str):
        """Atualiza a barra de status"""
        self.status_bar.config(text=mensagem)

    def mostrar_resposta(self, mensagem: str):
        """Mostra uma mensagem na área de resposta"""
        self.resposta.config(state=tk.NORMAL)
        self.resposta.delete(1.0, tk.END)
        self.resposta.insert(tk.END, mensagem)
        self.resposta.config(state=tk.DISABLED)
        self.resposta.see(tk.END)

    def tem_conexao(self) -> bool:
        """Verifica se há conexão com a internet"""
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def autenticar_google(self) -> Optional[GoogleDrive]:
        """Autentica com o Google Drive"""
        try:
            self.atualizar_status("Autenticando com o Google Drive...")
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()  # Abre o navegador para login
            self.drive = GoogleDrive(gauth)
            return self.drive
        except Exception as e:
            messagebox.showerror(
                "Erro de autenticação",
                f"Erro ao autenticar com o Google Drive:\n{e}"
            )
            return None
        finally:
            self.atualizar_status("Pronto")

    def sincronizar_arquivos(self):
        """Sincroniza arquivos com o Google Drive em uma thread separada"""
        if not self.tem_conexao():
            self.mostrar_resposta("Sem conexão com a internet.")
            return

        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos para sincronizar"
        )
        if not arquivos:
            self.mostrar_resposta("Nenhum arquivo selecionado.")
            return

        # Usar thread para não travar a interface
        threading.Thread(
            target=self._sincronizar_arquivos_thread,
            args=(arquivos,),
            daemon=True
        ).start()

    def _sincronizar_arquivos_thread(self, arquivos: List[str]):
        """Função executada em thread para sincronizar arquivos"""
        self.root.after(0, lambda: self.atualizar_status("Sincronizando arquivos..."))

        drive = self.autenticar_google()
        if not drive:
            self.root.after(0, lambda: self.mostrar_resposta("Falha na autenticação com o Google."))
            return

        try:
            total = len(arquivos)
            for i, arquivo in enumerate(arquivos, 1):
                nome = os.path.basename(arquivo)
                self.root.after(0, lambda: self.atualizar_status(f"Enviando {nome} ({i}/{total})..."))

                f = drive.CreateFile({'title': nome})
                f.SetContentFile(arquivo)
                f.Upload()

            self.root.after(0, lambda: self.mostrar_resposta(
                f"{total} arquivo(s) enviado(s) ao Google Drive com sucesso!"
            ))
        except Exception as e:
            self.root.after(0, lambda: self.mostrar_resposta(
                f"Erro ao enviar arquivos: {str(e)}"
            ))
        finally:
            self.root.after(0, lambda: self.atualizar_status("Pronto"))

    def processar_comando(self, comando: Optional[str] = None):
        """Processa o comando do usuário"""
        if comando is None:
            comando = self.entrada.get().strip().lower()
            self.entrada.delete(0, tk.END)

        if not comando:
            self.mostrar_resposta("Digite um comando.")
            return

        # Mapeamento de comandos para funções
        comandos = {
            "hora": self.mostrar_hora,
            "abrir navegador": self.abrir_navegador,
            "abrir google": self.abrir_navegador,
            "abrir spotify": self.abrir_spotify,
            "sair": self.fechar_aplicativo,
            "fechar": self.fechar_aplicativo,
            "sincronizar google": self.sincronizar_arquivos,
            "ajuda": self.mostrar_ajuda
        }

        # Verifica se o comando existe
        for cmd, func in comandos.items():
            if cmd in comando:
                func()
                return

        # Se não encontrou nenhum comando válido
        self.mostrar_resposta("Desculpe, não entendi o comando. Digite 'ajuda' para ver os comandos disponíveis.")

    def mostrar_hora(self):
        """Mostra a hora atual"""
        agora = datetime.datetime.now().strftime("%H:%M:%S")
        self.mostrar_resposta(f"Agora são {agora}.")

    def abrir_navegador(self):
        """Abre o Google no navegador padrão"""
        try:
            webbrowser.open("https://www.google.com")
            self.mostrar_resposta("Abrindo o Google no navegador...")
        except Exception as e:
            self.mostrar_resposta(f"Não foi possível abrir o navegador: {str(e)}")

    def abrir_spotify(self):
        """Abre o Spotify no navegador"""
        try:
            webbrowser.open("https://open.spotify.com/intl-pt")
            self.mostrar_resposta("Abrindo o Spotify...")
        except Exception as e:
            self.mostrar_resposta(f"Não foi possível abrir o Spotify: {str(e)}")

    def fechar_aplicativo(self):
        """Fecha o aplicativo"""
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AssistenteVirtual(root)
    root.mainloop()


if __name__ == "__main__":
    main()