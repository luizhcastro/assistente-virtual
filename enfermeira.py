def atuar_sobre_chamado(dispositivo, funcao, params, valor_parametro):
    from datetime import datetime
    hora_atual = datetime.now().strftime("%H:%M:%S")

    if funcao == "chamar":
        print(f"[{hora_atual}] Chamando enfermeira... Solicitação enviada!")
        if params is not None: 
            params["ultimo_chamado"] = hora_atual
    elif funcao == "cancelar":
        print(f"[{hora_atual}] Cancelando chamado da enfermeira.")
        if params is not None:
            params["ultimo_chamado"] = None
    else:
        print(f"Função desconhecida para o dispositivo '{dispositivo}'.")
