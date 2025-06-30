import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML内容
import re  # 导入re库，用于正则表达式匹配
import os  # 导入os库，用于文件操作

# 目标URL列表，包含要从中提取IP地址的网页
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz',
    'https://vps789.com/cfip/',
    'https://cf.090227.xyz',
    'https://www.wetest.vip/page/cloudfront/address_v4.html',
    'https://www.wetest.vip/page/cloudflare/address_v4.html',  # 已修正URL
    'https://www.wetest.vip/page/cloudfront/address_v6.html',
    'https://www.wetest.vip/page/cloudflare/address_v6.html'  # 已修正URL
]

# 正则表达式用于匹配IPv4地址
ipv4_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 改进后的正则表达式用于匹配IPv6地址 (更精确的版本)
ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'

# 存储提取的IP地址的集合，用于去重
unique_ips = set()

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 循环遍历每个URL
for url in urls:
    try:  # 添加错误处理，以应对网络问题
        # 发送HTTP请求获取网页内容，并设置超时时间为10秒
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError异常

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        elif url == 'https://vps789.com/cfip/':  # 针对vps789.com网站的特殊处理
            elements = soup.find_all('tr')  # 该网站使用<li>标签
        elif url == 'https://cf.090227.xyz':
            elements = soup.find_all('tr')
        elif "wetest.vip" in url:
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')

        # 遍历所有元素，查找IP地址
        for element in elements:
            element_text = element.get_text()

            # 查找IPv4地址
            ipv4_matches = re.findall(ipv4_pattern, element_text)
            for ip in ipv4_matches:
                unique_ips.add(ip)  # 添加到集合，自动去重

            # 查找IPv6地址
            ipv6_matches = re.findall(ipv6_pattern, element_text)
            for ip in ipv6_matches:
                unique_ips.add(ip)  # 添加到集合，自动去重

    except requests.exceptions.RequestException as e:
        print(f"抓取 {url} 时发生错误: {e}")  # 打印错误信息
    except Exception as e:
        print(f"处理 {url} 时发生未知错误: {e}")

# 将去重后的IP地址写入文件
with open('ip.txt', 'w') as file:
    for ip in sorted(unique_ips):  # 排序后再写入
        file.write(ip + '\n')

print('IP地址已保存到ip.txt文件中，已去重。')
