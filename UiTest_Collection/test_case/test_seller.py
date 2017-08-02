#-*-coding:utf-8-*-
#Time:2017/7/5-20:02
#Author:YangYangJun


import os
import sys
import SendKeys
#from UiTest import baseinfo

reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
import time
import unittest
from selenium.webdriver.common.action_chains import ActionChains

import re
#import baseinfo
from UiTest import baseinfo

class Seller(unittest.TestCase):
    '''卖家中心'''

    @classmethod
    def setUpClass(self):
        self.base_url = baseinfo.base_url
        self.username = baseinfo.sellerName
        self.password = baseinfo.sellerPassword
        self.drugList = [u'吲达帕胺片', u'硝酸咪康唑乳膏']
        self.manufacturerList = [u'遂成药业股份有限公司', u'遂成药业股份有限公司']
        profile = webdriver.FirefoxProfile()
        # 设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录
        profile.set_preference("browser.download.folderList", 2)
        # 这里设置与否不影响，没有发现有什么影响。
        # profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", r"c:\Down")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # 这里设置与否没有发现有什么影响
        profile.set_preference("browser.helperApps.alwaysAsk.force", False);
        self.driver = webdriver.Firefox(profile)
        # 需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可
        self.driver.maximize_window()
        self.driver.get("%s/user/tologin" % self.base_url)
        double_click = self.driver.find_element_by_id("username")
        ActionChains(self.driver).double_click(double_click).perform()
        self.driver.find_element_by_id("username").send_keys("%s" % self.username)
        double_click = self.driver.find_element_by_id("password")
        ActionChains(self.driver).double_click(double_click).perform()
        self.driver.find_element_by_id("password").send_keys("%s" % self.password)
        self.driver.find_element_by_id("sign_btn").click()
        print(u"登录成功")

    @classmethod
    def tearDownClass(self):
        self.driver.quit()




    # def setUp(self):
    #     self.base_url = baseinfo.base_url
    #     self.username = baseinfo.sellerName
    #     self.password = baseinfo.sellerPassword
    #     self.drugList = [u'吲达帕胺片',u'硝酸咪康唑乳膏']
    #     self.manufacturerList = [u'遂成药业股份有限公司',u'遂成药业股份有限公司']
    #     profile = webdriver.FirefoxProfile()
    #     # 设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录
    #     profile.set_preference("browser.download.folderList", 2)
    #     # 这里设置与否不影响，没有发现有什么影响。
    #     # profile.set_preference("browser.download.manager.showWhenStarting", False)
    #     profile.set_preference("browser.download.dir", r"c:\Down")
    #     profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
    #                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    #     # 这里设置与否没有发现有什么影响
    #     profile.set_preference("browser.helperApps.alwaysAsk.force", False);
    #     self.driver = webdriver.Firefox(profile)
    #     # 需要特别说明的是：隐性等待对整个driver的周期都起作用，所以只要设置一次即可
    #     self.driver.maximize_window()
    #     self.driver.get("%s/user/tologin" % self.base_url)
    #     double_click = self.driver.find_element_by_id("username")
    #     ActionChains(self.driver).double_click(double_click).perform()
    #     self.driver.find_element_by_id("username").send_keys("%s" % self.username)
    #     double_click = self.driver.find_element_by_id("password")
    #     ActionChains(self.driver).double_click(double_click).perform()
    #     self.driver.find_element_by_id("password").send_keys("%s" % self.password)
    #     self.driver.find_element_by_id("sign_btn").click()
    #     print(u"登录成功")

    def test_aOrderDetail(self):
        '''订单详情'''
        try :
            print u"订单详情"
            driver = self.driver
            time.sleep(3)
            driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
            test_text = u"卖家中心首页"
            get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
            self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
            driver.find_element_by_xpath(".//*[@id='firstpane']/div[1]/a[1]").click()
            get_orderText = driver.find_element_by_xpath(".//*[@id='seller_order']/div[1]/span").text
            orderText = u"订单管理"
            self.assertEqual(get_orderText, orderText, msg="打开订单管理异常，未定位到页面元素！")
            time.sleep(1)
            get_orderInfo = driver.find_element_by_xpath(".//*[@id='cly_order_list']/li[1]/form/table/thead/tr/th[1]/span[2]").text
            # 获取订单单号  通过正则提取
            print get_orderInfo
            orderNum = re.sub("\D", "", get_orderInfo)
            print orderNum
            # 通过查询找到指定订单
            driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li[1]/div[1]/input").clear()
            driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li[1]/div[1]/input").send_keys(orderNum)
            driver.find_element_by_xpath(".//*[@id='searchBtn']").click()
            # 查看订单详情
            time.sleep(1)
            driver.find_element_by_xpath(".//*[@id='cly_order_list']/li/form/table/tbody/tr/td[3]/a").click()
            time.sleep(2)
            handleList = driver.window_handles
            time.sleep(1)
            driver.switch_to_window(handleList[-1])
            time.sleep(2)
            # detail_tag = u"订单信息"
            get_orderDetail = driver.find_element_by_xpath(".//*[@id='cly_body']/div[4]/div[2]/div[1]/div/div[1]/a").text
            detail_tag = u"西藏UI测试买家"
            self.assertEqual(get_orderDetail, detail_tag, msg="打开订单详情异常，未定位到页面元素！")
            # 校验页面详情信息
            # 校验订单号
            time.sleep(1)
            get_orderNum = driver.find_element_by_xpath(".//*[@id='cly_body']/div[4]/div[2]/div[1]/span").text
            get_buyerPhone = driver.find_element_by_xpath(".//*[@id='cly_body']/div[4]/div[2]/div[2]/div/div/div/ul/li[1]/div[1]/p[2]").text
            buyerPhone = '15201062199'
            if orderNum in get_orderNum and buyerPhone in get_buyerPhone:
                print u"订单详情显示正常！"
            else:
                print u"订单详情显示异常，没有显示订单信息！"
        except BaseException as e :
            print "未找到页面元素，测试用例未正常执行！"
            print e
        finally:
            driver.switch_to_window(handleList[0])


    #总结以往出现的错误，是因为 查询的时候可能没有查询出对应的药品造成的，所以应该调整用例执行顺序
        #应该是先单品发布，然后批量发布，然后单品更新，然后批量更新。


    def atest_bRelease(self):
        '''单品发布'''
        print u"单品发布"
        driver = self.driver
        global releaseStatus
        releaseStatus = 0
        try:
            # time.sleep(3)
            # driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
            # test_text = u"卖家中心首页"
            # get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
            # self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
            time.sleep(2)
            # 打开商品管理
            driver.find_element_by_xpath(".//*[@id='firstpane']/h3[2]").click()
            # 打开商品发布
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='firstpane']/div[2]/a[2]").click()
            time.sleep(3)
            get_AwayText = driver.find_element_by_xpath(".//*[@id='title-tabs']/span[1]").text
            Away_Text = u"单品发布"
            self.assertEqual(get_AwayText, Away_Text, msg="打开单品发布异常，未定位到页面元素！")
            drugNameList = self.drugList[:]
            manuFacturerList = self.manufacturerList[:]
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='goods_keyword']").clear()
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='goods_keyword']").send_keys(drugNameList[0])
            driver.find_element_by_xpath(".//*[@id='factory_keyword']").clear()
            driver.find_element_by_xpath(".//*[@id='factory_keyword']").send_keys(manuFacturerList[0])
            time.sleep(3)
            driver.find_element_by_xpath(".//*[@id='factory_list']/p").click()
            # 点击查询
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='search_btn']").click()
            # 打开搜索到的药品
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='search_result_list']/li[1]").click()
            time.sleep(3)
            driver.find_element_by_xpath(".//*[@id='details']/ul[2]/li/div[1]/input").send_keys("25")
            driver.find_element_by_xpath(".//*[@id='lowest']").send_keys("1")
            driver.find_element_by_xpath(".//*[@id='details']/ul[3]/li[2]/div[1]/input").send_keys("4500")
            # 生产日期
            driver.find_element_by_xpath(".//*[@id='add_production_date']").send_keys("2017-06-06")
            driver.find_element_by_xpath(".//*[@id='add_end_date']").send_keys("2019-08-08")
            driver.find_element_by_xpath(".//*[@id='goods_sell']").click()
            time.sleep(3)
            noticeText = u"操作成功"
            get_Notice = driver.find_element_by_xpath(".//*[@id='popup_modal_success']/div[1]/h2/span").text
            if get_Notice == noticeText:
                releaseStatus = 1
                print u"单品发布成功！"
            else:
                releaseStatus = 0
                self.assertEqual(get_Notice, noticeText, msg="单品发布异常，未定位到页面元素！")
            # 继续发布
            driver.find_element_by_xpath(".//*[@id='popup_modal_success']/div[1]/div[2]/div/div/input").click()
        except BaseException as e:
            print "未找到页面元素，测试用例未正常执行！"
            print e



    def atest_cReleases(self):
        '''批量发布'''
        print u"批量发布"
        global releasesStatus
        releasesStatus = 0
        driver = self.driver
        try:
            time.sleep(5)
            # driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
            # test_text = u"卖家中心首页"
            # get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
            # self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
            # 打开商品管理
            #driver.find_element_by_xpath(".//*[@id='firstpane']/h3[2]").click()
            # 打开商品发布
            # time.sleep(2)
            # driver.find_element_by_xpath(".//*[@id='firstpane']/div[2]/a[2]").click()
            # 点击批量发布
            driver.find_element_by_xpath(".//*[@id='title-tabs']/span[2]").click()
            # 点击有69码上传 下载附件
            time.sleep(2)
            driver.find_element_by_xpath(".//*[@id='down_bar_code_template']").click()
            #获取当前用例的父目录
            #caseFile = os.path.dirname(os.getcwd())
            #根据当前路径 打开测试数据所在路径
            #print caseFile C:\PySpace\CMS
            #releaseFile_Path = os.path.join(caseFile,'caseData')
            #获取测试数据文件。
            releaseFile_Path = os.path.join(os.getcwd(), 'caseData')
            #print releaseFile_Path
            releaseFile = releaseFile_Path + '\itemRelease.xlsx'
            #releaseFile = r'C:\PySpace\CMS\UiTest\caseData' + '\itemRelease.xlsx'
            #print releaseFile_Path
            time.sleep(2)
            driver.find_element_by_css_selector(".webuploader-pick").click()
            time.sleep(2)
            # 将路径输入
            SendKeys.SendKeys(releaseFile)
            time.sleep(3)
            # 确定路径输入
            SendKeys.SendKeys("{ENTER}")
            time.sleep(2)
            # 确定打开按钮
            SendKeys.SendKeys("{ENTER}")
            time.sleep(2)
            # 点击上传
            driver.find_element_by_xpath(".//*[@id='file_upload_btn']").click()
            time.sleep(8)
            # 提示信息， 上传成功
            successTest = u"上传商品成功！"
            get_reInfo = driver.find_element_by_xpath(".//*[@id='step_05']/ul/li[1]").text
            time.sleep(1)
            if get_reInfo == successTest:
                releasesStatus = 1
                print u"批量发布成功！"
            else:
                releasesStatus = 0
                self.assertEqual(get_reInfo, successTest, msg="批量发布异常，未定位到页面元素！")
        except BaseException as e:
            print "未找到页面元素，测试用例未正常执行！"
            print e

    # 定义商品更新函数
    def atest_dItemUpdate(self):
        '''单品更新'''
        print u"单品更新"
        driver = self.driver
        if releaseStatus == 1:
            try:
                time.sleep(3)
                # driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
                # test_text = u"卖家中心首页"
                # get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
                # self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
                # 打开商品管理
                # driver.find_element_by_xpath(".//*[@id='firstpane']/h3[2]").click()
                # time.sleep(2)
                #商品更新
                driver.find_element_by_xpath(".//*[@id='firstpane']/div[2]/a[3]").click()
                item_tag = u"单品更新"
                time.sleep(2)
                get_itemText = driver.find_element_by_xpath(".//*[@id='title-tabs']/span[1]").text
                self.assertEqual(get_itemText, item_tag, msg="打开单品更新异常，未定位到页面元素！")
                print u"打开单品更新成功！"
                # 接下来进行单品更新，先执行一个查询
                drug_name = self.drugList[0]
                # 查询
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").clear()
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").send_keys(drug_name)
                driver.find_element_by_xpath(".//*[@id='searchBtn']").click()
                # 打开详细页面
                driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr[1]/td[8]/button").click()
                time.sleep(3)
                driver.find_element_by_xpath(".//*[@id='details']/ul[2]/li/div[1]/input").clear()
                newPrice = 30.00
                driver.find_element_by_xpath(".//*[@id='details']/ul[2]/li/div[1]/input").send_keys(newPrice)
                # 添加库存
                smallInventory = 6000
                driver.find_element_by_xpath(".//*[@id='details']/ul[3]/li[2]/div[1]/input").clear()
                driver.find_element_by_xpath(".//*[@id='details']/ul[3]/li[2]/div[1]/input").send_keys(smallInventory)
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='goods_submit']").click()
                time.sleep(2)
                update_info = driver.find_element_by_xpath(".//*[@id='popup_modal_success']/div[1]/div[2]/div/p").text
                update_Text = u"您的商品已经更新成功，请选择您需要的操作"
                self.assertEqual(update_info, update_Text, msg="单品更新异常，未定位到页面元素！")
                #print u"单品更新成功，请选择操作！"
                #点击继续更新
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='popup_modal_success']/div[1]/div[2]/div/div/input").click()
                # 查询
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").clear()
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").send_keys(drug_name)
                driver.find_element_by_xpath(".//*[@id='searchBtn']").click()
                time.sleep(2)
                # 获取修改后的价格
                new_Price = driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr/td[4]").text
                latest_Inventory = driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr/td[5]").text
                newPrice = '%.2f' % newPrice
                latestPrice = new_Price
                latestInventory = str(latest_Inventory)
                newPrice = str(newPrice)
                latestPrice = str(latestPrice)
                smallInventory = str(smallInventory)
                if latestPrice == newPrice and latestInventory == smallInventory:
                    print u"商品更新成功！"
                else:
                    print u"商品更新失败！"
                    self.assertEqual(latestPrice, newPrice, msg="价格更新异常！")
                    self.assertEqual(latestInventory, smallInventory, msg="库存更新异常！")
                    # 批量更新
            except BaseException as e:
                print "未找到页面元素，测试用例未正常执行！"
                print e
        else:
            print  U"无商品可更新，请先发布商品！"



    def atest_eItemsUpdate(self):
        '''商品批量更新'''
        print u"商品批量更新"
        driver = self.driver
        if releasesStatus == 1:
            try:
                time.sleep(3)
                # driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
                # test_text = u"卖家中心首页"
                # get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
                # self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
                # 打开商品管理
                # time.sleep(2)
                # driver.find_element_by_xpath(".//*[@id='firstpane']/h3[2]").click()
                # time.sleep(2)
                # driver.find_element_by_xpath(".//*[@id='firstpane']/div[2]/a[3]").click()
                # time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='title-tabs']/span[2]").click()
                # 点击下载
                driver.find_element_by_xpath(".//*[@id='down_template_btn']").click()
                # 输入更新文件路径
                #caseFile = os.path.dirname(os.getcwd())
                #updataFile_Path = os.path.join(caseFile, 'caseData')
                updataFile_Path = os.path.join(os.getcwd(), 'caseData')
                updataFile = updataFile_Path + '\itemUpdate.xlsx'
                #updataFile = r'C:\PySpace\CMS\UiTest\caseData' + '\item_update.xlsx'
                driver.find_element_by_css_selector(".webuploader-pick").click()
                time.sleep(2)
                # 将路径输入
                SendKeys.SendKeys(updataFile)
                time.sleep(3)
                # 确定路径输入
                SendKeys.SendKeys("{ENTER}")
                time.sleep(1)
                # 确定打开按钮
                SendKeys.SendKeys("{ENTER}")
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='file_upload_btn']").click()
                time.sleep(6)
                get_updataText = driver.find_element_by_xpath(".//*[@id='step_05']/ul/li[1]").text
                updataText = u"上传商品成功！"
                if get_updataText == updataText:
                    print u"批量更新成功！"
                else:
                    self.assertEqual(get_updataText, updataText, msg="批量更新异常，未定位到页面元素！")

            except BaseException as e:
                print "未找到页面元素，测试用例未正常执行！"
                print e
        else:
            print  U"无商品可更新，请先发布商品！"


    def atest_fputAway(self):
        '''商品上下架'''
        try:
            print u"商品上下架"
            driver = self.driver
            time.sleep(3)
            # driver.find_element_by_xpath(".//*[@id='slide_wrap']/ul/li[2]").click()
            # test_text = u"卖家中心首页"
            # get_text = driver.find_element_by_xpath(".//*[@id='float']/a").text
            # self.assertEqual(get_text, test_text, msg="进入卖家中心异常，未定位到页面元素！")
            # 打开商品管理
            # time.sleep(1)
            # driver.find_element_by_xpath(".//*[@id='firstpane']/h3[2]").click()
            # 打开商品上下架
            # time.sleep(1)
            driver.find_element_by_xpath(".//*[@id='firstpane']/div[2]/a[1]").click()
            awayText = u"商品上下架"
            time.sleep(1)
            get_awayText = driver.find_element_by_xpath(".//*[@id='cly_address']/span").text
            self.assertEqual(get_awayText, awayText, msg="打开商品上下架异常，未定位到页面元素！")
            # 全选商品-批量操作
            time.sleep(1)
            driver.find_element_by_xpath(".//*[@id='cly_checked_all']").click()
            # 批量下架
            driver.find_element_by_xpath(".//*[@id='soldOutAll']").click()
            #获取弹出提示信息
            get_alertText1 = driver.find_element_by_xpath(".//*[@id='popupSoldOutAll']/div[1]/div[2]/p").text
            alertText = u"您是否确认批量下架所选商品？"
            self.assertEqual(get_alertText1, alertText, msg="获取批量下架提示信息异常，未定位到页面元素！")
            print u"确认下架"
            driver.find_element_by_xpath(".//*[@id='popupSoldOutAll']/div[1]/div[3]/button[1]").click()
            # 全选商品-批量操作
            time.sleep(1)
            driver.find_element_by_xpath(".//*[@id='cly_checked_all']").click()
            # 批量上架
            driver.find_element_by_xpath(".//*[@id='onSellAll']").click()
            get_alertText2 = driver.find_element_by_xpath(".//*[@id='popupOnSellAll']/div[1]/div[2]/p").text
            alertText2 =u"您是否确认批量上架所选商品？"
            self.assertEqual(get_alertText2, alertText2, msg="获取批量上架提示信息异常，未定位到页面元素！")
            driver.find_element_by_xpath(".//*[@id='popupOnSellAll']/div[1]/div[3]/button[1]").click()
            # 单个商品操作 - 操作第一个商品
            # 查询

            time.sleep(1)
            if releaseStatus == 1:
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").clear()
                drugName = self.drugList[:]
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").send_keys(drugName[0])
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='searchBtn']").click()
                # 单个下架
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr/td[8]/button[1]").click()

                time.sleep(2)
                get_Confirm = driver.find_element_by_xpath(".//*[@id='soldOutThis']/div[1]/div[2]/p").text
                confirmText = u"您是否确认下架该商品？"
                self.assertEqual(get_Confirm, confirmText, msg="获取单品下架提示信息异常，未定位到页面元素！")
                #确认下架
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='soldOutThis']/div[1]/div[3]/button[1]").click()
                # 单个上架
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr/td[8]/button[1]").click()
                time.sleep(2)
                get_Confirm1 = driver.find_element_by_xpath(".//*[@id='onSellThis']/div[1]/div[2]/p").text
                confirmText1 = u"您是否确认上架该商品？"
                self.assertEqual(get_Confirm1, confirmText1, msg="获取单品上架提示信息异常，未定位到页面元素！")
                #print (U"上架商品%s" % drugName)
                time.sleep(2)

                driver.find_element_by_xpath(".//*[@id='onSellThis']/div[1]/div[3]/button[1]").click()
                # 删除首商品
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr/td[8]/button[2]").click()
                get_delText = driver.find_element_by_xpath(".//*[@id='delThis']/div[1]/div[2]/p").text
                delText = u"您是否确认删除该商品？"
                self.assertEqual(get_delText, delText, msg="获取单品删除提示信息异常，未定位到页面元素！")
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='delThis']/div[1]/div[3]/button[1]").click()
            else:
                print u"单品删除,无商品可删除，请先发布商品！"

            #print u"清除输入框"
            time.sleep(1)
            if releasesStatus == 1:
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").clear()
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='searchForm']/ul/li/div[3]/input").send_keys(drugName[1])
                time.sleep(1)
                driver.find_element_by_xpath(".//*[@id='searchBtn']").click()
                time.sleep(2)
                driver.find_element_by_xpath(".//*[@id='cly_product_list']/tbody/tr[1]/td[1]/label/input[1]").click()
                #点击批量删除
                driver.find_element_by_xpath(".//*[@id='delAll']").click()

                del_Text = driver.find_element_by_xpath(".//*[@id='popupDelAll']/div[1]/div[2]/p").text
                delText = u"您是否确认批量删除所选商品？"
                self.assertEqual(del_Text, delText, msg="获取批量删除提示信息异常，未定位到页面元素！")
                print u"确认批量删除！"
                driver.find_element_by_xpath(".//*[@id='popupDelAll']/div[1]/div[3]/button[1]").click()
            else:
                print u"批量删除,无商品可删除，请先发布商品！"

        except BaseException as e:
            print "未找到页面元素，测试用例未正常执行！"
            print e

    #
    # def tearDown(self):
    #     self.driver.quit()

if __name__ == "__main__":
    unittest.main()






