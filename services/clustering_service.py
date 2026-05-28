from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

def cluster_posts(posts):

    # IF NO POSTS
    if not posts:
        return posts

    texts = []

    for post in posts:

        if "text" in post and post["text"].strip():

            texts.append(post["text"])

    # IF NO VALID TEXTS
    if len(texts) == 0:
        return posts

    try:

        embeddings = model.encode(texts)

        # SINGLE POST CASE
        if len(embeddings) == 1:

            posts[0]["cluster"] = 0

            return posts

        clustering = DBSCAN(
            eps=0.5,
            min_samples=1,
            metric='cosine'
        ).fit(embeddings)

        labels = clustering.labels_

        for i, post in enumerate(posts):

            post["cluster"] = int(labels[i])

    except:

        # FALLBACK
        for i, post in enumerate(posts):

            post["cluster"] = i

    return posts
