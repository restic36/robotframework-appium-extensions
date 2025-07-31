from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import cv2
from skimage.metrics import structural_similarity as ssim
import os


class ScreenshotComparisonKeywords:

    def __init__(self):
        self._builtin = BuiltIn()

    @property
    def driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword("Capturar Screenshot Inicial Como")
    def capturar_screenshot_inicial(self, nome_arquivo, caminho="screenshots"):
        os.makedirs(caminho, exist_ok=True)
        caminho_completo = os.path.join(caminho, nome_arquivo)
        self.driver.save_screenshot(caminho_completo)
        logger.info(f"📸 Screenshot inicial salvo em: {caminho_completo}")

    @keyword("Comparar Screenshot Final Com")
    def comparar_screenshot_final(self, arquivo_referencia, tolerancia=0.01, caminho="screenshots"):
        os.makedirs(caminho, exist_ok=True)
        imagem_final_path = os.path.join(caminho, "screenshot_final.png")
        diff_path = os.path.join(caminho, "diff.png")

        self.driver.save_screenshot(imagem_final_path)
        logger.info(f"📸 Screenshot final salvo em: {imagem_final_path}")

        if not os.path.exists(arquivo_referencia):
            raise FileNotFoundError(f"❌ Arquivo de referência não encontrado: {arquivo_referencia}")
        if not os.path.exists(imagem_final_path):
            raise FileNotFoundError(f"❌ Arquivo da imagem final não encontrado: {imagem_final_path}")

        imagem1 = cv2.imread(arquivo_referencia)
        imagem2 = cv2.imread(imagem_final_path)

        if imagem1 is None or imagem2 is None:
            raise ValueError("❌ Falha ao carregar uma ou ambas as imagens.")

        if imagem1.shape != imagem2.shape:
            raise AssertionError("❌ As imagens têm tamanhos diferentes e não podem ser comparadas.")

        gray1 = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(imagem2, cv2.COLOR_BGR2GRAY)

        score, diff = ssim(gray1, gray2, full=True)
        percentual_diferenca = 1 - score

        # Normaliza diff para imagem e salva diff visual
        diff = (diff * 255).astype("uint8")
        cv2.imwrite(diff_path, diff)
        logger.info(f"📂 Diferença visual salva como: {diff_path}")

        logger.info(f"🔍 Similaridade SSIM: {score:.4f} — Diferença: {percentual_diferenca:.2%}")

        if percentual_diferenca > tolerancia:
            raise AssertionError(f"❌ Diferença visual maior que o tolerado: {percentual_diferenca:.2%}")
        
        logger.info("✅ As imagens são visualmente semelhantes dentro da tolerância.")
