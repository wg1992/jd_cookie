import json
import time
import requests
import logging
requests.packages.urllib3.disable_warnings()


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

jd_ua = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5 UCBrowser/13.4.2.1122 TM/{0}'


def token_get():
    t = round(time.time())
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    }
    t = round(time.time())
    url = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
    res = s.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    s_token = res_json['s_token']
    token_post(s_token)
    # return s_token


def token_post(s_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s_token, t)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t)
        }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    qrurl = 'https://plogin.m.jd.com/cgi-bin/m/tmauth?client_type=m&appid=300&token={0}'.format(token)
    logger.info("请手动复制链接到在线二维码生成网站,并扫码登录")
    logger.info('')
    logger.info(qrurl)
    logger.info('')
    check_token(token, okl_token)


def check_token(token, okl_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua.format(t),
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    global i
    while code == 0:
        logger.info("扫码成功")
        jd_ck = s.cookies.get_dict()
        pt_key = 'pt_key=' + jd_ck['pt_key']
        pt_pin = 'pt_pin=' + jd_ck['pt_pin']
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        logger.info(ck)
        break
    else:
        i = i + 1
        if i < 60:
            logger.info(message)
            time.sleep(3)
            check_token(token, okl_token)
        else:
            exit(0)


if __name__ == '__main__':
    logger.info("Ver: 1.2.2 By: limoe 面板专用版本")
    logger.info("https://github.com/Zy143L/jd_cookie")
    logger.info("JD扫码获取Cookie")
    i = 1
    s = requests.session()
    token_get()
    exit(0)
