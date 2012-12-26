import xbmc, xbmcgui, mc
import time
import subprocess
import common
from random import randint

fanart = {}
fanart_changed = 0

from pysqlite2 import dbapi2 as sqlite

def get_fanart_list():
    global fanart
    showlist = common.file_get_contents("/data/etc/.fanart")
    if showlist == "":
        return
        
    showlist = showlist.split("\n")
    fanart = {}
    for line in showlist:
        if "=" in line:
            line = line.split("=")
            show = line[0]
            art = line[1]
            fanart[show] = art

def store_fanart_list():
    global shows, fanart_changed
    
    file = ""
    for show in fanart:
        file = file + show + "=" + fanart[show] + "\n"
    
    common.file_put_contents("/data/etc/.fanart", file)
    fanart_changed = 0
    
def grab_fanart_for_item(item):
    global fanart, fanart_changed

    if item.GetProperty("fanart") != "":
        return

    label = item.GetLabel()

    path = "%s" % item.GetPath()
    if "stack:" in path:
        path = path.split(" , ")
        path = path[len(path)-1]
        
    thumbnail = item.GetThumbnail()
    art = ""

    # to make sure we don't generate fanart entries for things like vimeo
    if path.find("http://") != -1:
        return

    print art
    if path != "" and path.find("boxeedb://") == -1:
        art = path[0:path.rfind("/")+1] + "fanart.jpg"
    elif thumbnail.find("special://") == -1:
        art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"
    elif label in fanart:
        art = fanart[label]
    else:
        db_path = xbmc.translatePath('special://profile/Database/') + "../../../Database/boxee_catalog.db"
        conn = sqlite.connect(db_path)
        c = conn.cursor()
        if path.find("boxeedb://") == -1:
            # it must be a movie
            sql = "SELECT strCover FROM video_files WHERE strTitle=\"" + label + "\";"
        else:
            # it must be a tv show
            sql =  "SELECT strCover FROM series WHERE strTitle=\"" + label + "\";"

        data = c.execute(sql)
        for row in data:
            thumbnail = "%s" % row[0]
            if "/" in thumbnail:
                art = thumbnail[0:thumbnail.rfind("/")+1] + "fanart.jpg"

        c.close()
        conn.close()
        
    if art != "" and art != "fanart.jpg":
        fanart[label] = art
        fanart_changed = 1
        item.SetProperty("fanart", str(art))
        
def grab_random_fanart(controlNum, special):
    global fanart
    
    get_fanart_list()
    
    # sometimes the list control isn't available yet onload
    # so add some checking to make sure
    control = common.get_control(controlNum, special)
    count = 10
    while control == "" and count > 0 and not common.get_abort_requested():
        time.sleep(0.25)
        control = common.get_control(controlNum, special)
        count = count - 1
    
    window = common.get_window_id(special)
    if control == "":
        pass
    else:
        more = 1
        while control != "" and more == 1 and len(fanart) > 0 and not common.get_abort_requested():
            art = fanart[fanart.keys()[randint(0, len(fanart) - 1)]]
            if art != "":
                art = "$COMMA".join(art.split(","))
            
            xbmc.executebuiltin("Skin.SetString(random-fanart,%s)" % art)
            count = 8
            while count > 0 and more == 1 and not common.get_abort_requested():
                if window != common.get_window_id(special):
                    more = 0
                time.sleep(1)
                count = count - 1
            
            control = common.get_control(controlNum, special)

def grab_fanart_list(listNum, special):
    global fanart_changed
    
    get_fanart_list()
    
    # sometimes the list control isn't available yet onload
    # so add some checking to make sure
    lst = common.get_list(listNum, special)
    count = 10
    while lst == "" and count > 0 and not common.get_abort_requested():
        time.sleep(0.25)
        lst = common.get_list(listNum, special)
        count = count - 1

    window = common.get_window_id(special)
    if lst == "":
        pass
    else:
        # as long as the list exists (while the window exists)
        # the list gets updated at regular intervals. otherwise
        # the fanart disappears when you change sort-orders or
        # select a genre
        # should have very little overhead because all the values
        # get cached in memory
        numItems = 0
        more = 1
        items = lst.GetItems()
        while lst != "" and more == 1 and not common.get_abort_requested():

            # try and apply the stuff we already know about
            if (len(items) > numItems):
                for item in items:
                    grab_fanart_for_item(item)

                items = numItems
            
            if window != common.get_window_id(special):
                more = 0
                
            time.sleep(1)
            
            # store the fanart list for next time if the list
            # was modified
            if fanart_changed == 1:
                store_fanart_list()

            if not common.get_abort_requested():
                control = common.get_control(listNum, special)
                lst = common.get_list(listNum, special)
                if lst != "":
                    items = lst.GetItems()

if (__name__ == "__main__"):
    command = sys.argv[1]

    if command == "grab_fanart_list": grab_fanart_list(int(sys.argv[2]), False)
    if command == "grab_fanart_list_special": grab_fanart_list(int(sys.argv[2]), True)
    if command == "grab_random_fanart": grab_random_fanart(int(sys.argv[2]), False)