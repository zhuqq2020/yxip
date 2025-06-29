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
# 正则表达式用于匹配IPv6地址 (更健壮的版本)
ipv6_pattern = r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
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
                    file.write(ip + '\n')  # 强制转换为字符串

                # 查找IPv6地址
                ipv6_matches = re.findall(ipv6_pattern, element_text)
                for match in ipv6_matches:
                    # 确保 match 是一个字符串。如果 re.findall 返回一个元组，
                    # 说明你的正则表达式有多个捕获组。你需要选择哪个组
                    # 包含你想要的 IP 地址。 在这里，我们假设第一个组包含 IP 地址
                    if isinstance(match, tuple):
                        ip = match[0]  # 假设第一个捕获组是 IP 地址
                    else:
                        ip = match  # 如果不是元组，直接使用匹配项
                    file.write(ip + '\n') # 直接写入，因为已经确保了是字符串

        except requests.exceptions.RequestException as e:
            print(f"抓取 {url} 时发生错误: {e}")  # 打印错误信息
        except Exception as e:
            print(f"处理 {url} 时发生未知错误: {e}")

print('IP地址已保存到ip.txt文件中。')
