import requests  # 导入requests库，用于发送HTTP请求
from bs4 import BeautifulSoup  # 导入BeautifulSoup库，用于解析HTML内容
import re  # 导入re库，用于正则表达式匹配
import os  # 导入os库，用于文件操作
from urllib.parse import urlparse  # 导入urlparse，用于提取域名

# 目标URL列表，包含要从中提取IP地址的网页
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz',
    'https://cf.090227.xyz',
    'https://www.wetest.vip/page/cloudfront/address_v4.html',
    'https://www.wetest.vip/page/cloudflare/address_v4.html',  # 已修正URL
    'https://www.wetest.vip/page/cloudfront/address_v6.html',
    'https://www.wetest.vip/page/cloudflare/address_v6.html'  # 已修正URL
]

# 正则表达式用于匹配IPv4地址
ipv4_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
# 正则表达式用于匹配IPv6地址 (更健壮的版本)
ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:))'

# 存储提取的IP地址的列表，用于去重和编号
unique_ips = []

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 自动编号计数器
counter = 1

# 循环遍历每个URL
for url in urls:
    try:  # 添加错误处理，以应对网络问题
        # 发送HTTP请求获取网页内容，并设置超时时间为10秒
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果响应状态码不是200，则抛出HTTPError异常

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取域名
        parsed_uri = urlparse(url)
        domain = parsed_uri.netloc

        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        elif url == 'https://cf.090227.xyz':
            elements = soup.find_all('tr')
        elif "wetest.vip" in url:
            elements = soup.find_all('tr')
            # 针对 wetest.vip 网站的特殊处理，提取 IPv6 地址
            for element in elements:
                td_element = element.find('td', {'data-label': '优选地址'})
                if td_element:
                    ipv6_text = td_element.get_text().strip()
                    if re.match(ipv6_pattern, ipv6_text):
                        formatted_ip = f"{ipv6_text} #{counter:03d}.IPv6.{domain}"
                        if formatted_ip not in unique_ips:
                            unique_ips.append(formatted_ip)
                            counter += 1
        else:
            elements = soup.find_all('li')

        # 遍历所有元素，查找IP地址
        for element in elements:
            element_text = element.get_text()

            # 查找IPv4地址
            ipv4_matches = re.findall(ipv4_pattern, element_text)
            for ip in ipv4_matches:
                formatted_ip = f"{ip} #{counter:03d}.IPv4.{domain}"
                if formatted_ip not in unique_ips:
                    unique_ips.append(formatted_ip)
                    counter += 1

            # 查找IPv6地址
            ipv6_matches = re.findall(ipv6_pattern, element_text)
            for match in ipv6_matches:
                if isinstance(match, tuple):
                    ip = match[0]  # 假设第一个捕获组是 IP 地址
                else:
                    ip = match
                formatted_ip = f"{ip} #{counter:03d}.IPv6.{domain}"
                if formatted_ip not in unique_ips:
                    unique_ips.append(formatted_ip)
                    counter += 1

    except requests.exceptions.RequestException as e:
        print(f"抓取 {url} 时发生错误: {e}")  # 打印错误信息
    except Exception as e:
        print(f"处理 {url} 时发生未知错误: {e}")

# 将去重后的IP地址写入文件
with open('ip.txt', 'w') as file:
    for ip in sorted(unique_ips):  # 排序后再写入
        file.write(ip + '\n')

print('IP地址已保存到ip.txt文件中，已去重并添加IPv4/IPv6标识、域名和编号。')
