import time 
import requests
from bs4 import BeautifulSoup
import json

def scrape_trending_repositories():
    response = requests.get('https://github.com/trending')
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = soup.find_all('article', class_='Box-row')

    readme_dict = {}

    for repo in repos:
        name_element = repo.find('h2', class_='h3 lh-condensed')
        
        # 检查 name_element 是否为 None
        if name_element:
            name = name_element.get_text(strip=True)
            url = 'https://github.com' + name_element.find('a')['href']
            

            language_element = repo.find('span', itemprop='programmingLanguage')
            language = language_element.get_text(strip=True) if language_element else 'Not specified'

            time.sleep(1)
            readme_url = url.replace('https://github.com', 'https://raw.githubusercontent.com') + '/master/README.md'
            readme_response = requests.get(readme_url)
            if readme_response.status_code == 200:
                readme_dict[name] = readme_response.text
            else:
                print(f'Failed to get README for {name}')

            print(f'{name}: {url}, Main language: {language}')
        else:
            print(f'Failed to find name for repository: {repo}')
    
    with open('readme_summaries.txt', 'w') as f:
        for repo_name, readme in readme_dict.items():
            url = 'https://github.com' + name_element.find('a')['href']
            language_element = repo.find('span', itemprop='programmingLanguage')
            language = language_element.get_text(strip=True) if language_element else 'Not specified'

            summary_line = f'{repo_name}: {url}, Main language: {language} '
            f.write(summary_line)

            url_gemini = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + YOUR_API_KEY
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": "请用中文一句话总结这个repository的README:" + readme[:500]
                            }
                        ]
                    }
                ]
            }
            try:
                response = requests.post(url_gemini, headers=headers, data=json.dumps(data))
                response.raise_for_status()  # 如果请求失败，这会引发 HTTPError 异常
                summary = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                f.write('Summary: ' + summary + '\n\n')
            except requests.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                f.write('Summary: HTTP error occurred\n\n')
            except Exception as err:
                print(f'Other error occurred: {err}')
                f.write('Summary: Other error occurred\n\n')

YOUR_API_KEY = 'AIzaSyAbP0mbJUbWTqKyeRRrSngfkIUPSRWMDgI'
readme_dict = scrape_trending_repositories()