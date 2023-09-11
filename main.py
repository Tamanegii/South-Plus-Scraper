import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


web_url="https://www.spring-plus.net/"
headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
}
cookies = {
    'eb9e6_winduser': 'YOUE COOKIE',

}
save_folder = "YOUR SAVE FOLDER"

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

def find_url(tid):
    ss1 = requests.Session()
    website_url = web_url + "read.php?tid-" + str(tid) + ".html"
    response = ss1.get(website_url,headers=headers,cookies=cookies)
    if(response.status_code ==200):
        soup = BeautifulSoup(response.content,"html.parser")
        a_element = soup.select_one('a[title="只看楼主的所有帖子"]')
        href_value = a_element.get("href")
        new_url = web_url + href_value
        down_img(new_url)
    else:
        print(f"获取网页内容失败：{website_url}")

def down_img(new_url):
    ss1 = requests.Session()
    response = ss1.get(new_url,headers=headers,cookies=cookies)
    if(response.status_code == 200):
        soup = BeautifulSoup(response.content,"html.parser")
        title = soup.title.string.strip()
        sub_title = title.split(" - 南+")[0].strip()
        save_folder = save_folder+sub_title
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            img_src = img_tag["src"]
            print(img_src)
            img_url = urljoin(new_url,img_src)
            img_filename = os.path.basename(urlparse(img_url).path)
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                if check_string(img_filename):                   
                    img_filename = os.path.basename(urlparse(img_url).path)
                    save_path = os.path.join(save_folder,img_filename)
                    with open(save_path,"wb") as img_file:
                        img_file.write(img_response.content)
                    file_size = os.path.getsize(save_path)
                    if file_size < 100000:
                        os.remove(save_path)
                        print("太小了，不要\n")
                    else:
                        print(f"保存图片：{img_filename}\n")
            else:
                print(f"下载图片失败：{img_url}")
    else:
        print(f"获取网页内容失败：{new_url}")
                


def main():
    tid = input("tid plz:")
    find_url(tid)

if __name__ == '__main__':
    main()
#delete_small_files(save_folder)