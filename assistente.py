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

def iniciar():
    global reconhecedor
    iniciado = False
    global acoes
    global palavras_de_parada
    
    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

    try:
        with open(CAMINHO_CONFIGURACAO, "r") as arquivo_de_configuracao:
            configuracao = json.load(arquivo_de_configuracao)
            acoes = configuracao["acoes"]
            arquivo_de_configuracao.close()

        iniciado = True
    except FileNotFoundError:
        print("Arquivo de configuração não encontrado!")
        return False, None, None

    
    for dispositivo, dados in ATUADORES.items():
        parametros = dados["iniciar"]()
        dados["parametros"] = parametros

    return iniciado, reconhecedor, acoes

def escutar_fala(reconhecedor):
    tem_fala = False
    fala = None

    with sr.Microphone() as fonte_de_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_de_audio)  # Ajuste para o ruído ambiente
        print("\nOuvindo... Fale seu comando!")
        
        try:
            fala = reconhecedor.listen(fonte_de_audio, timeout=5)
            tem_fala = True
            print("Fala detectada!")  # Confirma que algo foi capturado
        except sr.UnknownValueError:
            print("Não consegui ouvir nada!")
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido!")
    
    return tem_fala, fala

def transcrever_fala(fala, reconhecedor):
    tem_transcricao = False
    transcricao = None
    
    try:
        transcricao = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        tem_transcricao = True
        print(f"Comando detectado: {transcricao}")  # Imprime a transcrição
    except sr.UnknownValueError:
        print("Não entendi o comando. Pode repetir?")
    
    return tem_transcricao, transcricao.lower() if transcricao else None

def tokenizar_transcricao(transcricao):
    tokens = word_tokenize(transcricao)
    print(f"Tokens: {tokens}")  # Exibe os tokens gerados
    return tokens

def validar_comando(tokens, acoes):
    valido, dispositivo, funcao, parametros = False, None, None, None

    for i, token in enumerate(tokens):
        for acao in acoes:
            if token == acao["nome"]:
                dispositivo = token
                # Verificar função
                for funcao_possivel in acao["funcoes"]:
                    if funcao_possivel in tokens[i + 1:]:
                        funcao = funcao_possivel
                        parametros = ' '.join(tokens[i + 2:])
                        valido = True
                        break
                if valido:
                    break

    return valido, dispositivo, funcao, parametros



def executar_comando(dispositivo, funcao, parametros):
    print(f"Executando: {dispositivo} - {funcao}")
    if dispositivo in ATUADORES:
        atuador = ATUADORES[dispositivo]
        parametros_de_atuacao = atuador["parametros"]
        processo_paralelo = Thread(
            target=atuador["atuar"],
            args=[dispositivo, funcao, parametros_de_atuacao, parametros]
        )
        processo_paralelo.start()
    else:
        print(f"Dispositivo '{dispositivo}' não encontrado.")

def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada
    tokens_filtrados = [token for token in tokens if token not in palavras_de_parada]
    print(f"Tokens após remoção das palavras de parada: {tokens_filtrados}")  # Exibe tokens após filtragem
    return tokens_filtrados

palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))


if __name__ == "__main__":
    iniciado, reconhecedor, acoes = iniciar()

    if iniciado:
        print("Assistente Virtual iniciada!")
        print("Comandos disponíveis:")
        for acao in acoes:
            print(f"- {acao['nome']} [{ ' | '.join(acao['funcoes']) }]")
        
        while True:
            tem_fala, fala = escutar_fala(reconhecedor)
            if tem_fala:
                tem_transcricao, transcricao = transcrever_fala(fala, reconhecedor)
                if tem_transcricao:
                    tokens = tokenizar_transcricao(transcricao)
                    tokens = eliminar_palavras_de_parada(tokens)

                    valido, dispositivo, funcao, parametros = validar_comando(tokens, acoes)
                    if valido:
                        executar_comando(dispositivo, funcao, parametros)
                    else:
                        print("Comando inválido, por favor tente novamente")
