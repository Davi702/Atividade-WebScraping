import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def coletar_dados_x(url_perfil, limite=4):
    chrome_options = Options()
    # Se quiser que o navegador não apareça, use: chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    dados = []

    try:
        driver.get(url_perfil)
        print("Aguardando carregamento (faça o login se necessário)...")
        
        time.sleep(10) 

        posts = driver.find_elements(By.TAG_NAME, "article")[:limite]

        for post in posts:
            try:
                autor = post.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text.split('\n')[0]
                texto = post.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                data = post.find_element(By.TAG_NAME, "time").get_attribute("datetime")

                dados.append({"autor": autor, "descricao": texto, "data": data})
            except:
                continue

        return dados

    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://x.com/NASA"
    lista_de_posts = coletar_dados_x(url, limite=4)

    # Se coletou algo, salva no CSV usando Pandas
    if lista_de_posts:
        df = pd.DataFrame(lista_de_posts)
        df.to_csv("posts_coletados.csv", index=False, encoding="utf-8-sig")
        print(f"Sucesso! {len(df)} posts salvos em 'posts_coletados.csv'")
    else:
        print("Falha na coleta. Verifique se o perfil é público ou se precisa de login.")