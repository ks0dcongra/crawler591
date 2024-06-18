from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

def main():
    # 獲取用戶輸入的網址
    house_url = input("請輸入要訪問的591網址: ")

    # 創建爬蟲
    driver = webdriver.Chrome()

    try:
        # 透過網址打開591
        # house_url = "https://rent.591.com.tw/16824984"
        driver.get(house_url)

        # 模擬滑鼠操作移動到網頁總高度的8%位置上
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.08);")

        # 獲取591房子標題，需去除標題兩側的空白字元
        house_title_div = driver.find_element(By.CLASS_NAME, "house-title")
        house_title_h1_tag = house_title_div.find_element(By.TAG_NAME, "h1")
        house_title=house_title_h1_tag.text.strip()

        # 用標題名稱來創建資料夾，需確認資料夾是否存在
        if not os.path.exists(house_title):
            os.makedirs(house_title)
        
        # 等待一秒，確保爬蟲會點擊到查看更多照片
        time.sleep(1)

        # 點擊查看全部照片，需避免591中的漂浮物件阻擋我們點擊
        link = driver.find_element(By.CLASS_NAME, "view-more-btn")
        driver.execute_script("arguments[0].click();", link)

        # 下載照片至資料夾
        album_divs=driver.find_elements(By.CLASS_NAME,"album-img")
        for i, album_div in enumerate(album_divs):
            img_tag = album_div.find_element(By.TAG_NAME, "img")
            img_url=img_tag.get_attribute("data-src")
            if img_url:
                img_data = requests.get(img_url).content
                with open(f"{house_title}/image_{i+1}.jpg", "wb") as img_file:
                    img_file.write(img_data)

    except Exception as e:
        print(f"出現錯誤: {e}")

    finally:
        # 關閉爬蟲
        driver.quit()

if __name__ == "__main__":
    while True:
        main()
    
    