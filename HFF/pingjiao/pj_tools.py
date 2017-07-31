import httplib2
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup


class PJAction:
    """This class-object will execute the action

    also offers some information, such handle progress
    """

    encoding = 'gbk'
    hidden_name = ''
    jwc_href = 'http://202.115.47.141/loginAction.do'
    main_href = 'http://202.115.47.141/jxpgXsAction.do?oper=listWj&totalrows=24&pageSize=200'
    pj_judge_href = 'http://202.115.47.141/jxpgXsAction.do'
    form_action_href = 'http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1)'
    }

    def extract(self, origin):
        """Extract each lesson's essential arguments, then
        return a list-object which contains all lessons' infomation
        """

        data = [ele.attrs['name'] for ele in origin]
        pattern = re.compile('(.*?)#@(.*?)#@(.*?)#@(.*?)#@(.*?)#@([0-9]+)', re.DOTALL)
        info = []
        for ele in data:
            temp = re.match(string=ele, pattern=pattern).groups()
            info.append({'wjbm': temp[0], 'bpr': temp[1], 'bprm': temp[2], 'wjmc': temp[3], 'pgnrm': temp[4], 'pgnr': temp[5], 'oper': 'wjShow'})
        return info

    def do_pj(self, html_content, h):
        """This function execute the physical pingjiao action

        More:
        1) firstly, it accepts the page with all lesson(this is list, exactly a table)
        2) using BeautifulSoup extract the table, and extract all images, these images resource redirect to the real information
        3) getting cleaned information by using extract function
        4) extract cookie-value, then use this cookie value to visit all pingjiao page
        5) pingjiao's action href is http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg, whose name is: form_action_href

        What next:
        * wrap the main part of this function with a try/except-clause
        * store the progress information, it is convinient for notify the front template
        """
        cleaned_info = []  # store the cleaned information of each lesson, by getting the return value of extract function
        soup = BeautifulSoup(html_content, 'html.parser')
        table_info = soup.find_all('table')[-2]
        table_info = table_info.find_all('img')  # table info
        input_hidden = soup.find_all('input')[-1]
        cleaned_info = self.extract(table_info)  # 格式：wjbm | bpr | bprm | wjmc | pgnrm | pgnr | oper='wjShow'

        self.hidden_name = input_hidden.attrs['name']

        data_for_teacher = {
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
            self.hidden_name: ''
        }

        data_for_ta = {
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
            self.hidden_name: ''
        }
        # print(cleaned_info)
        # main part
        for data in cleaned_info:
            r2, c2 = h.request(self.pj_judge_href, method='POST', headers=self.headers, body=urlencode(data))
            if r2['status'] == '200':
                result = c2.decode(self.encoding, 'ignore')
                soup_content = BeautifulSoup(result, 'html.parser')
                # 拿到评教页面的hidden value
                hidden_value_2 = soup_content.find('input', attrs={'name': 'wjbm', 'type': 'hidden'}).attrs['value']

                if data['wjmc'] == '学生评教':
                    data_for_teacher['wjbm'] = data['wjbm']
                    data_for_teacher['bpr'] = data['bpr']
                    data_for_teacher['pgnr'] = data['pgnr']
                    data_for_teacher[self.hidden_name] = hidden_value_2
                    r3, c3 = h.request(self.form_action_href, method='POST', headers=self.headers, body=urlencode(data_for_teacher, encoding=self.encoding))
                else:
                    data_for_ta['wjbm'] = data['wjbm']
                    data_for_ta['bpr'] = data['bpr']
                    data_for_ta['pgnr'] = data['pgnr']
                    data_for_ta[self.hidden_name] = hidden_value_2
                    r3, c3 = h.request(self.form_action_href, method='POST', headers=self.headers, body=urlencode(data_for_ta, encoding=self.encoding))
                print('{0}, {1}, {2} 评教完成！'.format(data['bprm'], data['wjmc'], data['pgnrm']))
            else:
                print('----失败：---')
                print(r2)

    def do_action(self, account, passwd):
        data = {'zjh': account, 'mm': passwd}
        h = httplib2.Http()
        r, c = h.request(self.jwc_href, method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
        soup = BeautifulSoup(c.decode('gbk'), 'html.parser')
        try:
            if soup.title.get_text() == '学分制综合教务':
                print('--> 身份验证成功！')
                pj_header = {'cookie': r['set-cookie'].split(';')[0]}
                self.headers['Cookie'] = pj_header['cookie']
                # 获取课程列表的连接
                r, c = h.request(self.main_href, headers=pj_header)
                html = c.decode(self.encoding)
                # do action
                if r['status'] == '200':
                    print('--> 成功获取所有课程信息!')
                    self.do_pj(html, h)
                    print('===Done!===')
            else:
                print('获取主页失败，确认你的用户名和密码！')
        except Exception as e:
            print(str(e))
