import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv
import os
import io


def c_distance(dist):
    dist  = dist.strip().lower()
    try:
        if 'km' in dist:
            value = float(dist.replace('km', ' ').strip().replace(',', '.'))
            return value * 1000
        elif 'm' in dist:
            value = float(dist.replace('m', '').strip())
            return value
    except ValueError:
        return float('inf')
    return float('inf')


def hotel_graph(filepath):
    graph = {}
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(header)

            for row in reader :
                if not row:
                    continue
                hotel_name = row[0]
                landmark = row[6].strip()
                distance = row[7]

                r_distance = c_distance(distance)

                if landmark not in graph:
                    graph[landmark] = []

                graph[landmark].append((hotel_name, r_distance))


    except FileNotFoundError:
        messagebox.showerror("error")
        return None
 
class hotel:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencari Hotel")
        self.root.geometry("1000x1000")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        load_frame= ttk.LabelFrame(main_frame, text="Muat data", padding="10")
        load_frame.pack(fill=tk.X)

        self.status = ttk.Label(load_frame, text="Belum ada File")
        self.status.pack(fill=tk.X)

        button = ttk.Button(load_frame, text="Pilih File CSV", command=self.load_csv)
        button.pack(fill=tk.X)

        self.search = ttk.LabelFrame(main_frame, text="cari hotel")
        self.search.pack(fill=tk.X, pady=10)

        land_label = ttk.Label(self.search, text="pilih landmark", font=("Arial", 15))
        land_label.pack(pady=(0, 5), anchor="w")

        self.landmark = tk.StringVar()
        self.landmark_drop = ttk.Combobox(self.search, textvariable=self.landmark, state="disabled")
        self.landmark_drop.pack(fill=tk.X, pady=(0, 5))

        self.method = tk.StringVar(value="bfs")

        bfs_radio = ttk.Radiobutton(self.search, text="Menggunakan bfs", textvariable=self.method, value="bfs")
        bfs_radio.pack(anchor="w")

        bfs_radio = ttk.Radiobutton(self.search, text="Menggunakan dfs", textvariable=self.method, value="dfs")
        bfs_radio.pack(anchor="w")

        self.button = ttk.Button(self.search, text="waktunya kita cari", state="disabled")
        self.button.pack(fill=tk.X, ipady=5)

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            title="Pilih File csv",
            filetypes=(("CSV Files", "*csv"))
        )
        if not filepath:
            return
        
        graph = hotel_graph(filepath)

        if graph is not None:
            self.graph = graph
            self.status.config(text=f"File: {os.path.basename(filepath)}")
            self.update_ui()

    def update_ui(self):
        landmarks = list(self.graph.keys())

        if landmarks:
            self.landmark_drop.config(values=landmarks, state="readonly")
            self.landmark_drop.current(0)
            self.button.config(state="normal")
            self.display("Tunggu hasil")
        else:
            self.landmark_drop.config(values=[], state="disabled")
            self.button.config(state="disabeld")
            self.display("NGK ada isinya woy")



if __name__ == "__main__":
    root = tk.Tk()
    app = hotel(root)
    root.mainloop()

