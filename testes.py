import unittest
import os
import speech_recognition as sr
from assistente import *
from dispositivos import ControleDispositivos

class TestAssistenteVirtual(unittest.TestCase):
    def setUp(self):
        """Inicializa o ambiente de teste"""
        self.iniciado, self.reconhecedor, self.acoes = iniciar()
        self.assertTrue(self.iniciado)
        
        # Reset dispositivos para estado inicial
        for dispositivo in ATUADORES.values():
            if "parametros" in dispositivo:
                if "controle" in dispositivo["parametros"]:
                    dispositivo["parametros"]["controle"] = ControleDispositivos()

    def simular_comando_voz(self, texto):
        """Helper para simular comando de voz a partir de texto"""
        tokens = tokenizar_e_filtrar(texto)
        return encontrar_comando(tokens, self.acoes)

    def test_inicializacao(self):
        """Testa se a inicialização ocorre corretamente"""
        self.assertIsNotNone(self.reconhecedor)
        self.assertIsNotNone(self.acoes)
        self.assertTrue(isinstance(self.acoes, list))

    def test_comandos_luz(self):
        """Testa comandos relacionados à luz"""
        # Teste ligar luz
        valido, dispositivo, funcao, params = self.simular_comando_voz("ligar luz")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "luz")
        self.assertEqual(funcao, "ligar")

        # Teste desligar luz
        valido, dispositivo, funcao, params = self.simular_comando_voz("desligar luz")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "luz")
        self.assertEqual(funcao, "desligar")

    def test_comandos_tv(self):
        """Testa comandos relacionados à TV"""
        # Teste ligar TV
        valido, dispositivo, funcao, params = self.simular_comando_voz("ligar televisão")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "televisão")
        self.assertEqual(funcao, "ligar")

        # Teste desligar TV
        valido, dispositivo, funcao, params = self.simular_comando_voz("desligar tv")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "tv")
        self.assertEqual(funcao, "desligar")

    def test_comandos_ar(self):
        """Testa comandos relacionados ao ar condicionado"""
        # Teste ligar ar
        valido, dispositivo, funcao, params = self.simular_comando_voz("ligar ar")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "ar")
        self.assertEqual(funcao, "ligar")

        # Teste ajustar temperatura
        valido, dispositivo, funcao, params = self.simular_comando_voz("ajustar temperatura do ar para 24")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "ar")
        self.assertEqual(funcao, "ajustar")
        self.assertIn("24", params)

        # Teste aumentar temperatura
        valido, dispositivo, funcao, params = self.simular_comando_voz("aumentar temperatura")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "ar")
        self.assertEqual(funcao, "aumentar")

    def test_comando_enfermeira(self):
        """Testa comando para chamar enfermeira"""
        valido, dispositivo, funcao, params = self.simular_comando_voz("chamar enfermeira")
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "enfermeira")
        self.assertEqual(funcao, "chamar")

    def test_comandos_invalidos(self):
        """Testa rejeição de comandos inválidos"""
        # Comando com dispositivo inexistente
        valido, *_ = self.simular_comando_voz("ligar radio")
        self.assertFalse(valido)

        # Comando com função inexistente
        valido, *_ = self.simular_comando_voz("piscar luz")
        self.assertFalse(valido)

        # Comando vazio
        valido, *_ = self.simular_comando_voz("")
        self.assertFalse(valido)

    def test_controle_dispositivos(self):
        """Testa a execução real dos comandos nos dispositivos"""
        # Inicializar dispositivos
        controle = ATUADORES["luz"]["parametros"]["controle"]
        
        # Testar luz
        executar_comando("luz", "ligar", "")
        self.assertTrue(controle.luz_ligada)
        
        executar_comando("luz", "desligar", "")
        self.assertFalse(controle.luz_ligada)

        # Testar TV
        executar_comando("tv", "ligar", "")
        self.assertTrue(controle.tv_ligada)
        
        executar_comando("tv", "desligar", "")
        self.assertFalse(controle.tv_ligada)

        # Testar ar condicionado
        executar_comando("ar", "ligar", "")
        self.assertTrue(controle.ar_ligado)
        
        temperatura_inicial = controle.temperatura_ar
        executar_comando("ar", "aumentar", "2")
        self.assertEqual(controle.temperatura_ar, temperatura_inicial + 2)

class TestProcessamentoTexto(unittest.TestCase):
    """Testes específicos para o processamento de texto"""
    
    def setUp(self):
        self.iniciado, self.reconhecedor, self.acoes = iniciar()

    def test_tokenizacao(self):
        """Testa a tokenização e filtragem de texto"""
        texto = "por favor ligar a luz do quarto"
        tokens = tokenizar_e_filtrar(texto)
        self.assertIn("ligar", tokens)
        self.assertIn("luz", tokens)
        self.assertNotIn("por", tokens)  # Stopword deve ser removida
        self.assertNotIn("a", tokens)    # Stopword deve ser removida

    def test_encontrar_comando(self):
        """Testa a extração de comandos do texto tokenizado"""
        tokens = ["ligar", "luz", "quarto"]
        valido, dispositivo, funcao, params = encontrar_comando(tokens, self.acoes)
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "luz")
        self.assertEqual(funcao, "ligar")

if __name__ == '__main__':
    unittest.main()