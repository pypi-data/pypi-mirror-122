import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm.auto import trange
from .embeddings import AnchiBert
from .UtilsGeneral import stringify_obj, flatten


class SenseAnalysis:

    def __init__(self, concord_lines:list, bert_model:AnchiBert, is_traditional=True, token_idx:tuple=None, hover_df:pd.DataFrame=None):
        
        self.model = bert_model
        self.concords = concord_lines
        self.concords_len = len(self.concords)
        self.embeddings = np.empty((self.concords_len, 768))
        self._get_embeddings(is_traditional, token_idx)
        self.embeddings_plotting = None
        self.clustering = None

        # Plotting info
        self.hover_df = hover_df
        if hover_df is None:
            hover_df = []
            for x in self.concords:
                d = {
                    'left': x.data['left'],
                    'keyword': x.data['keyword'],
                    'right': x.data['right'],
                    # 'kwic': x.data['left'] + '{' + x.data['keyword'] + '}' + x.data['right'],
                    'timestep': str(x.get_timestep()),
                }
                for k, v in flatten(x.data['meta'], parent_key='m').items():
                    d[k] = stringify_obj(v)
                hover_df.append(d)
            self.hover_df = pd.DataFrame(hover_df)
    

    def hierarchical_clustering(self, threshold=5, criterion='maxclust', standardize=True, method='average', metric='cosine', visualize=True):
        from scipy.cluster.hierarchy import fcluster

        if self.clustering is None:
            self.hierarchical_clustering_explore(standardize=standardize, method=method, metric=metric, dendrogram=False, elbow=False)
        self.hover_df['cluster'] = fcluster(self.clustering, t=threshold, criterion=criterion)

        if visualize:
            self.plot_embeddings(interactive=False, labels=self.hover_df['cluster'])

        return self.hover_df


    def hierarchical_clustering_explore(self, standardize=True, method='average', metric='cosine', \
        dendrogram=True, elbow=True, elbow_metrics="distortion calinski_harabasz silhouette", figsize=(23,7)):
        """Perform hierarchical clustering on the embedding space

        Parameters
        ----------
        standardize : bool, optional
            Whether to use zscores for each of the 768 dimension in the 
            Bert model, by default True
        """
        from scipy.stats import zscore
        from scipy.cluster.hierarchy import linkage

        # Scale features
        if standardize:
            X = zscore(self.embeddings, axis=0)
        else:
            X = self.embeddings
        
        # Clustering with cosine distance and average linkage method
        self.clustering = linkage(X, method=method, metric=metric)
        # Dendrogram
        if dendrogram:
            self.plot_dendrogram(figsize=figsize)
        
        # Elbow visualizer
        if elbow:
            from sklearn.cluster import AgglomerativeClustering
            model = AgglomerativeClustering(linkage=method, affinity=metric)
            self.plot_elbow(model, X, metrics=elbow_metrics, figsize=figsize)


    def plot_elbow(self, cluster_model, data, metrics='distortion calinski_harabasz silhouette', figsize=(23, 7)):
        from yellowbrick.cluster import KElbowVisualizer
        
        # Plot
        metrics = metrics.strip().split()
        fig, axes = plt.subplots(ncols=len(metrics), figsize=figsize)
        for i, m in enumerate(metrics):
            visualizer = KElbowVisualizer(cluster_model, k=(2,30), metric=m, timings= False, locate_elbow=True, ax=axes[i])
            visualizer.fit(data)      # Fit the data to the visualizer
            visualizer.finalize()  # Finalize and render the figure


    def plot_dendrogram(self, model=None, figsize=(25,10)):
        from scipy.cluster.hierarchy import dendrogram
        
        fig = plt.figure(figsize=figsize)
        if model is None:
            dn = dendrogram(self.clustering)
        else:
            dn = dendrogram(model)
        plt.show()


    def plot_embeddings(self, interactive=True, labels:str=None, **keywords):
        import umap.plot
        if self.embeddings_plotting is None:
            self.embeddings_plotting = self.embeddings_dim_reduce(dim=2, method="umap")
        labels = self.hover_df[labels] if labels is not None else None

        if interactive:
            from bokeh.plotting import show as bokeh_show
            f = umap.plot.interactive(self.embeddings_plotting, 
                            labels=labels, 
                            hover_data=self.hover_df, 
                            **keywords)
            bokeh_show(f)
        else:
            umap.plot.points(self.embeddings_plotting, labels=labels, **keywords)


    def embeddings_dim_reduce(self, dim=2, method="umap"):
        print(f"Reducing the embedding space to {dim} dimensions...")
        if method.lower() == "umap":
            import umap
            emb = umap.UMAP(n_components=dim, metric='cosine').fit(self.embeddings)
        if method.lower() == "pca":
            from sklearn.decomposition import PCA
            emb = PCA(n_components=dim).fit_transform(self.embeddings)
        return emb


    def _get_embeddings(self, is_traditional=True, token_idx:tuple=None):
        print('Computing embeddings...')
        for i in trange(self.concords_len):
            sent, tk_idx = self.concords[i].get_kwic()
            if token_idx is not None:
                tk_idx = token_idx
            self.embeddings[i] = self.model.encode_sentence(sent, *tk_idx, is_traditional=is_traditional)

