import pandas as pd
import json
import time

class AfadQuakeGetter:
    def __init__(self, url) -> None:
        self.url = url
        self.last_quake = None
        self.quake_list = []
    
    def refresh(self):
        try:
            df = pd.read_html(self.url, header=0)[0]
        except:
            print("Connection error. Trying to reconnect.")
            time.sleep(json.load(open("run_infos.json"))['Wait_Time'])
            print("\033[A                                                            \033[A")
            return
        print("Refreshing...")
        time.sleep(json.load(open("run_infos.json"))['Wait_Time'])
        dirty_quake_list = json.loads(df.to_json(orient="records"))
        print("Importing...")
        time.sleep(json.load(open("run_infos.json"))['Wait_Time'])
        print("\033[A                                                            \033[A")
        print("\033[A                                                            \033[A")
        self.quake_list.clear()
        for a in dirty_quake_list:
            self.quake_list.append({
                'Date/Time': a['Tarih(TS)'],
                'Depth': float(a['Derinlik(Km)']),
                'Magnitude': float(a['Büyüklük']),
                'Location': a['Yer']
            })
        self.last_quake = self.quake_list[0]

    def get_last_quake(self):
        return self.last_quake

    def save_last_quake(self, file_path="last.json"):
        with open(file_path, "w") as last_file:
            json.dump(self.get_last_quake(), last_file)
