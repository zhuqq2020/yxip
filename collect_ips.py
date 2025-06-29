import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://api.uouin.com/cloudflare.html', 
        'https://ip.164746.xyz',
        'https://vps789.com/cfip',
        'https://cf.090227.xyz',
        'https://www.wetest.vip/page/cloudfront/address_v4.html',
        'https://www.wetest.vip/page/cloudflare/address_v4.html'
        ]

# 正则表达式用于匹配IP地址
ipv4_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ipv6_pattern = r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)'  # More robust IPv6 regex

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
            
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        elif url == 'https://vps789.com/cfip':
            elements = soup.find_all('li')
        else:
            elements = soup.find_all('tr')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ipv4_matches = re.findall(ip_pattern, element_text)
            for ip in ipv4_matches:
                file.write(ip + '\n')
            ipv6_matches = re.findall(ipv6_pattern, element_text)
            for ip in ipv6_matches:
                file.write(ip + '\n')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")                 
              
print('IP地址已保存到ip.txt文件中。')
