import os
import re
import sys
import random

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    random_page_p = (1 - damping_factor) / len(corpus)
    result = {k: random_page_p for k in corpus.keys()}
    links = corpus[page]
    link_p = damping_factor / len(links)
    for k in result.keys():
        if k in links:
            result[k] = link_p
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # print(corpus, damping_factor, n)
    result = {k: 0 for k in corpus.keys()}
    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        sample = transition_model(corpus, page, damping_factor)
        weights = []
        pages = []
        for k, v in sample.items():
            pages.append(k)
            weights.append(v)
        page = random.choices(pages, weights=weights)[0]
        result[page] += 1
    for k in result:
        result[k] /= n
    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # print(corpus, damping_factor)
    corpus_len = len(corpus)
    result = {k: 1/corpus_len for k in corpus.keys()}

    while True:
        for page in result:
            links = [page_ for page_, links in corpus.items() if page in links]

            first = (1 - damping_factor)/corpus_len

            sum = 0
            for link in links:
                sum += result[link] / len(corpus[link])
            second = damping_factor*sum

            new = first + second
            if abs(new - result[page]) < 0.001:
                return result
            result[page] = new


if __name__ == "__main__":
    main()
