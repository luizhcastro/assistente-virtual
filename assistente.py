import speech_recognition as sr
from nltk import word_tokenize
from nltk.corpus import stopwords
from enfermeira import *
from dispositivos import controle
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "./config.json"

ATUADORES = {
    "enfermeira": {
        "parametros": {"ultimo_chamado": None},  
        "atuar": atuar_sobre_chamado,
    },
    "luz": {"atuar": lambda dispositivo, funcao, params, valor_parametro: controle.controlar_luz(funcao == "ligar")},
    "lâmpada": {"atuar": lambda dispositivo, funcao, params, valor_parametro: controle.controlar_luz(funcao == "ligar")},
    "ar": {"atuar": lambda dispositivo, funcao, params, valor_parametro: controle.controlar_ar(funcao, valor_parametro)},
    "tv": {"atuar": lambda dispositivo, funcao, params, valor_parametro: controle.controlar_tv(funcao == "ligar")},
    "televisão": {"atuar": lambda dispositivo, funcao, params, valor_parametro: controle.controlar_tv(funcao == "ligar")},
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

    palavras_de_parada = set(stopwords.words(IDIOMA_CORPUS))

    configuracao = carregar_configuracao()
    if not configuracao:
        return False, None, None

    for dispositivo, dados in ATUADORES.items():
        dados["parametros"] = None
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
    palavras_de_parada = set(stopwords.words(IDIOMA_CORPUS))
    tokens = word_tokenize(transcricao)
    tokens_filtrados = [token for token in tokens if token not in palavras_de_parada]
    print(f"Tokens processados: {tokens_filtrados}")
    return tokens_filtrados

def encontrar_comando(tokens, acoes):
    for acao in acoes:
        if acao["nome"] in tokens or ("temperatura" in tokens and acao["nome"] == "ar"):
            dispositivo = acao["nome"]
            for funcao in acao["funcoes"]:
                if funcao in tokens:
                    parametros = None
                    if funcao in ["ajustar", "definir", "aumentar", "diminuir"]:
                        parametros = next((token for token in tokens if token.isdigit()), None)
                    return True, dispositivo, funcao, parametros
    return False, None, None, None

def executar_comando(dispositivo, funcao, parametros):
    print(f"Executando comando: {dispositivo} - {funcao} - Parâmetros: {parametros}")
    if dispositivo in ATUADORES:
        atuador = ATUADORES[dispositivo]
        params = atuador.get("parametros", {})
        atuador["atuar"](dispositivo, funcao, params, parametros)
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
