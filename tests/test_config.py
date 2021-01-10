# -*- coding: utf-8 -*-
"""
Created on 2021/1/10 21:37

@author: Irvinfaith

@email: Irvinfaith@hotmail.com
"""
import json

from tinyCrawl import Config

with open("../tinyCrawl/common/config.json", "w") as w:
    json.dump({
        "log_path": "./",
        "is_save_log": False,
        "checkpoint_dir_path": "./"
    }, w, ensure_ascii=False, indent="\t")

def test_set_config():
    config = Config()
    config.set("log_path", "./log")
    with open("../tinyCrawl/common/config.json", "r") as w:
        s = w.readlines()
        config_dict = json.loads(''.join([i.strip() for i in s]))
    assert config_dict["log_path"] == "./log"


def test_get_config():
    config = Config()
    log_path = config["log_path"]
    with open("../tinyCrawl/common/config.json", "r") as w:
        s = w.readlines()
        config_dict = json.loads(''.join([i.strip() for i in s]))
    assert config_dict["log_path"] == log_path
