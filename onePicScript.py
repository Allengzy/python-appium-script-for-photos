from appium import webdriver
import time
import os
i=0
#i记录本次总共处理图片数量
j=0
#j记录文件夹里图片数量
importPath = "C:/Users/allen/Documents/appium/raw/"
exportPath = "C:/Users/allen/Documents/appium/export/"
#导入图片路径
p1Size = 0
exportP1 = ""
os.system("adb root")
while i < 20:
    importP1 = importPath+str(i)+'.jpg'
    p1Size = os.path.getsize(importP1)
    i = i+1
    os.system("adb push "+importP1+" /storage/emulated/legacy/Pictures/Screenshots")
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
            # 休眠2秒等待页面加载完成
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

            try:
                time.sleep(1)
                driver.tap([(372,1714),(444,1795)],300)  #load太慢了所以只能直接tap固定位置了加快速度
            except:pass

            try:
                time.sleep(1)
                driver.tap([(372,1714),(444,1795)],300)  #load太慢了所以只能直接tap固定位置了加快速度
            except:pass

            time.sleep(2)
            driver.find_element_by_id("com.intsig.camscanner:id/tv_select").click()
            #图片全选

            time.sleep(2)
            driver.find_element_by_id("com.intsig.camscanner:id/tv_export").click()
            #导入

            time.sleep(4)
            driver.tap([(625,1808),(725,1920)],500)  #太慢了所以只能直接tap固定位置了加快速度
            #取消自动切边(全选按钮)

            time.sleep(3)
            driver.tap([(889,1808),(1001,1920)],500)  #太慢了所以只能直接tap固定位置了加快速度
            #下一步(箭头按钮）

            time.sleep(5)
            driver.tap([(956,1836),(1044,1892)],500)  # 太慢了所以只能直接tap固定位置了加快速度
            #driver.find_element_by_id("com.intsig.camscanner:id/scv_wave_behind").click()
            #结束处理(打钩按钮)[956,1836][1044,1892]

        except:
            loopFinish = False
            #本次处理出现问题(app crash etc)
        else:
            loopFinish = True
            #本次处理无误可以进行导出
            time.sleep(5)
            driver.close_app()
            time.sleep(2)
            os.system("adb pull /storage/emulated/legacy/CamScanner/.images/.afterOCRs/. "+ exportPath)
            time.sleep(2)
            os.system("adb shell rm -r /storage/emulated/legacy/CamScanner/.images")
            files = os.listdir(exportPath)
            if len(files) != i:
                print(len(files))
                loopFinish = False
                #导出不对，继续回到loop进行该张图片操作
            else:
                #确定导出文档数量正确再删本次导入的图片以免出现储存问题
                time.sleep(2)
                os.system("adb shell rm /storage/emulated/legacy/Pictures/Screenshots/" + str(i - 1) + '.jpg')
    #本次图片处理结束，没有问题
    loopFinish = False
    #default loop value为下次loop做准备

#结束所有图片处理后将export文档里面处理完图片按时间排序命名
sortFiles = os.listdir(exportPath)
sortFiles.sort(key=lambda x: os.stat(os.path.join(exportPath, x)).st_mtime)
for filename in sortFiles:
    os.rename(exportPath +filename, exportPath +str(j)+ 'c.jpg')
    j = j+1