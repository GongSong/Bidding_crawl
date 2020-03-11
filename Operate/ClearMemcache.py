from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException
import time

#手动清理手机它运行内存
def ClearMemory(device,poco,deviceNum:str):
    device.keyevent("121")
    print('点击所有应用按钮')
    time.sleep(2)
    #针对Mate8系列
    if poco("com.android.systemui:id/clear_all_recents_image_button").exists():
        poco("com.android.systemui:id/clear_all_recents_image_button").click([0,0])
        print('清理内存')
    
    pass