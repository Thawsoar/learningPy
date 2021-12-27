#-*- coding: UTF-8 -*- 

import requests
import json
import re
import time


class ZentaoCli(object):
    session = None   # 用于实现单例类，避免多次申请sessionID
    sid = None
    userList = None
    buildBranchList = None

    def __init__(self, url, account, password, override=False):
        self.url = url
        self.account = account   # 账号
        self.password = password   # 密码
        self.override = override    # 是否覆盖原会话
        self.pages = {
            "login": "/user-login.html",  # 登录的接口
            "get_session_id": "/api-getsessionid.json",  # 获取sessionId sessionName
            "my_bug": "/my-bug.json",  # 获取bug列表 json
            "my_bug_html": "/my-bug.html",  # 获取bug列表 html
            "user_list": "/company-browse-1-bydept-id-62-100-1.json",  # 获取研发部成员列表
            "bug_detail": "/bug-view-{}.json",  # bug 详情
            "bug_detail_html": "/bug-view-{}.html",  # bug 详情的 uid  服了， 这Tmd设计的什么鬼神api
            "resolve_bug": "/bug-resolve-{}.html?onlybody=yes",  # 解决bug
            "build_branch": '/project-build-220-42.json',  # 跨运管家版本分支
            'file_read': '/file-read-{}',  # 文件读取
        }
        self.s = None
        self.sid = None

    # 获取api地址
    def get_api(self, api_name, **args):
        return self.url.rstrip("/") + self.pages[api_name]

    @staticmethod
    def req(self, url):
        web = self.s.get(url)
        if web.status_code == 200:
            resp = json.loads(web.content)
            if resp.get("status") == "success":
                return True, resp
            else:
                return False, resp

    # 登录
    def login(self):
        if self.s is None:
            if not self.override and ZentaoCli.session is not None:
                self.s = ZentaoCli.session
            else:
                # 新建会话
                self.s = requests.session()
                print(self.url)
                res, resp = self.req(self, self.url.rstrip("/") + self.pages['get_session_id'])
                print(res, resp)
                if res:
                    print("获取sessionID成功")
                    self.sid = json.loads(resp["data"])["sessionID"]
                    ZentaoCli.sid = self.sid
                    login_res = self.s.post(
                        url=self.url.rstrip("/") + self.pages["login"],
                        params={'account': self.account, 'password': self.password, 'sid': self.sid}
                    )
                    if login_res.status_code == 200:
                        print("登录成功")
                        ZentaoCli.session = self.s

    # bug分支版本列表
    def get_build_branch(self):
        if ZentaoCli.buildBranchList is None or self.override:
            req_url = self.get_api("build_branch")
            query_data = self.s.get(req_url).json()
            json_query_data = json.loads(query_data['data'])
            # print(json_query_data)
            build_branch_list = []
            build_branch_map = {}
            for item in json_query_data['projectBuilds']['42']:
                build_branch_list.append({
                    'name': item['name'],
                    'id': item['id'],
                    'builder': item['builder'],
                })
                build_branch_map[item['name']] = item['id']
            if build_branch_map is not None:
                ZentaoCli.buildBranchList = build_branch_list
            print('fetch branch list')
            return build_branch_list, build_branch_map
        else:
            build_branch_map = {}
            for item in ZentaoCli.buildBranchList:
                build_branch_map[item['name']] = item['id']
            print('local branch list')
            return ZentaoCli.buildBranchList, build_branch_map

    # 用户列表
    def get_user_list(self):
        if ZentaoCli.userList is None or self.override:
            req_url = self.get_api("user_list")
            query_data = self.s.get(req_url).json()
            json_query_data = json.loads(query_data['data'])
            json_query_data['users'].extend([
                {
                    'id': '0',
                    'account': 'liya.lei',
                    'realname': '雷雅丽',
                },
                {
                    'id': '1',
                    'account': 'joyce.zhang',
                    'realname': '张晶',
                },
                {
                    'id': '2',
                    'account': 'skinny.li',
                    'realname': '李清娴',
                },
                {
                    'id': '2',
                    'account': 'june.chu',
                    'realname': '储君',
                },
            ])
            user_list = []
            user_map = {}
            for item in json_query_data['users']:
                user_list.append({
                    'id': item['id'],
                    'account': item['account'].lower(),
                    'realname': item['realname'],
                })
                user_map[item['account']] = item['realname']
            if user_map is not None:
                ZentaoCli.userList = user_list
            print('fetch user list')
            return user_list, user_map
        else:
            user_map = {}
            for item in ZentaoCli.userList:
                user_map[item['account']] = item['realname']
            print('local user list')
            return ZentaoCli.userList, user_map

    # 获取bug列表
    def get_my_bug(self):
        req_url = self.get_api('my_bug')
        query_data = self.s.get(req_url).json()
        json_query_data = json.loads(query_data['data'])
        bug_list = []
        user_list, user_map = self.get_user_list()

        for item in json_query_data['bugs']:
            match_img_list = re.findall('\{(.*?)\}', item['steps'])
            quicklookurl = []
            if len(match_img_list):
                quicklookurl = self.url.rstrip("/") + self.pages["file_read"].format(match_img_list[0]),

            bug_list.append({
                'uid': item['id'],
                'title': '{}（{}）'.format(item['id'], user_map[item['openedBy'].lower()]),
                'subtitle': item['title'],
                'arg': self.get_api("bug_detail_html").format(item['id']),
                'valid': True,
                'quicklookurl': '' if not quicklookurl else quicklookurl[0]
            })
        first_item = {
            'uid': '-1',
            'title': '淦，还有{}个bug'.format(len(bug_list)),
            'subtitle': '加油改吧💪🏻',
            'arg': self.pages['my_bug_html'],
            'valid': True,
        }
        if len(bug_list) == 0:
            first_item['title'] = '🐂 木有bug啦'
            first_item['subtitle'] = '划水去 👻'
        bug_list.insert(0, first_item)
        return bug_list

    # 获取bug 详情
    def get_bug_detail(self, bug_id):
        req_url = self.get_api("bug_detail").format(bug_id)
        query_data = self.s.get(req_url).json()
        json_query_data = json.loads(query_data['data'])
        return json_query_data

    # 解析html获取bug详情的 uid
    def get_bug_uid(self, bug_id):
        req_url = self.get_api("bug_detail_html").format(bug_id)
        res = self.s.get(req_url)
        res.encoding = 'utf-8'    # 使用utf-8对内容编码
        if res.status_code == 200:
            html = res.content.decode()
            uid = re.findall('var kuid = \'(.*?)\'', html)
            return uid[0]
        else:
            return None

    # 解决bug
    def resolve_bug(self, bug_id, *arg):
        uid = self.get_bug_uid(bug_id)
        req_url = self.get_api("resolve_bug").format(bug_id)
        print(req_url)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # build_branch_list, build_branch_map = self.get_build_branch()
        json_query_data = self.get_bug_detail(bug_id)
        print(json_query_data)
        bug_detail = json_query_data['bug']
        builds_detail = json_query_data['builds']
        users_detail = json_query_data['users']
        print(users_detail)
        print(bug_detail)
        params = {
            'resolution': 'fixed',
            'uid': uid,
            'resolvedDate': now_time,
            'assignedTo': bug_detail['openedBy'],  # 默认指给提出bug的测试人员
            'resolvedBuild': bug_detail['openedBuild'],  # 解决版本的分支id
            'comment': '--- commit comment by Alfred4 Workflow ---',
        }
        print(params)
        res = self.s.post(req_url, params)
        if res.status_code == 200:
            print('✅ bug #{} 已点解决 by {}'.format(bug_id, now_time))
        else:
            print('淦，bug #{} 没点掉 by {}'.format(bug_id, now_time))


if __name__ == "__main__":
    cli = ZentaoCli("http://chandao.hgj.net/zentao", "taoxiang.tao", "Tx~12138", override=False)
    cli.login()
    cli.get_user_list()
    cli.get_build_branch()
    cli.get_my_bug()
    cli.resolve_bug(10681)

