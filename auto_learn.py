from selenium import webdriver
import datetime
import time


def is_element_exist(x_path):
    """
    判断元素是否存在
    :param x_path:组件的full_x_path
    :return:存在/不存在
    """
    flag = True
    try:
        browser.find_element_by_xpath(x_path)
    except:
        flag = False
    finally:
        return flag


def auto_learn(browser):
    """
    自动挂课主程序
    使用方法：
    1.执行python脚本
    2.登录系统
    3.打开学习视频，关闭其他标签页
    4.视频播放完毕后，打开其他视频，并关闭其他标签页
    :param browser:chrome的句柄
    :return:none
    """
    login_url = "https://rs.jshrss.jiangsu.gov.cn/web/login?appId=202107150001&returnUrl=https%3A%2F%2Fm.mynj.cn%3A11097%2Fplateform%2FrediectIndex%2Fgoods"
    video_full_xpath = "/html/body/table[2]/tbody/tr/td[1]/div[3]/div/video"
    browser.get(login_url)

    time.sleep(100)

    cur_handle = 0
    while(True):
        # 先判断页面有没有改变，改变了则自动切到最后一个页面
        # to do：chrome新打开多个标签页后，handle顺序似乎不是按打开顺序排列的，所以现在还需要手动关闭其他标签页
        windows = browser.window_handles
        if windows[-1] != cur_handle:
            cur_handle = windows[-1]
            print("页面已改变，切换到新页面...")
            browser.switch_to.window(cur_handle)

        # 当视频在播放时，每隔一段时间暂停/恢复一次，防止自动暂停
        if is_element_exist(video_full_xpath):
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("{} 我要点窗口了！".format(cur_time))
            video = browser.find_element_by_xpath(video_full_xpath)
            video.click()# 点一下暂停
            time.sleep(0.1)
            video.click()# 再点一下恢复

        time.sleep(300)# 每300秒轮询一次


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.maximize_window()

    auto_learn(browser)


