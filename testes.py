import unittest
from assistente import *

class TestAssistenteVirtual(unittest.TestCase):
    def setUp(self):
        self.iniciado, self.reconhecedor, self.acoes = iniciar()
        self.assertTrue(self.iniciado)

    def processar_audio_arquivo(self, caminho_audio, reconhecedor):
        try:
            with sr.AudioFile(caminho_audio) as fonte_de_audio:
                print(f"Processando o arquivo de áudio: {caminho_audio}")
                audio = reconhecedor.record(fonte_de_audio)
                return transcrever_fala(audio, reconhecedor)
        except FileNotFoundError:
            print(f"Arquivo de áudio não encontrado: {caminho_audio}")
            return False, None
        except Exception as e:
            print(f"Erro ao processar o arquivo de áudio: {e}")
            return False, None

    def test_chamar_enfermeira(self):
        caminho_audio = r".\\audios\\chamar a enfermeira.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "enfermeira")
        self.assertEqual(funcao, "chamar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_ligar_luz(self):
        caminho_audio = r".\\audios\\ligar luz.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "luz")
        self.assertEqual(funcao, "ligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_ligar_ar(self):
        caminho_audio = r".\\audios\\ligar ar condicionado.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "ar")
        self.assertEqual(funcao, "ligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_ligar_tv(self):
        caminho_audio = r".\\audios\\ligar a tv.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "tv")
        self.assertEqual(funcao, "ligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_ajustar_temperatura(self):
        caminho_audio = r".\\audios\\ajustar temperatura.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido, "Comando não reconhecido como válido.")
        self.assertEqual(dispositivo, "ar", "O dispositivo não foi identificado corretamente.")
        self.assertEqual(funcao, "ajustar", "A função não foi identificada corretamente.")
        self.assertEqual(params, "18", "O parâmetro da temperatura não foi identificado corretamente.")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")

        
    def test_desligar_luz(self):
        caminho_audio = r".\\audios\\desligar luz.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "luz")
        self.assertEqual(funcao, "desligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_desligar_ar(self):
        caminho_audio = r".\\audios\\desligar ar condicionado.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "ar-condicionado")
        self.assertEqual(funcao, "desligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")
        
    def test_desligar_tv(self):
        caminho_audio = r".\\audios\\desligar a tv.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, params = encontrar_comando(tokenizar_e_filtrar(transcricao), self.acoes)
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "tv")
        self.assertEqual(funcao, "desligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {params}")

if __name__ == '__main__':
    unittest.main()
