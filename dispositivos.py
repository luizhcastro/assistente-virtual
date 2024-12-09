class ControleDispositivos:
    def __init__(self):
        self.luz_ligada = False
        self.tv_ligada = False
        self.temperatura_ar = 23
        self.ar_ligado = False

    def controlar_luz(self, ligar):
        self.luz_ligada = ligar
        print(f"Luz {'ligada' if ligar else 'desligada'}")

    def controlar_tv(self, ligar):
        self.tv_ligada = ligar
        print(f"TV {'ligada' if ligar else 'desligada'}")

    def controlar_ar(self, comando, valor_parametro=None):
        if comando in ["ligar", "desligar"]:
            self.ar_ligado = comando == "ligar"
            print(f"Ar condicionado {'ligado' if self.ar_ligado else 'desligado'}")
        elif comando in ["ajustar", "definir", "aumentar", "diminuir"]:
            if not self.ar_ligado:
                print("Ar condicionado está desligado!")
                return

            if valor_parametro:
                try:
                    valor = int(''.join(filter(str.isdigit, valor_parametro)))
                    if comando in ["aumentar"]:
                        self.temperatura_ar += valor if valor else 1
                    elif comando in ["diminuir", "abaixar"]:
                        self.temperatura_ar -= valor if valor else 1
                    else:
                        self.temperatura_ar = valor
                except ValueError:
                    if comando in ["aumentar"]:
                        self.temperatura_ar += 1
                    elif comando in ["diminuir", "abaixar"]:
                        self.temperatura_ar -= 1
                    
            self.temperatura_ar = max(16, min(30, self.temperatura_ar))
            print(f"Temperatura ajustada para {self.temperatura_ar}°C")

controle = ControleDispositivos()
