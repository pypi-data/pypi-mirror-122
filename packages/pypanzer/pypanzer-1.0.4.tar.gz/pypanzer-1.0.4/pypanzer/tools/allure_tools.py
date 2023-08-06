# -*- coding: utf-8 -*-

import os
import platform
import re
import shutil
import subprocess
import time
from subprocess import CalledProcessError

from loguru import logger


def run_command(command):
    system = platform.system()
    if system == 'Linux':
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    elif system == "Darwin":
        subprocess.run("source ~/.bash_profile && " + str(command), shell=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
    elif system == 'Windows':
        windows_command = ['cmd', '/c']
        command_detail_list = re.split(r"[ ]+", command)
        windows_command.extend(command_detail_list)
        subprocess.run(windows_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    else:
        raise RuntimeError


class AllureTools(object):
    """
    Allure测试报告操作类
    """

    def __init__(self, result_path, report_path, resource_path=None):
        """
        初始化Allure
        :param result_path: Allure结果文件目录
        :param report_path: Allure报告文件目录
        :param resource_path: Allure外部资源文件目录（即environment.properties及categories.properties所在目录）
        """
        self._ALLURE_RESULT = result_path
        self._ALLURE_REPORT = report_path
        self._RESOURCE_PATH = resource_path

    def check_result(self, check_count=3):
        """
        检查Allure测试结果json文件是否生成。
        :param check_count: 检测次数（默认为3）。
        :return:
        """
        check_result = None
        for count in range(check_count):
            if os.listdir(self._ALLURE_RESULT) == list() and count < check_count:
                if count == check_count - 1:
                    logger.warning("仍未检测到Allure测试结果json文件，已达检测次数上限({})，停止检测。".format(check_count))
                    check_result = False
                    break
                logger.warning("未检测到Allure测试结果json文件，可能正在生成......")
                time.sleep(2)
                continue
            if os.listdir(self._ALLURE_RESULT) != list():
                logger.info("[Success]：已检测到Allure测试结果json文件.")
                check_result = True
                break
        return check_result

    def generate_report(self):
        """
        根据json结果文件自动生成Allure测试报告。
        """
        try:
            if self.check_result() is True:
                command = "allure generate {0} -o {1} --clean".format(self._ALLURE_RESULT, self._ALLURE_REPORT)
                time.sleep(1)
                logger.info('开始执行Allure测试报告生成命令："{}"'.format(command))
                run_command(command)
                logger.info("[Done]：已经成功生成Allure测试报告.")
            else:
                logger.warning("[Warning]：由于未检测到Allure测试结果json文件，停止生成Allure测试报告！")
        except CalledProcessError:
            logger.exception("[Exception]：Allure测试报告生成命令执行失败！")
        except Exception:
            logger.exception("[Exception]：生成Allure测试报告过程中发生异常，请检查！")

    def clear_result(self):
        """
        清空Allure测试结果json文件。
        """
        try:
            if os.listdir(self._ALLURE_RESULT) != list():
                time.sleep(1)
                shutil.rmtree(self._ALLURE_RESULT)
                os.mkdir(self._ALLURE_RESULT)
                logger.info("[Success]：已经成功清空Allure历史测试结果.")
            else:
                logger.info("当前暂无Allure历史测试结果，无需清除操作！")
        except Exception:
            logger.exception("[Exception]：清空Allure历史测试结果过程中发生异常，请检查！")

    def sync_history(self):
        """
        追加Allure历史追溯信息
        :return:
        """
        ALLURE_RESULT_HISTORY = os.path.join(self._ALLURE_RESULT, "history")
        ALLURE_REPORT_HISTORY = os.path.join(self._ALLURE_REPORT, "history")
        try:
            if os.path.exists(ALLURE_RESULT_HISTORY):
                raise FileExistsError
            if os.path.exists(ALLURE_REPORT_HISTORY):
                time.sleep(1)
                shutil.copytree(ALLURE_REPORT_HISTORY, ALLURE_RESULT_HISTORY)
                logger.info("[Success]：已经成功同步Allure历史追溯信息.")
            else:
                logger.warning('[WARNING]：Allure历史追溯信息"{}"当前并不存在，无法完成同步！'.format(ALLURE_REPORT_HISTORY))
        except FileExistsError:
            logger.exception('[Exception]：已同步Allure历史追溯信息至"{}"，无需再次同步！'.format(ALLURE_RESULT_HISTORY))
        except Exception:
            logger.exception("[Exception]：同步Allure历史追溯信息过程中发生异常，请检查！")

    def sync_environment(self):
        """
        同步Allure环境信息文件
        :return:
        """
        if self._RESOURCE_PATH is None:
            pass
        else:
            ENVIRONMENT_INFO = os.path.join(self._RESOURCE_PATH, "environment.properties")
            try:
                if os.path.exists(ENVIRONMENT_INFO):
                    time.sleep(1)
                    shutil.copyfile(ENVIRONMENT_INFO, os.path.join(self._ALLURE_RESULT, "environment.properties"))
                    logger.info("[Success]：已经成功同步Allure环境信息文件.")
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                logger.exception('[Exception]：Allure环境信息文件"{}"并不存在，无法同步，请检查！'.format(ENVIRONMENT_INFO))
            except Exception:
                logger.exception("[Exception]：同步Allure环境信息文件过程中发生异常，请检查！")

    def sync_categories(self):
        """
        同步Allure测试分类文件
        :return:
        """
        if self._RESOURCE_PATH is None:
            pass
        else:
            CATEGORIES_INFO = os.path.join(self._RESOURCE_PATH, "categories.json")
            try:
                if os.path.exists(CATEGORIES_INFO):
                    time.sleep(1)
                    shutil.copyfile(CATEGORIES_INFO, os.path.join(self._ALLURE_RESULT, "categories.json"))
                    logger.exception("[Success]：已经成功同步Allure测试分类文件.")
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                logger.exception('[Exception]：Allure测试分类文件"{}"并不存在，无法同步，请检查！'.format(CATEGORIES_INFO))
            except Exception:
                logger.exception("[Exception]：同步Allure测试分类文件过程中发生异常，请检查！")

    def initial_allure(self):
        """
        初始化Allure
        :return:
        """
        try:
            logger.info('[Initial]：开始初始化Allure......')
            self.clear_result()
            if os.path.exists(self._ALLURE_REPORT):
                self.sync_history()
            self.sync_environment()
            self.sync_categories()
            logger.info("[Done]：已经成功初始化Allure.")
        except Exception:
            logger.exception("[Exception]：初始化Allure过程中发生异常，请检查！")
