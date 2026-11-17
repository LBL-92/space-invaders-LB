from config import SCORES_FILE, TOP_SCORES_SHOWN


def load_scores():
    """Reto 12: read scores.txt and return a list of (name, score) sorted from highest to lowest.

    Each line of the file has the format:  name;score
    Missing file or malformed lines are ignored.
    """
    scores = []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ";" not in line:
                    continue
                name, _, value = line.rpartition(";")
                try:
                    scores.append((name, int(value)))
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    scores.sort(key=lambda item: item[1], reverse=True)
    return scores


def save_score(name, score):
    """Append a new score at the end of scores.txt"""
    name = name.replace(";", "").strip() or "ANON"
    with open(SCORES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{name};{score}\n")


def top_scores(n=TOP_SCORES_SHOWN):
    """Return the n best scores"""
    return load_scores()[:n]
