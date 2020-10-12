from appium import webdriver
import time
import os
os.system("adb push C:\\Users\\allen\\Documents\\appium\\raw /storage/emulated/legacy/Pictures")
#导入图片
desired_caps = {}
desired_caps['platformName'] = 'Android'   #android的apk还是IOS的ipa
#desired_caps['platformVersion'] = '5.1.1'  #android系统的版本号
desired_caps['deviceName'] = '127.0.0.1:62001'    #手机设备名称，通过adb devices  查看
desired_caps['appPackage'] = 'com.android.gallery3d'  #apk的包名
desired_caps['appActivity'] = 'com.android.gallery3d.app.GalleryActivity'  #apk的launcherActivity
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps) #启动服务器地址，后面跟的是手机信息
#先开gallery加载导入的图片确保之后能找到
#休眠3秒等待页面加载完成
time.sleep(3)
driver.close_app()


desired_caps['appPackage'] = 'com.intsig.camscanner'  #apk的包名
desired_caps['appActivity'] = 'com.intsig.camscanner.launcher.WelcomeDefaultActivity'  #apk的launcherActivity
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(5)
driver.find_element_by_id("com.intsig.camscanner:id/go_to_main").click()
time.sleep(4)
driver.find_element_by_id("com.intsig.camscanner:id/fab_add_doc").click()
time.sleep(3)
driver.find_element_by_id("com.intsig.camscanner:id/iv_cap_new_user_guide_cancel").click()

time.sleep(30)
driver.tap([(372,1714),(444,1795)],100) #load太慢了所以只能直接tap固定位置了加快速度
#driver.find_element_by_id("com.intsig.camscanner:id/com.intsig.camscanner:id/combine_import_container").click()
#选择图片导入

driver.implicitly_wait(10)
driver.find_element_by_id("com.intsig.camscanner:id/tv_i_know").click()
#我知道了

driver.implicitly_wait(10)
driver.find_element_by_id("com.intsig.camscanner:id/tv_select").click()
#全选

#driver.implicitly_wait(10)
#driver.find_element_by_id("com.intsig.camscanner:id/tv_enhance_mode").click()
#调整处理选项

#time.sleep(3)
#driver.tap([(672, 796),(768, 892)],100)
#选择黑白

driver.implicitly_wait(20)
driver.find_element_by_id("com.intsig.camscanner:id/tv_export").click()
#处理图片



#导入
time.sleep(60)
os.system("adb pull /storage/emulated/legacy/CamScanner/.images/.afterOCRs C:\\Users\\allen\\Documents\\appium\\export")
time.sleep(5)
os.system("adb shell rm -r /storage/emulated/legacy/CamScanner/.images/.afterOCRs")
time.sleep(5)
os.system("adb shell rm -r /storage/emulated/legacy/Pictures/raw")
time.sleep(5)
os.system("adb shell rm -r /storage/emulated/legacy/CamScanner/.images/.originals")