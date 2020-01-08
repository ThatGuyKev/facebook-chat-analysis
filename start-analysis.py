from jsonutilities import handleFile
import sys
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiment_analyzer = SentimentIntensityAnalyzer()


def analyze(chat):
    # Use jsonutilites for clean up
    contents, hours = handleFile(chat+'.json')

    neutral, negative, positive = 0, 0, 0

    for index, sentence in enumerate(contents):

        scores = sentiment_analyzer.polarity_scores(sentence)
        scores.pop('compound', None)

        maxAttribute = max(scores, key=lambda k: scores[k])

        if maxAttribute == "neu":
            neutral += 1
        elif maxAttribute == "neg":
            negative += 1
        else:
            positive += 1

    total = neutral + negative + positive
    print("Negative: {0}% | Neutral: {1}% | Positive: {2}%".format(
        negative*100/total, neutral*100/total, positive*100/total))

    labels = 'Neutral', 'Negative', 'Positive'
    sizes = [neutral, negative, positive]
    colors = ['#00bcd7', '#D22500', '#41CB00']

    # Plot
    figs, (ax1, ax2) = plt.subplots(2, figsize=(8, 8))

    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)


    wedges, texts, autotexts = ax1.pie(sizes, autopct=lambda pct: func(pct, sizes),
            colors=colors,
            textprops=dict(color="w"))

    ax1.legend(wedges, labels,
          title="labels",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    ax1.set_title("Chat Analysis - Chat with {0}".format(chat.capitalize()))

    time_groups = {}

    for i in range(24):
        time_groups[str(i)] = 0

    for hour in hours:
        time_groups[str(int(hour))] += 1



    ax2.bar(range(len(time_groups)), time_groups.values(), align='center')

    ax2.set_xticks(np.arange(len(time_groups)))
    ax2.set_xticklabels(time_groups.keys())

    ax2.set_xlabel('Time groups with 1 hour interval')
    ax2.set_ylabel('Frequency')

    ax2.set_title("Timing Analysis - Chat with {0}".format(chat.capitalize()))
    
    plt.show()

analyze(sys.argv[1])