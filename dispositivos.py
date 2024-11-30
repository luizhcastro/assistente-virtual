class ControleDispositivos:
    def __init__(self):
        self.luz_ligada = False
        self.tv_ligada = False
        self.temperatura_ar = 23

    def controlar_luz(self, ligar):
        self.luz_ligada = ligar
        print(f"Luz {'ligada' if ligar else 'desligada'}")

    def controlar_temperatura(self, valor=None):
        if valor is not None:
            self.temperatura_ar = valor
        print(f"Temperatura ajustada para {self.temperatura_ar}°C")

    def controlar_tv(self, ligar):
        self.tv_ligada = ligar
        print(f"TV {'ligada' if ligar else 'desligada'}")


controle = ControleDispositivos()

def iniciar_dispositivos():
    print("Sistema de controle de dispositivos iniciado")
    return {"controle": controle}

def atuar_sobre_dispositivos(dispositivo, funcao, parametros, valor_parametro):
    if dispositivo in ["luz", "lâmpada"]:
        if funcao in ["ligar", "desligar"]:
            controle.controlar_luz("ligar" in funcao)
    elif dispositivo == "ar":
        if funcao in ["ligar", "desligar"]:
            print(f"Ar condicionado {'ligado' if funcao == 'ligar' else 'desligado'}")
        elif funcao in ["ajustar", "definir", "temperatura"]:
            try:
                valor = int(''.join(filter(str.isdigit, valor_parametro)))
                controle.controlar_temperatura(valor=valor)
            except ValueError:
                print("Valor de temperatura inválido")
    elif dispositivo in ["tv", "televisão"]:
        if funcao in ["ligar", "desligar"]:
            controle.controlar_tv("ligar" in funcao)

