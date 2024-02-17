import requests
from bs4 import BeautifulSoup

# def scrape_trending_repositories():
#     # 发送一个get请求到trending页面
#     response = requests.get('https://github.com/trending')
    
#     # 解析响应文本
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # 寻找所有的repo元素
#     repos = soup.find_all('article', class_='Box-row')
#     # with open('trending_repos.txt', 'w') as f:
#     #     f.write(str(repos))

#     # import pdb;pdb.set_trace()
#     # 打印每个repo的名字和链接
#     for repo in repos:
#         name_element = repo.find('h1', class_='h3 lh-condensed')
#         name = name_element.get_text(strip=True)
#         url = 'https://github.com/' + name_element.find('a')['href']
#         print(f'{name}: {url}')

def scrape_trending_repositories():
    response = requests.get('https://github.com/trending')
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = soup.find_all('article', class_='Box-row')

    for repo in repos:
        name_element = repo.find('h2', class_='h3 lh-condensed')
        
        # 检查 name_element 是否为 None
        if name_element:
            name = name_element.get_text(strip=True)
            url = 'https://github.com' + name_element.find('a')['href']
            print(f'{name}: {url}')
        else:
            print(f'Failed to find name for repository: {repo}')

scrape_trending_repositories()