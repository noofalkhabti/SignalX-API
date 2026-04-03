def run_classification(df):
    out=[]
    for _,r in df.iterrows():
        label="High" if r["cluster"]==0 else "Medium" if r["cluster"]==1 else "Low"
        out.append({"zone":r["zone"],"label":label})
    return {"zone_clusters":out}
