# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 10:42
# @Author  : abo123456789
# @Desc    : free_chatgpt.py
import requests
import retrying
from requests import ReadTimeout


def retry_if_timeout_error(excep):
    return isinstance(excep, ReadTimeout)


class FreeChatgpt(object):

    @staticmethod
    def ask(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=4, stop_max_delay=100000,
                            wait_fixed=1500, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                url = f'https://api.wqwlkj.cn/wqwlapi/chatgpt.php?msg={question.strip()}&type=json'
                print('AI问题思考中=====')
                res = requests.get(url, timeout=25).json()
                print('AI问题回答完成===')
                del res['info']
                return res

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


if __name__ == '__main__':
    r = FreeChatgpt.ask(question='帮我创作一个广告视频宣传跨境选品SAAS？')
    print(r)
    t = FreeChatgpt.ask(question='帮我创作一个广告视频宣传华为mate手机卖点？')
    print(t)

