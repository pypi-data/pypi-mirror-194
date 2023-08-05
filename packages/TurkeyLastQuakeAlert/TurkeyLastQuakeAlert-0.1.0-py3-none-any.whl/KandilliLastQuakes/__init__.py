import wget
import os
import json
import time
import general

def to_quake_dict(text:str):
    list = text.split(" ")
    true_quake = []
    for a in list:
        if a != "":
            true_quake.append(a)
    location_list = true_quake[8:len(true_quake) - 1]
    location = ""
    for a in location_list:
        location += a + " "
    location = location.strip(" ")
    time = str(int(true_quake[1].split(":")[0]) + 3) + ":" + true_quake[1].split(":")[1] + ":" + true_quake[1].split(":")[2]
    return {
        'Date': true_quake[0],
        'Time': time,
        'Depth': float(true_quake[4]),
        'Magnitude': float(true_quake[6]),
        'Location': location
    }

class KandilliQuakeGetter:
    def __init__(self, list_url) -> None:
        self.url = list_url
        self.quake_list = []
        self.last_quake = None

    def refresh(self):
        if os.path.exists("kandilli_list.txt"):
            os.remove("kandilli_list.txt")
        print("----------------")
        print("wget download list...")
        wget.download(self.url, "kandilli_list.txt")
        print("\nImporting...")
        time.sleep(json.load(open("run_infos.json"))['Wait_Time'])
        quake_list = open("kandilli_list.txt").readlines()[6:len(open("kandilli_list.txt").readlines())]
        self.quake_list.clear()
        for a in quake_list:
            self.quake_list.append(to_quake_dict(a))
        os.remove("kandilli_list.txt")
        self.last_quake = self.quake_list[0]

    def get_last_quake(self):
        return self.last_quake
    
    def get_quake_list(self):
        return self.quake_list

    def save_last_quake(self, file_path="last.json"):
        with open(file_path, "w") as last_file:
            json.dump(self.get_last_quake(), last_file)
