import speech_recognition as sr
from nltk import word_tokenize, corpus
from threading import Thread
from enfermeira import *
from dispositivos import *
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "./config.json"

ATUADORES = {
    "enfermeira": {
        "iniciar": iniciar_chamado_enfermeira,
        "atuar": atuar_sobre_chamado,
    },
    "luz": {
        "iniciar": iniciar_dispositivos,
        "atuar": atuar_sobre_dispositivos,
    },
    "lâmpada": {
        "iniciar": iniciar_dispositivos,
        "atuar": atuar_sobre_dispositivos,
    },
    "ar": {
        "iniciar": iniciar_dispositivos,
        "atuar": atuar_sobre_dispositivos,
    },
    "tv": {
        "iniciar": iniciar_dispositivos,
        "atuar": atuar_sobre_dispositivos,
    },
    "televisão": {
        "iniciar": iniciar_dispositivos,
        "atuar": atuar_sobre_dispositivos,
    },
}

def carregar_configuracao():
    try:
        with open(CAMINHO_CONFIGURACAO, "r", encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado!")
        return None
    except json.JSONDecodeError:
        print("Erro ao ler arquivo de configuração!")
        return None

def iniciar():
    global reconhecedor, palavras_de_parada
    

    reconhecedor = sr.Recognizer()
    reconhecedor.dynamic_energy_threshold = True
    reconhecedor.energy_threshold = 4000
    

    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))
    

    configuracao = carregar_configuracao()
    if not configuracao:
        return False, None, None
    

    for dispositivo, dados in ATUADORES.items():
        dados["parametros"] = dados["iniciar"]()

    return True, reconhecedor, configuracao["acoes"]

def escutar_fala(reconhecedor):
    with sr.Microphone() as fonte_de_audio:
        print("\nOuvindo... Fale seu comando!")
        try:
            reconhecedor.adjust_for_ambient_noise(fonte_de_audio, duration=1)
            fala = reconhecedor.listen(fonte_de_audio, timeout=5, phrase_time_limit=5)
            print("Fala detectada!")
            return True, fala
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            print("Não consegui ouvir nada!")
            return False, None

def transcrever_fala(fala, reconhecedor):
    try:
        transcricao = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        print(f"Comando detectado: {transcricao}")
        return True, transcricao.lower()
    except sr.UnknownValueError:
        print("Não entendi o comando. Pode repetir?")
        return False, None

def tokenizar_e_filtrar(transcricao):
    tokens = word_tokenize(transcricao)
    tokens_filtrados = [token for token in tokens if token not in palavras_de_parada]
    print(f"Tokens processados: {tokens_filtrados}")
    return tokens_filtrados

def encontrar_comando(tokens, acoes):
    for acao in acoes:
        if acao["nome"] in tokens:
            dispositivo = acao["nome"]
            for funcao in acao["funcoes"]:
                if funcao in tokens:
                    if funcao in ["ajustar", "definir", "aumentar", "diminuir"]:
                        parametros = ""
                        for token in tokens[tokens.index(funcao):]:
                            if token.isdigit():
                                parametros = token
                                break
                    else:
                        inicio_params = tokens.index(funcao) + 1
                        parametros = " ".join(tokens[inicio_params:])
                    
                    return True, dispositivo, funcao, parametros
    return False, None, None, None

def executar_comando(dispositivo, funcao, parametros):
    print(f"Executando comando: {dispositivo} - {funcao} - Parâmetros: {parametros}")
    if dispositivo in ATUADORES:
        atuador = ATUADORES[dispositivo]
        params = atuador["parametros"]
        Thread(
            target=atuador["atuar"],
            args=[dispositivo, funcao, params, parametros],
            daemon=True 
        ).start()
        
        import time
        time.sleep(0.1)
    else:
        print(f"Dispositivo '{dispositivo}' não encontrado.")


if __name__ == "__main__":
    iniciado, reconhecedor, acoes = iniciar()
        
    print("\nAssistente Virtual iniciada!")
    print("Comandos disponíveis:")
    for acao in acoes:
        print(f"- {acao['nome']}: {', '.join(acao['funcoes'])}")
    
    while True:
        tem_fala, fala = escutar_fala(reconhecedor)
        if tem_fala:
            tem_transcricao, transcricao = transcrever_fala(fala, reconhecedor)
            if tem_transcricao:
                tokens = tokenizar_e_filtrar(transcricao)
                valido, dispositivo, funcao, parametros = encontrar_comando(tokens, acoes)
                
                if valido:
                    executar_comando(dispositivo, funcao, parametros)
                else:
                    print("Comando não reconhecido. Por favor, tente novamente.")