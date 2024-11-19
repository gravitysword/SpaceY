from playwright.sync_api import sync_playwright
import json,os

platform = {
}
'''
 "zhihu" : "https://www.zhihu.com/",
    "bili" : "https://www.bilibili.com/",
    "kuaishou": "https://www.kuaishou.com/"
"douyin" : "https://www.douyin.com/",
    #"toutiao": "https://www.toutiao.com/"
    #"weibo": "https://weibo.cn/"'''
def login():
    os.system('python -m playwright install chromium')
    with sync_playwright() as p:
        with open('config.json', 'r') as f:
            config = json.loads(f.read())

        # 启动浏览器，并设置 headless=False 显示界面
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        for i in platform:

            page.goto(platform[i])
            input("登陆成功后，点击继续")
            main_cookies = page.context.cookies()
            config['cookies'][i] = main_cookies,


            with open('config.json', 'w') as f:
                f.write(json.dumps(config, indent=4))

        # 关闭浏览器
        browser.close()
        input("Press any key to continue...")


if __name__ == '__main__':
    login()
