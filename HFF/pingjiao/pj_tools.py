import httplib2
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup


def extract(origin):
    print('test')
    data = [ele.attrs['name'] for ele in origin]
    pattern = re.compile('(.*?)#@(.*?)#@(.*?)#@(.*?)#@(.*?)#@([0-9]+)', re.DOTALL)
    info = []
    for ele in data:
        temp = re.match(string=ele, pattern=pattern).groups()
        info.append({'wjbm': temp[0], 'bpr': temp[1], 'bprm': temp[2], 'wjmc': temp[3], 'pgnrm': temp[4], 'pgnr': temp[5], 'oper': 'wjShow'})
    return info


def do_pj(html_content, h, url_pj, cookie):
    # h = httplib2.Http()
    cleaned_info = []
    soup = BeautifulSoup(html_content, 'html.parser')
    table_info = soup.find_all('table')[-2].find_all('img')  # table info
    input_hidden = soup.find_all('input')[-1]
    # print(table_test)

    cleaned_info = extract(table_info)  # 格式：wjbm | bpr | bprm | wjmc | pgnrm | pgnr | oper='wjShow'

    hidden_name = input_hidden.attrs['name']
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)'
    }

    data_std = {
        '0000000005': '10_1',
        '0000000006': '10_1',
        '0000000007': '10_1',
        '0000000008': '10_1',
        '0000000009': '10_1',
        '0000000010': '10_1',
        '0000000035': '10_1',
        'zgpj': '认真负责，气氛活跃！',
        'wjbm': '',
        'bpr': '',
        'pgnr': '',
        hidden_name: ''
    }

    data_std2 = {
        '0000000028': '10_1',
        '0000000029': '10_1',
        '0000000030': '10_1',
        '0000000031': '10_1',
        '0000000032': '10_1',
        '0000000033': '10_1',
        'zgpj': '认真负责，气氛活跃！',
        'wjbm': '',
        'bpr': '',
        'pgnr': '',
        hidden_name: ''
    }
    # 显示评教页面的url
    url_dest = 'http://202.115.47.141/jxpgXsAction.do'
    # table_info = tables[-2].find_all('img')  # table info

    # DO ACTION
    for data in cleaned_info:

        r2, c2 = h.request(url_dest, method='POST', headers=headers, body=urlencode(data))

        if r2['status'] == '200':
            result = c2.decode('gbk', 'ignore')
            soup_content = BeautifulSoup(result, 'html.parser')
            # 拿到评教页面的hidden value
            hidden_value_2 = soup_content.find('input', attrs={'name': hidden_name, 'type': 'hidden'}).attrs['value']

            if data['wjmc'] == '学生评教':
                data_std['wjbm'] = data['wjbm']
                data_std['bpr'] = data['bpr']
                data_std['pgnr'] = data['pgnr']
                data_std[hidden_name] = hidden_value_2
                r3, c3 = h.request('http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg', method='POST', headers=headers, body=urlencode(data_std, encoding='gbk'))
            else:
                data_std2['wjbm'] = data['wjbm']
                data_std2['bpr'] = data['bpr']
                data_std2['pgnr'] = data['pgnr']
                data_std2[hidden_name] = hidden_value_2
                r3, c3 = h.request('http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg', method='POST', headers=headers, body=urlencode(data_std2, encoding='gbk'))
            print('{0}, {1}, {2} 评教完成！'.format(data['bprm'], data['wjmc'], data['pgnrm']))
        else:
            print('----失败：---')
            print(r2)


def do_action(account, passwd):
    url_main = 'http://202.115.47.141/loginAction.do'
    data = {'zjh': account, 'mm': passwd}
    h = httplib2.Http()
    r, c = h.request(url_main, method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    soup = BeautifulSoup(c.decode('gbk'), 'html.parser')
    try:
        if soup.title.get_text() == '学分制综合教务':
            print('--> 身份验证成功！')
            pj_header = {'cookie': r['set-cookie'].split(';')[0]}
            # 获取课程列表的连接
            # url_pj = 'http://202.115.47.141/jxpgXsAction.do?oper=listWj&totalrows=24&pageSize=200'
            # r, c = h.request(url_pj, headers=pj_header)
            # html = c.decode('gbk')
            # # do action
            # if r['status'] == '200':
            #     print('--> 成功获取所有课程信息!')
            #     do_pj(html, h, url_pj, pj_header['cookie'])
            #     print('===Done!===')
        else:
            print('获取主页失败，确认你的用户名和密码！')
    except Exception as e:
        print(str(e))
