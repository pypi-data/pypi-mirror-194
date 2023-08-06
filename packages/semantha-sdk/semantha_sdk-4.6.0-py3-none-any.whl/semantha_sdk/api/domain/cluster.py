from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.cluster import DocumentCluster, DocumentClusterSchema


class DocumentClusterEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/clusters"

    def get(
            self,
            min_cluster_size: str = None,
            clustering_structure: str = None
    ) -> list[DocumentCluster]:
        """ Get document clusters, i.e. a semantic clustering of the documents in the library. Clusters are named and
        have an integer ID. Note that a special cluster with ID '-1' is reserved for outliers, i.e. documents that could
        not have been assigned to a cluster.
        Args:
            min_cluster_size: choose whether to require only a few documents to form a cluster or more. Choose from
                                     either 'LOW', 'MEDIUM' or 'HIGH'.
            clustering_structure: the strategy the clustering algorithm uses to create the clustering space. Choose from
                                  either 'LOCAL', 'BALANCED' or 'GLOBAL' (default 'BALANCED') where LOCAL means that the
                                  model is able to better represent dense structure and GLOBAL means that more
                                  datapoints are considered and the model better represents the overall structure of the
                                  data but lacks details.

        Compatibility note: In future releases more parameters will be added to alter the clustering.
        """
        q_params = {}
        if min_cluster_size is not None:
            q_params["minclustersize"] = min_cluster_size
        if clustering_structure is not None:
            q_params["clusteringstructure"] = clustering_structure
        return self._session.get(
            self._endpoint,
            q_params=q_params
        ).execute().to(DocumentClusterSchema)
