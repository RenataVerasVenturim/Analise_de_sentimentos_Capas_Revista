#-------------------BAIXAR IMAGENS--------------------------------------
import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Configurar o driver do Selenium (sem especificar executable_path)
driver = webdriver.Chrome()

# URL da página a ser acessada
url = 'https://veja.abril.com.br/edicoes-veja/'

# Acessar a página com o Selenium
driver.get(url)

# Aguardar um tempo para a página carregar completamente (ajuste conforme necessário)
driver.implicitly_wait(10)

# Obter o conteúdo da página carregada
page_content = driver.page_source

# Fechar o driver do Selenium
driver.quit()

# Analisar o conteúdo da página com BeautifulSoup
soup = BeautifulSoup(page_content, 'html.parser')

# Encontrar todas as tags de imagem com a classe "media lazyloaded"
img_tags = soup.find_all('img', class_='media lazyloaded')

# Criar a pasta 'capas' se ela não existir
if not os.path.exists('capas'):
    os.makedirs('capas')

# Loop através das tags de imagem
for img_tag in img_tags:
    # Obter o URL da imagem original
    img_url = img_tag['data-src']

    # Analisar a URL para modificar os valores de "w" e "h"
    parsed_url = urlparse(img_url)
    query_params = parse_qs(parsed_url.query)
    query_params['w'] = ['570']  # Novo valor de largura
    query_params['h'] = ['750']  # Novo valor de altura

    # Recriar a URL modificada
    modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                               parsed_url.params, urlencode(query_params, doseq=True), parsed_url.fragment))

    # Baixar a imagem
    img_data = requests.get(modified_url).content

    # Extrair o nome do arquivo da URL ou criar um nome baseado na posição da imagem
    img_filename = os.path.basename(urlparse(modified_url).path) or f"image_{img_tags.index(img_tag)}.jpg"

    # Caminho completo do arquivo na pasta 'capas'
    img_path = os.path.join('capas', img_filename)

    # Salvar a imagem na pasta 'capas'
    with open(img_path, 'wb') as img_file:
        img_file.write(img_data)

    print(f'Imagem salva como {img_path}')

print('Download de imagens concluído.')

#-------------------EXTRAIR TEXTOS DAS IMAGENS COM TESSERACT--------------

import os
import cv2
from pytesseract import pytesseract

# Configuração do caminho do executável do Tesseract
caminho_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pytesseract.tesseract_cmd = caminho_tesseract

# Diretório das imagens
diretorio_imagens = 'capas'

# Lista para armazenar o texto extraído de cada imagem
textos = []

# Loop através de todas as imagens na pasta 'capas'
for imagem_filename in os.listdir(diretorio_imagens):
    if imagem_filename.endswith('.jpg'):
        imagem_path = os.path.join(diretorio_imagens, imagem_filename)

        # Carregar a imagem usando OpenCV
        image = cv2.imread(imagem_path)

        # Ajustar o brilho e o contraste (se necessário)
        brightness = 0.0  # Ajuste o brilho conforme necessário
        contrast = 1.0    # Ajuste o contraste conforme necessário
        adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

        # Executar OCR na imagem ajustada
        texto = pytesseract.image_to_string(adjusted_image)

        # Adicionar o texto extraído à lista
        textos.append(texto)

# Agora você tem todos os textos extraídos em uma lista chamada 'textos'
# Você pode salvá-los em um arquivo ou processá-los de acordo com suas necessidades

# Exemplo: Salvar os textos em um arquivo de texto
with open('textos_extraidos.txt', 'w', encoding='utf-8') as arquivo_texto:
    for texto in textos:
        arquivo_texto.write(texto)
        arquivo_texto.write('\n')

print('Extração de texto concluída e textos salvos em "textos_extraidos.txt".')
#---------------------------ANÁLISE DE SENTIMENTO TEXTUAL----------------
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

# Certifique-se de ter o VADER Lexicon baixado
nltk.download('vader_lexicon')

# Instancie o analisador de sentimento
sia = SentimentIntensityAnalyzer()

# Nome do arquivo de texto
nome_arquivo = "textos_extraidos.txt"

# Lê o texto do arquivo
with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
    texto = arquivo.read()

# Realize a análise de sentimento
sentimento = sia.polarity_scores(texto)

# Interpretando os resultados
if sentimento['compound'] >= 0.05:
    resultado = "Positivo"
elif sentimento['compound'] <= -0.05:
    resultado = "Negativo"
else:
    resultado = "Neutro"

print("-----Análise de sentimento com NLTK:-----")
print("Análise de sentimento:", resultado)
print("Score de sentimento:", sentimento)

# Nome do arquivo de texto
nome_arquivo = "textos_extraidos.txt"

# Lê o texto do arquivo
with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
    texto = arquivo.read()

# Crie um objeto TextBlob com o texto
blob = TextBlob(texto)

# Realize a análise de sentimento
analise_sentimento = blob.sentiment

# Interpretando os resultados
if analise_sentimento.polarity > 0:
    resultado = "Positivo"
elif analise_sentimento.polarity < 0:
    resultado = "Negativo"
else:
    resultado = "Neutro"

print("-----Análise de sentimento com textblob:-----")
print("Análise de Sentimento:", resultado)
print("Polaridade:", analise_sentimento.polarity)
print("Subjetividade:", analise_sentimento.subjectivity)

