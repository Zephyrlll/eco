import os, csv, json

# オートセーブ
def autosave_tick(self, path='save.json'):
    self._save_counter += 1
    if self._save_counter >= self.save_frequency:
        self._save_counter = 0
        save(self, path)

# セーブ先
def save(self, path='save.json'):
    data = {
        "status": self.status,
        "hazards": [{"name": hz.name, "days": hz.days} for hz in self.envsys.hazards]
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ログ書き込み
def csv_log(self, path='ecosystem_log.csv'):
    fields = ["年", "月", "日", "植物", "草食動物", "肉食動物", "人間", "酸素", "二酸化炭素", "窒素", "水"]
    row = [self.status.get(i, 0) for i in fields]
    file_exists = os.path.exists(path)
    with open(path, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(fields)
        w.writerow(row)