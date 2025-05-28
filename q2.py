import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv
import os

def c_distance(dist):
    dist = dist.strip().lower()
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
            header = next(reader)

            for row in reader:
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
        messagebox.showerror("Error", "File not found")
        return None
    return graph

def bfs(graph, start):
    visited = set()
    queue = [start]
    result = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if node in graph:
                # Sort nearest first
                sorted_hotels = sorted(graph[node], key=lambda x: x[1])
                result.extend(sorted_hotels)
    return result

def dfs(graph, start):
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            if node in graph:
                # Sort furthest first
                sorted_hotels = sorted(graph[node], key=lambda x: x[1], reverse=True)
                result.extend(sorted_hotels)
    return result


class hotel:
    def __init__(self, root):
        self.root = root
        self.root.title("Nearest Hotel from Certain Landmark Finder")
        self.root.geometry("1000x700")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Nearest Hotel Locator", font=("Arial", 24, "bold"), anchor="center")
        title_label.pack(pady=(0, 20))


        load_frame = ttk.LabelFrame(main_frame, text="Select your region you wanted to explore!", padding="10")
        load_frame.pack(fill=tk.X)

        self.status = ttk.Label(load_frame, text="Location has not selected yet")
        self.status.pack(fill=tk.X)

        button = ttk.Button(load_frame, text="Select CSV file of your region area", command=self.load_csv)
        button.pack(fill=tk.X)

        self.search = ttk.LabelFrame(main_frame, text="Search Hotels", padding="10")
        self.search.pack(fill=tk.X, pady=10)

        land_label = ttk.Label(self.search, text="Select the landmark you wanted to choose", font=("Arial", 15))
        land_label.pack(pady=(0, 5), anchor="w")

        self.landmark = tk.StringVar()
        self.landmark_drop = ttk.Combobox(self.search, textvariable=self.landmark, state="disabled")
        self.landmark_drop.pack(fill=tk.X, pady=(0, 5))

        self.method = tk.StringVar(value="bfs")

        bfs_radio = ttk.Radiobutton(self.search, text="Using BFS", variable=self.method, value="bfs")
        bfs_radio.pack(anchor="w")

        dfs_radio = ttk.Radiobutton(self.search, text="Using DFS", variable=self.method, value="dfs")
        dfs_radio.pack(anchor="w")

        self.button = ttk.Button(self.search, text="SEARCH!", state="disabled", command=self.search_hotels)
        self.button.pack(fill=tk.X, ipady=5)

        self.output = tk.Text(main_frame, height=20)
        self.output.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            title="Select your CSV file",
            filetypes=[("CSV Files", "*.csv")]
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
            self.display("Wait...")
        else:
            self.landmark_drop.config(values=[], state="disabled")
            self.button.config(state="disabled")
            self.display("Data not found")

    def search_hotels(self):
        landmark = self.landmark.get()
        method = self.method.get()

        if method == "bfs":
            results = bfs(self.graph, landmark)
        else:
            results = dfs(self.graph, landmark)

        if results:
            output_text = f"These are the nearest hotels from '{landmark}' searched using {method.upper()}:\n\n"
            for hotel_name, distance in results:
                output_text += f"- {hotel_name} ({distance:.0f} meter)\n"
        else:
            output_text = "Nearest hotels not found."

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, output_text)

    def display(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    app = hotel(root)
    root.mainloop()
