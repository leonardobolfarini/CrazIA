import pytesseract
from PIL import Image 

def extrair_texto_receita(imagem_path):
    imagem = Image.open(imagem_path)
    texto = pytesseract.image_to_string(imagem, lang='por')
    return texto
