import speech_recognition as sr 
import pyttsx3 
import os
import webbrowser
import subprocess
import requests


def falar(texto):
    """Converte texto em fala."""
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def falar(texto):
    engine = pyttsx3.init()

    # Alterar a velocidade da fala
    engine.setProperty("rate", 200)  # Padrão é 200

    # Alterar o volume (0.0 a 1.0)
    engine.setProperty("volume", 1.0)

    # Escolher tipo de voz 
    vozes = engine.getProperty("voices")
    engine.setProperty("voice", vozes[1].id) 

    engine.say(texto)
    engine.runAndWait()

def ouvir():
    """Captura áudio do microfone e converte em texto."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        print("Pode repetir por favor ? Não Entendi...")
        return ""
    except sr.RequestError:
        print("Erro na conexão...")
        return ""

API_WEATHER = "b476217bf067ecb67e83d9ec4b1b348c"
API_NEWS = "2a23c74692744f9fb7a1fadc2f301c8a"

# Inicializa o sintetizador de voz
voz = pyttsx3.init()

def falar(texto):
    """Faz o assistente falar."""
    voz.say(texto)
    voz.runAndWait()

def pegar_previsao_tempo(cidade="São Paulo"):
    """Obtém a previsão do tempo para uma cidade e fala o resultado."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_WEATHER}&lang=pt_br&units=metric"
    resposta = requests.get(url).json()

    if resposta["cod"] == 200:
        descricao = resposta["weather"][0]["description"]
        temperatura = resposta["main"]["temp"]
        previsao = f"O clima em {cidade} está {descricao} com temperatura de {temperatura}°C."
        
        falar(previsao)  # Faz o assistente falar a previsão
        return previsao
    else:
        erro_msg = "Não consegui obter a previsão do tempo."
        falar(erro_msg)
        return erro_msg

def pegar_noticias():
    """Obtém as últimas notícias e as lê em voz alta."""
    url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={API_NEWS}"
    resposta = requests.get(url).json()

    if resposta["status"] == "ok":
        noticias = resposta["articles"][:3]  # Pega as 3 primeiras notícias
        resultado = "Aqui estão as últimas notícias:\n"
        
        for i, noticia in enumerate(noticias, 1):
            titulo = noticia['title']
            resultado += f"{i}. {titulo}\n"
            falar(f"Notícia {i}: {titulo}")  # Assistente fala a notícia

        return resultado
    else:
        return "Não consegui obter as notícias."

def executar_comando(comando):
    """Executa ações com base no comando reconhecido."""

    # Previsão do tempo
    if "tempo" in comando or "previsão do tempo" in comando:
        palavras = comando.split()
        if "em" in palavras:
            indice = palavras.index("em")
            cidade = " ".join(palavras[indice + 1:])  # Pega tudo depois de "em"
        else:
            cidade = "São Paulo"  # Padrão caso não informe cidade

        resposta = pegar_previsao_tempo(cidade)
        falar(resposta)
        return resposta

    # Notícias
    elif "notícia" in comando or "notícias" in comando:
        resposta = pegar_noticias()
        falar(resposta)
        return resposta

    # Abrir programas e sites
    elif "abrir navegador" in comando:
        falar("Abrindo o navegador.")
        webbrowser.open("https://www.google.com")

    elif "abrir bloco de notas" in comando:
        falar("Abrindo o bloco de notas.")
        os.system("notepad")

    elif "abrir youtube" in comando:
        webbrowser.open("https://www.youtube.com")
        return "Abrindo YouTube..."

    elif "sair" in comando:
        falar("Encerrando o assistente. Até logo!")
        exit()

    elif "abrir calculadora" in comando:
        subprocess.run("calc.exe")
        return "Abrindo Calculadora..."

    elif "abrir explorador de arquivos" in comando:
        subprocess.run("explorer.exe")
        return "Abrindo Explorador de Arquivos..."

    elif "abrir netflix" in comando:
        webbrowser.open("https://www.netflix.com")
        return "Abrindo Netflix..."

    elif "abrir discord" in comando:
        webbrowser.open("https://discord.com/app")
        return "Abrindo Discord..."

    elif "abrir spotify" in comando:
        webbrowser.open("https://open.spotify.com")
        return "Abrindo Spotify..."

    elif "abrir instagram" in comando:
        webbrowser.open("https://www.instagram.com")
        return "Abrindo Instagram..."

    elif "abrir whatsapp" in comando:
        webbrowser.open("https://web.whatsapp.com")
        return "Abrindo WhatsApp Web..."
    
    elif "sair" in comando or "desligar" in comando:
        falar("Desligando o assistente. Até logo!")
        exit()  
    

    else:
        falar("Desculpe, não entendi o comando.")
        return "Comando não reconhecido."

# Loop principal
falar("Olá! Como posso ajudar?")
while True:
    comando_usuario = ouvir()
    if comando_usuario:
        executar_comando(comando_usuario)
