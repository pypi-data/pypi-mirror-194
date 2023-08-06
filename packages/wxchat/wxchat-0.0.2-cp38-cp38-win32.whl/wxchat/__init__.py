import time, json, logging, threading, re
from .log import set_logging
from weixin_client_python import WeixinClient
import xmltodict

logger = logging.getLogger('wechat')

TEXT = 0x01
PICTURE = 0x03
VOICE = 0x22
CARD = 0x2A
ARTICLE = 0x1F
SYSTEM = 0x2710


class TryAgain(RuntimeError): ...


class WechatHelper(WeixinClient):

    def __init__(self, ip="127.0.0.1", port1=10086, port2=10010):
        super().__init__(ip, port1, port2)
        self.running = True
        self.logging = False
        self.self_info = None
        self.func_dict = dict()

    def wait_until_login(self):
        if self.logging:
            logger.info("already logging")
            return
        self.logging = True
        while not self.is_login():
            time.sleep(1)
        self.logging = False
        return self.get_self_info()

    def add_friend_by_wxid(self, wxid: str, remark: str = ""):
        self.add_friend(3, wxid, remark)

    def add_friend_by_mobile(self, mobile: str, remark: str = ""):
        def stranger(topic, payload):
            self.add_friend(15, payload["v3"], remark)
            self.remove_listener("stranger", stranger)

        self.register_listener("stranger", stranger)
        self.find_stranger(mobile)

    def get_chatroom_list(self):
        friends = self.get_friend_list()
        return [friend for friend in friends if "@chatroom" in friend.wxid]

    def clear_listener(self, endpoint):
        self.func_dict[endpoint] = []

    def remove_listener(self, endpoint, func):
        if endpoint in self.func_dict:
            self.func_dict[endpoint].remove(func)

    def register_listener(self, endpoint, func):
        if endpoint not in self.func_dict:
            self.func_dict[endpoint] = []

        if func not in self.func_dict[endpoint]:
            self.func_dict[endpoint].append(func)

    def listen(self, endpoint):
        def register(func):
            self.register_listener(endpoint, func)

        return register

    def message(self, endpoint: str, msgtype=[CARD, TEXT, PICTURE, VOICE, ARTICLE, SYSTEM], keywords=[], atuserlist=[],
                filter_self_send=True):
        if not endpoint.startswith("chat"):
            raise Exception("unknown topic!")
        if not (isinstance(msgtype, list) or isinstance(msgtype, tuple)):
            msgtype = [msgtype]

        if not (isinstance(keywords, list) or isinstance(keywords, tuple)):
            keywords = [keywords]

        if not (isinstance(atuserlist, list) or isinstance(atuserlist, tuple)):
            atuserlist = [atuserlist]

        def register(func):
            if endpoint not in self.func_dict:
                self.func_dict[endpoint] = []

            def func_proxy(topic, payload):
                if int(payload["type"], 16) not in msgtype:
                    return

                if filter_self_send and int(payload["is_self_send"]) == 1:
                    return

                if keywords and len(keywords) and payload["content"]:
                    flag = True

                    for keyword in keywords:
                        if re.search(keyword, payload["content"]):
                            flag = False

                    if flag:
                        return

                if atuserlist and len(atuserlist) and payload["source"]:
                    source = xmltodict.parse(payload["source"])
                    if not source or "msgsource" not in source or "atuserlist" not in source["msgsource"]:
                        return

                    flag = True
                    for item in atuserlist:
                        if item in source["msgsource"]["atuserlist"]:
                            flag = False
                    if flag:
                        return

                func(topic, payload)

            self.func_dict[endpoint].append(func_proxy)
            return func_proxy

        return register

    def recv_data(self):
        message = self.recieve_message(1)
        if message and ":" in message:
            logger.debug("recv_data:%s", message)
            topic, payload = message.split(":", 1)
            return topic, json.loads(payload)
        raise TryAgain

    def terminate(self):
        self.running = False

    def run_forever(self, debug=False, block=True):
        def main_loop():
            if debug:
                set_logging(loggingLevel=logging.DEBUG)

            logger.info("start receive message...")
            self.subscribe("")  # 订阅所有消息
            while self.running:
                try:
                    topic, payload = self.recv_data()
                    for endpoint in self.func_dict:
                        if re.match(endpoint, topic):
                            callback_func = self.func_dict[endpoint]
                            for func in callback_func:
                                func(topic, payload)

                except TryAgain:
                    continue
                except KeyboardInterrupt:
                    logger.debug('received ^C and exit.')
                    logger.info('Bye~')
                    break
            self.unsubscribe("")

        if block:
            main_loop()
        else:
            thread = threading.Thread(target=main_loop)
            thread.setDaemon(True)
            thread.start()
