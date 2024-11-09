# Reqs for GUI application
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# For jupyter notebook
import requests as rq
from scipy import stats
from nltk.metrics.distance import jaccard_distance

## Functions imported from the jupyter notebook
N = 200

def query_datamuse(word, n=100):
    query = "https://api.datamuse.com/words?ml={}&max={}".format(word, n)
    response = rq.get(query)
    results = []
    for obj in response.json(): 
        results.append(obj["word"])
    return results

def jaccard_similarity(set1, set2): 
    return 1 - jaccard_distance(set1, set2)

def datamuse_similarity(X, Y, n=100):
    words1 = query_datamuse(X, n=n)
    words2 = query_datamuse(Y, n=n)    
    return jaccard_similarity(set(words1), set(words2))

def calculate_similarities(df, n): 
    words1 = df["word1"].tolist()
    words2 = df["word2"].tolist()
    scores = df["score"].tolist()

    sim_values = []
    for w1, w2 in zip(words1, words2): 
        sim_values.append(datamuse_similarity(w1, w2, n=n))
        
    p = stats.pearsonr(sim_values, scores)
    return p

def get_bag_of_words(sentence): 
    words = sentence.split(" ")
    bag = set(words)
    for word in words: 
        bag = bag.union(set(query_datamuse(word, n=N)))
    return bag

def get_sentence_similarity(sentence1, sentence2):
    bag1 = get_bag_of_words(sentence1)
    bag2 = get_bag_of_words(sentence2)
    return jaccard_similarity(bag1, bag2)

## End of import

root = tk.Tk()
root.geometry("1280x768")
root.title("Semantic Similarity Tasks")
root.configure(bg="white")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

options = ["Dataset statistics", "Custom sentence similarity"]

data = {
    "Word similarity\nMC Dataset @ N100": {"statistic": 0.6197982041050111, "pvalue": 0.0003360473903788395},
    "Word similarity\nMC Dataset": {"statistic": 0.724072525404594, "pvalue": 8.994311402784625e-06},
    "Word similarity\nRG Dataset": {"statistic": 0.7850157130429563, "pvalue": 1.6236618035026146e-14},
    "Word similarity\nWordSim Dataset": {"statistic": 0.49022656405756004, "pvalue": 1.1105676505687779e-22},
    "Sent. similarity\nSTSS-131 v. Datamuse": {"statistic": 0.6207214473990158, "pvalue": 3.342555588241077e-15},
    "Sent. similarity\nSTSS-131 v. TF-IDF": {"statistic": 0.776216151106484, "pvalue": 2.0516274140670272e-27}
}

def show_plot():
    clear_frame()

    figure = Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    methods = list(data.keys())
    statistics = [data[method]["statistic"] for method in methods]
    pvalues = [data[method]["pvalue"] for method in methods]

    ax.bar(methods, statistics, color="skyblue", label="Pearson Statistic")
    ax.set_ylabel("Pearson Statistic", color="blue", fontsize=8)
    ax.tick_params(axis="y", labelcolor="blue", labelsize=8)
    ax.tick_params(axis="x", labelsize=8)

    ax2 = ax.twinx()
    ax2.plot(methods, pvalues, color="red", marker="o", linestyle="--", label="P-Value")
    ax2.set_ylabel("P-Value (log scale)", color="red", fontsize=8)
    ax2.tick_params(axis="y", labelcolor="red", labelsize=8)
    ax2.set_yscale("log")

    plt.title("Pearson Statistic and P-Values for datasets", fontsize=12)
    figure.tight_layout()    

def custom_sentence():
    clear_frame()

    text1 = tk.Text(frame, height=2, wrap="word")
    text1.insert("1.0", "Enter custom sentence here...")
    text1.pack(fill="both", expand=True, pady=10)
    
    text2 = tk.Text(frame, height=2, wrap="word")
    text2.insert("1.0", "Enter another custom sentence here...")
    text2.pack(fill="both", expand=True, pady=10)

    result_label = tk.Label(frame, text="Similarity result will be shown here.")
    result_label.pack(pady=10)

    def calculate_result():
        button.config(state=tk.DISABLED)
        text1.config(state=tk.DISABLED)
        text2.config(state=tk.DISABLED)
        
        sentence1 = text1.get("1.0", "end-1c")
        sentence2 = text2.get("1.0", "end-1c")
        print(f"Sentence 1: {sentence1}")
        print(f"Sentence 2: {sentence2}")

        similarity = get_sentence_similarity(sentence1, sentence2)
        print(f"Datamuse sentence similarity: {similarity}")
        result_label.config(text=f"Datamuse sentence similarity: {similarity}")

        button.config(state=tk.NORMAL)
        text1.config(state=tk.NORMAL)
        text2.config(state=tk.NORMAL)
    
    button = tk.Button(frame, text="Calculate Result", command=calculate_result)
    button.pack(pady=10)

def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

def on_select(event):
    selection = dropdown_var.get()
    if selection == "Dataset statistics":
        show_plot()
    elif selection == "Custom sentence similarity":
        custom_sentence()

show_plot()

dropdown_var = tk.StringVar(value=options[0])
dropdown = ttk.Combobox(root, textvariable=dropdown_var, values=options)
dropdown.set("Select an option")
dropdown.bind("<<ComboboxSelected>>", on_select)
dropdown.pack(pady=10)

# Start the GUI
root.mainloop()
