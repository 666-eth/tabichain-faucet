import os
import random
import string
import time

from loguru import logger

import requests


def get_proxy(nstproxy_channel="XXX", nstproxy_password="XXX"):
    session = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(10))
    return f"http://{nstproxy_channel}-residential-country_ANY-r_5m-s_{session}:{nstproxy_password}@gw-us.nstproxy.com:24125"


def parse_txt_file(file_path):
    if not os.path.exists(file_path):
        logger.error(f"file '{file_path}' not found.")
        exit(1)
    with open(file_path, 'r', encoding='utf-8') as file:
        datas = file.readlines()

    datas = [data.strip() for data in datas if data.strip()]
    if len(datas) == 0:
        raise Exception("file data not found.")
    return datas


if __name__ == '__main__':
    address_list = parse_txt_file("./add.txt")
    for address in address_list:
        logger.info(f"加载钱包：{address}  .....")
        try:

            proxy_url = get_proxy()
            proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }
            data = {
                "address": address.strip()
            }
            url = f"https://faucet-api.testnet.tabichain.com/api/faucet"
            resp = requests.post(url=url, json=data, proxies=proxies , timeout=30)
            resp.raise_for_status()
            if resp.ok:
                resp_text = resp.text

                if "success" in resp_text:
                    tx_id = resp_text.split(" ")[0]
                    logger.success(
                        f"地址：{address} 领取成功，txId：{tx_id}")
                    continue
                logger.error(f"地址：{address} 领取失败，原因：{resp_text}")
            else:
                logger.error(f"地址：{address} 发送领取请求失败，原因: {resp.text}")
        except Exception as e:
            logger.error(f"发生异常：{e}")

