from datetime import datetime

def iniciar_chamado_enfermeira():
    print("Sistema de chamado de enfermeira iniciado")
    return {"ultimo_chamado": None}

def atuar_sobre_chamado(acao, funcao, parametros, valor_parametro):
    hora_atual = datetime.now().strftime("%H:%M:%S")
    
    if funcao == "chamar":
        print(f"[{hora_atual}] Chamando enfermeira... Solicitação enviada!")
        parametros["ultimo_chamado"] = hora_atual
    elif funcao == "cancelar":
        print(f"[{hora_atual}] Cancelando chamado da enfermeira...")
        parametros["ultimo_chamado"] = None
