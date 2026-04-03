from sklearn.cluster import KMeans
def run_kmeans(df):
    features = df[["trend_score","store_density","iot_score","vehicles_live"]]
    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = model.fit_predict(features)
    return df
