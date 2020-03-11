# -*- encoding=utf8 -*-
from poco.proxy import UIObjectProxy
from poco.exceptions import PocoNoSuchNodeException

def CloseUpDateInfo(poco):
    if poco("com.sankuai.meituan.takeoutnew:id/wm_upgrade_force_cancel").exists():
        poco("com.sankuai.meituan.takeoutnew:id/wm_upgrade_force_cancel").click()