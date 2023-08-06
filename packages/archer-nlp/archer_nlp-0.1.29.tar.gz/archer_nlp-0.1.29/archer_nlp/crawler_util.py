from urllib import request
from bs4 import BeautifulSoup
import requests

# content_type = 'application/json;charset=UTF-8'
content_type = 'application/json'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'

headers = [('Content-Type', content_type), ('User-Agent', user_agent)]
opener = request.build_opener()
opener.addheaders = headers
request.install_opener(opener)

requests_headers = {'Content-Type': content_type, 'User-Agent': user_agent}


# 常见流程
# 1、初始化bs：init_bs
# 2、用class name查找元素：find_element、find_elements、select_elements
# 3、获取元素内容：get_text、get_text_tag


def get_content(url):
    """
    获取页面内容
    :param url:
    :return:
    """
    # 如果慢的话，关闭代理。
    try:
        return request.urlopen(url).read().decode('UTF-8')
    except:
        # 上面的方法报错时调用
        return requests.get(url, headers=requests_headers).text


def init_bs(url):
    """
    初始化bs
    :param url:
    :return:
    """
    con = get_content(url)
    return BeautifulSoup(con, 'lxml')


def find_element(element, class_obj, class_name=''):
    """
    获取元素
    :param element:
    :param class_obj:
    :param class_name:
    :return:
    """
    return element.find(class_obj, attrs={'class': class_name})


def find_elements(element, class_obj, class_name=''):
    """
    获取多个元素
    :param element:
    :param class_obj:
    :param class_name:
    :return:
    """
    return element.find_all(class_obj, attrs={'class': class_name})


def select_elements(element, xpath_str):
    """
    使用xpath路径选择元素
    :param element:
    :param xpath_str:
    :return:
    """
    # element.select('div.short-field-item > div > p.short-field-title')
    return element.select(xpath_str)


def get_text(element):
    """
    获取文本内容（无HTML标签）
    :param element:
    :return:
    """
    return element.get_text().strip()


def get_text_tag(element):
    """
    获取带HTML标签（如<p>标签）的文本内容
    :param element:
    :return:
    """
    # element = find_element(soup, 'div', 'docYes')
    # get_text_tag(element).strip()
    return ''.join([str(ele) for ele in element.contents])
