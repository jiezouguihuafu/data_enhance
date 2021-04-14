import json,time,os,logging,re,urllib, hashlib, http.client,random,codecs,tqdm


# 把翻译的结果通过日志的方式存到txt文本中
logging.basicConfig(level=logging.INFO,
                    # format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    # datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.txt',
                    filemode='w'
                    )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def clean_text(text:str):
    div = "src|class|style|href|url|hide|alt"
    rule = re.compile(r'(http[:0-9a-zA-Z\\/=@#$%&.?\-<>()~^{}+_]+)|((src|class|style|href|url|hide|alt|color)=(["“\']).*?(["“\']))')
    text = re.sub(rule,"",text)
    return text.strip()


def baidu_translate(word: str,fromLang:str,toLang:str) -> str:
    """
    调用百度翻译接口
    :param word:
    :return:
    """
    appid = '20200427000431686'  # 填写你的appid
    secretKey = 'IKOU2eUShurv01TYJmAG'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    # fromLang = 'auto'  # 原文语种
    # toLang = "zh"  # 译文语种
    salt = random.randint(32768, 65536)
    q = word
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)['trans_result'][0]['dst']
        time.sleep(1)
        return result

    except Exception as e:
        return ""
    finally:
        if httpClient:
            httpClient.close()


def zh_to_en(word):
    return baidu_translate(word,"zh","en")


def en_to_zh(word):
    return baidu_translate(word,"en","zh")


def sentence_trans(text):
    en = zh_to_en(text)
    print(en)
    zh = en_to_zh(en)
    print(zh)
    return zh



if __name__ == '__main__':
    sentence = "你最喜欢的人是我吗？"
    resu = sentence_trans(sentence)

