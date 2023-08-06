from dataclasses import dataclass, field
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class Individualization(object):
    """
    Individualize a mechanistic model by incorporating gene expression levels.

    Attributes
    ----------
    parameters : List[str]
        List of model parameters.

    species : List[str]
        List of model species.

    transcriptomic_data : str
        Path to normalized gene expression data (CSV-formatted),
        e.g., (1) RLE-normalized and (2) post-ComBat TPM values.

        =========== ======== ======== ======== ===
        Description patient1 patient2 patient3 ...
        =========== ======== ======== ======== ===
        gene1       value1,1 value1,2 value1,3 ...
        gene2       value2,1 value2,2 value2,3 ...
        gene3       value3,1 value3,2 value3,3 ...
        ...         ...      ...      ...      ...
        =========== ======== ======== ======== ===

    gene_expression : Dict[str, List[str]]
        Pairs of proteins and their related genes.

    read_csv_kws : dict, optional
        Keyword arguments to pass to ``pandas.read_csv``.

    prefix : str (default: "w_")
        Prefix of weighting factors on gene expression levels.
    """

    parameters: List[str]
    species: List[str]
    transcriptomic_data: str
    gene_expression: Dict[str, List[str]]
    read_csv_kws: Optional[dict] = field(default=None)
    prefix: str = field(default="w_", init=False)

    def __post_init__(self) -> None:
        kwargs = self.read_csv_kws
        if kwargs is None:
            kwargs = {}
        self._expression_level: pd.DataFrame = pd.read_csv(self.transcriptomic_data, **kwargs)

    @property
    def expression_level(self) -> pd.DataFrame:
        return self._expression_level

    def _calculate_weighted_sum(
        self,
        id: str,
        x: List[float],
    ) -> Dict[str, float]:
        """
        Incorporate gene expression levels in the model.

        Returns
        -------
        weighted_sum : Dict[str, float]
            Estimated protein levels after incorporating transcriptomic data.
        """
        weighted_sum = dict.fromkeys(self.gene_expression, 0.0)
        for (protein, genes) in self.gene_expression.items():
            for gene in genes:
                weighted_sum[protein] += (
                    x[self.parameters.index(self.prefix + gene)]
                    * self.expression_level.at[gene, id]
                )
        return weighted_sum

    def as_reaction_rate(
        self,
        id: str,
        x: List[float],
        param_name: str,
        protein: str,
    ) -> float:
        """
        Gene expression levels are incorporated as a reaction rate.

        Parameters
        ----------
        id : str
            CCLE_ID or TCGA_ID.

        x : List[float]
            List of parameter values.

        param_name : str
            Name of the parameter incorporating gene_expression_data.

        protein: str
            Protein involved in the reaction.

        Returns
        -------
        param_value : float
        """
        weighted_sum = self._calculate_weighted_sum(id, x)
        param_value = x[self.parameters.index(param_name)]
        param_value *= weighted_sum[protein]
        return param_value

    def as_initial_conditions(
        self,
        id: str,
        x: List[float],
        y0: List[float],
    ) -> List[float]:
        """
        Gene expression levels are incorporated as initial conditions.

        Parameters
        ----------
        id : str
            CCLE_ID or TCGA_ID.

        x : List[float]
            List of parameter values.

        y0 : List[float]
            List of initial values.

        Returns
        -------
        y0 (individualized) : List[float]
            Cell-line- or patient-specific initial conditions.
        """
        weighted_sum = self._calculate_weighted_sum(id, x)
        for protein in self.gene_expression.keys():
            y0[self.species.index(protein)] *= weighted_sum[protein]
        return y0
