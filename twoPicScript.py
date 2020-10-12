from appium import webdriver
import time
import os
i=0
importPath = "C:/Users/allen/Documents/appium/raw/"
exportPath = "C:/Users/allen/Documents/appium/export"
#导入图片路径
p1Size = 0
p2Size = 0
largerI = str(i)
smallerI = str(i)
exportP1 = ""
exportP2 = ""
while i < 90:
    importP1 = importPath+str(i)+'.jpg'
    p1Size = os.path.getsize(importP1)
    i = i+1
    importP2 = importPath+str(i)+'.jpg'
    p2Size = os.path.getsize(importP2)
    i = i+1
    if p1Size > p2Size:
        largerI = str(i-2)
        smallerI = str(i-1)
    else:
        largerI = str(i-1)
        smallerI = str(i-2)
    os.system("adb push "+importP1+" /storage/emulated/legacy/Pictures/Screenshots")
    os.system("adb push "+importP2+" /storage/emulated/legacy/Pictures/Screenshots")

    successOpen = False
    while successOpen == False:
        #打开gallery检查图片
        try:
            desired_caps = {}
            desired_caps['platformName'] = 'Android'  # android的apk还是IOS的ipa
            # desired_caps['platformVersion'] = '5.1.1'  #android系统的版本号
            desired_caps['deviceName'] = '127.0.0.1:62001'  # 手机设备名称，通过adb devices  查看
            desired_caps['appPackage'] = 'com.android.gallery3d'  # apk的包名
            desired_caps['appActivity'] = 'com.android.gallery3d.app.GalleryActivity'  # apk的launcherActivity
            driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)  # 启动服务器地址，后面跟的是手机信息
            # 先开gallery加载导入的图片确保之后能找到
            # 休眠3秒等待页面加载完成
            time.sleep(3)
            driver.close_app()
            #结束所有关于gallery的操作
        except:
            successOpen = False
        else:
            successOpen = True

    loopFinish = False
    while loopFinish == False:
        try:
        #导入图片

            desired_caps['appPackage'] = 'com.intsig.camscanner'  #apk的包名
            desired_caps['appActivity'] = 'com.intsig.camscanner.launcher.WelcomeDefaultActivity'  #apk的launcherActivity
            driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            time.sleep(2)
            driver.find_element_by_id("com.intsig.camscanner:id/go_to_main").click()
            time.sleep(2)
            driver.find_element_by_id("com.intsig.camscanner:id/fab_add_doc").click()
            time.sleep(2)
            driver.find_element_by_id("com.intsig.camscanner:id/iv_cap_new_user_guide_cancel").click()
            #time.sleep(30)
            #driver.implicitly_wait(20)

            try:
                time.sleep(3)
                driver.tap([(372,1714),(444,1795)],100)  #load太慢了所以只能直接tap固定位置了加快速度
            except:pass

            try:
                time.sleep(3)
                driver.tap([(372,1714),(444,1795)],100)  #load太慢了所以只能直接tap固定位置了加快速度
            except:pass

            '''
            try:
                time.sleep(5)
                #driver.implicitly_wait(10)
                driver.find_element_by_id("com.intsig.camscanner:id/tv_i_know").click()
                #我知道了选项（并不一定会出现）
            except:pass #如果没出现就继续
            '''

            driver.implicitly_wait(5)
            driver.find_element_by_id("com.intsig.camscanner:id/tv_select").click()
            #图片全选

            time.sleep(3)
            driver.find_element_by_id("com.intsig.camscanner:id/cb_trim").click()
            #取消自动切边

            driver.implicitly_wait(7)
            driver.find_element_by_id("com.intsig.camscanner:id/tv_export").click()
            #选择增强并锐化处理图片

        except:
            loopFinish = False
            #本次处理出现问题(app crash etc)
        else:
            #driver.close_app()
            #driver.terminate_app('com.intsig.camscanner') ---这个方法好像不太行，目前没有找到更好的解决可能存在的闪退问题
            loopFinish = True
            #本次处理无误可以进行导出
            time.sleep(5)
            os.system("adb pull /storage/emulated/legacy/CamScanner/.images/.afterOCRs " + exportPath)
            time.sleep(2)
            os.system("adb shell rm -r /storage/emulated/legacy/Pictures/Screenshots/" + str(i - 2) + '.jpg')
            time.sleep(2)
            os.system("adb shell rm -r /storage/emulated/legacy/Pictures/Screenshots/" + str(i - 1) + '.jpg')
            time.sleep(3)
            os.system("adb shell rm -r /storage/emulated/legacy/CamScanner/.images")
            files = os.listdir(exportPath + "/.afterOCRs")
            if len(files)!=2:
                loopFinish = False
            else: pass

    #等待软件处理图片并准备导出
    exportP1 = exportPath+"/.afterOCRs/"+files[0]
    exportP2 = exportPath+"/.afterOCRs/"+files[1]
    if os.path.getsize(exportP1) > os.path.getsize(exportP2):
        os.rename(exportP1, exportPath + "/" + largerI + "c.jpg")
        os.rename(exportP2, exportPath + "/" + smallerI + "c.jpg")
    else:
        os.rename(exportP2, exportPath + "/" + largerI + "c.jpg")
        os.rename(exportP1, exportPath + "/" + smallerI + "c.jpg")
    loopFinish = False
    time.sleep(3)
    driver.close_app()
    #default loop value为下次loop做准备