import sys
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QLabel, QLineEdit, QStackedWidget, QMessageBox,
    QWidget, QVBoxLayout, QFormLayout, QInputDialog, QHBoxLayout, QDialog, QComboBox
)
from PyQt5.QtGui import QPixmap

# Banco de dados simulado
usuarios = {}

# Cardápio com preços
cardapio = {
    "Pizza": {"preco": 50},
    "Lasanha": {"preco": 40},
    "Suco": {"preco": 10},
    "Café": {"preco": 5},
    "Energético": {"preco": 15},
    "Salgado Frito": {"preco": 7.50},
    "Salgado Assado": {"preco": 8}
}

class TelaLogin(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QFormLayout()
        self.usuario_input = QLineEdit()
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Usuário:", self.usuario_input)
        layout.addRow("Senha:", self.senha_input)

        btn_login = QPushButton("Entrar")
        btn_cadastro = QPushButton("Cadastrar")
        btn_login.clicked.connect(self.login)
        btn_cadastro.clicked.connect(lambda: self.app.setCurrentIndex(1))
        layout.addRow(btn_login, btn_cadastro)
        self.setLayout(layout)

    def login(self):
        user = self.usuario_input.text()
        senha = self.senha_input.text()
        if user in usuarios and usuarios[user]["senha"] == senha:
            self.app.usuario_atual = user
            QMessageBox.information(self, "Sucesso", f"Bem-vindo, {user}!")
            self.app.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")

class TelaCadastro(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QFormLayout()
        self.usuario_input = QLineEdit()
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Novo usuário:", self.usuario_input)
        layout.addRow("Nova senha:", self.senha_input)

        btn_cadastrar = QPushButton("Cadastrar")
        btn_voltar = QPushButton("Voltar")
        btn_cadastrar.clicked.connect(self.cadastrar)
        btn_voltar.clicked.connect(lambda: self.app.setCurrentIndex(0))
        layout.addRow(btn_cadastrar, btn_voltar)
        self.setLayout(layout)

    def cadastrar(self):
        user = self.usuario_input.text()
        senha = self.senha_input.text()
        if user in usuarios:
            QMessageBox.warning(self, "Erro", "Usuário já existe!")
        else:
            usuarios[user] = {"senha": senha, "quarto": None, "pedido": [], "dias": 0}
            QMessageBox.information(self, "Sucesso", "Usuário cadastrado!")
            self.app.setCurrentIndex(0)

class TelaMenu(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        layout = QVBoxLayout()
        self.bem_vindo = QLabel()
        btn_quarto = QPushButton("Escolher Quarto")
        btn_cardapio = QPushButton("Escolher Itens do Cardápio")
        btn_checkout = QPushButton("Fazer Checkout")
        btn_quarto.clicked.connect(self.escolher_quarto)
        btn_cardapio.clicked.connect(self.escolher_cardapio)
        btn_checkout.clicked.connect(self.checkout)
        layout.addWidget(self.bem_vindo)
        layout.addWidget(btn_quarto)
        layout.addWidget(btn_cardapio)
        layout.addWidget(btn_checkout)
        self.setLayout(layout)

    def showEvent(self, event):
        user = self.app.usuario_atual
        self.bem_vindo.setText(f"Bem-vindo, {user}")

    def escolher_quarto(self):
        user = self.app.usuario_atual
        quartos = {1: 150, 2: 200, 3: 300}
        quarto_escolhido, ok = QInputDialog.getInt(self, "Escolher Quarto", "Escolha (1: R$150, 2: R$200, 3: R$300):")
        if ok and quarto_escolhido in quartos:
            dias, ok2 = QInputDialog.getInt(self, "Dias", "Quantos dias de estadia?")
            if ok2:
                usuarios[user]["quarto"] = quartos[quarto_escolhido]
                usuarios[user]["dias"] = dias
                QMessageBox.information(self, "Quarto reservado",
                                        f"Quarto {quarto_escolhido} reservado por {dias} dias.")

    def escolher_cardapio(self):
        user = self.app.usuario_atual
        item, ok = QInputDialog.getItem(self, "Cardápio", "Escolha um item:", list(cardapio.keys()), 0, False)
        if ok:
            usuarios[user]["pedido"].append(item)
            QMessageBox.information(self, "Item adicionado", f"{item} adicionado à conta.")

    def checkout(self):
        user = self.app.usuario_atual
        pedido = usuarios[user]["pedido"]
        dias = usuarios[user]["dias"]
        valor_quarto = usuarios[user]["quarto"] or 0
        valor_pedidos = sum([cardapio[i]["preco"] for i in pedido])
        subtotal = valor_quarto * dias + valor_pedidos

        dialog = QDialog()
        dialog.setWindowTitle("Checkout")
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Subtotal: R${subtotal:.2f}"))

        # Mostra miniaturas dos itens do cardápio
        layout.addWidget(QLabel("Itens consumidos:"))
        for item in pedido:
            hbox = QHBoxLayout()
            imagem = QLabel()
            pixmap = QPixmap(cardapio[item]["imagem"])
            pixmap = pixmap.scaled(64, 64)
            imagem.setPixmap(pixmap)
            hbox.addWidget(imagem)
            hbox.addWidget(QLabel(f"{item} - R${cardapio[item]['preco']}"))
            layout.addLayout(hbox)

        layout.addWidget(QLabel("Forma de pagamento:"))
        combo_pagamento = QComboBox()
        combo_pagamento.addItems(["PIX", "Cartão de Débito", "À vista (PIX ou Débito)"])
        layout.addWidget(combo_pagamento)

        btn_finalizar = QPushButton("Finalizar Pagamento")

        def finalizar_pagamento():
            forma = combo_pagamento.currentText()
            desconto = 0
            if forma == "PIX":
                desconto = 0.05
            elif forma == "Cartão de Débito":
                desconto = 0.03
            elif forma == "À vista (PIX ou Débito)":
                desconto = 0.08
            total = subtotal * (1 - desconto)
            QMessageBox.information(dialog, "Pagamento", f"Total com desconto: R${total:.2f}")
            dialog.accept()
            self.app.setCurrentIndex(0)

        btn_finalizar.clicked.connect(finalizar_pagamento)
        layout.addWidget(btn_finalizar)
        dialog.setLayout(layout)
        dialog.exec_()

class HotelApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.usuario_atual = None
        self.addWidget(TelaLogin(self))
        self.addWidget(TelaCadastro(self))
        self.addWidget(TelaMenu(self))
        self.setWindowTitle("Sistema de Hotel")
        self.resize(500, 400)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = HotelApp()
    janela.show()
    sys.exit(app.exec_())
