import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

website_url = input("URL plz:")
headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
}
cookies = {
    'eb9e6_winduser': '———YOUR OWN CODE',

}

def check_string(string):
    banned_words = ["face", "masha", "home", "logo", "segucrwj","none.gif",".php","kong.png","post.png","reply.png","mobile"]

    for word in banned_words:
        if word in string:
            return False

    return True

def delete_small_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            if file_size < 50000:  # 文件大小小于50KB
                os.remove(file_path)

ss1 = requests.Session()

response = ss1.get(webite_url,headers=headers,cookies=cookies)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string.strip()
    sub_title = title.split(" - 南+")[0].strip()
    save_folder = f"Your Own Path/{sub_title}"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    img_tags = soup.find_all("img")
    print(img_tags)

    for img_tag in img_tags:
        img_src = img_tag["src"]
        print(img_src+'\n')

        img_url = urljoin(website_url, img_src)
        img_filename = os.path.basename(urlparse(img_url).path)

        if check_string(img_filename):
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_filename = os.path.basename(urlparse(img_url).path)
                save_path = os.path.join(save_folder, img_filename)
                with open(save_path, "wb") as img_file:
                    img_file.write(img_response.content)
                print(f"保存图片：{img_filename}")
            else:
                print(f"下载图片失败：{img_url}")

else:
    print(f"获取网页内容失败：{website_url}")

delete_small_files(save_folder)