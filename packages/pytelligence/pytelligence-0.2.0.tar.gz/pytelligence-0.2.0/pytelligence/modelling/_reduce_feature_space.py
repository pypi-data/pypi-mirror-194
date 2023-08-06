import logging
from typing import List, Optional, Tuple

import pandas as pd
import seaborn as sns

from . import _internals
from ._train_model import train_model

logger = logging.getLogger(f"stream.{__name__}")


def reduce_feature_space(
    setup: _internals.Setup,
    algorithm: str,
    metric: str,
    reference_metric: float,
    acceptable_loss: float,
    hyperparams: Optional[dict] = None,
) -> Tuple[List[str], pd.DataFrame]:
    """
    Reduces the feature space used for model training
    by iteratively removing the feature with the smallest
    impact on model performance.

    Given an algorithm and metric, retrains models with
    one feature removed. Notes the metric when the weakest
    feature is removed and compares it with the acceptable
    loss threshold. If the threshold has not been reached
    the process is repeated.

    If a metric higher than the reference_metric is found,
    it is printed.

    Parameters
    ----------
    setup : Setup
        Dataclass containing the prepared data and further
        configurations.

    algorithm : str
        Algorithm to use for model training.

    metric : str
        Metric to use for evaluating model performance.

    reference_metric : float
        Metric value to use as baseline.

    acceptable_loss : float
        Acceptable loss threshold, e.g. 0.95. Once a value
        of acceptable_loss * reference_metric is undercut,
        the feature space reduction is reduced.

    hyperparams : Optional[dict]
        Hyperparameters to use with the given algorithm.
        Default `None` will use standard hyperparameters.

    Returns
    -------
    Tuple[List[str], pd.DataFrame]
        best_feature_list : List[str]

        metric_feature_df : pd.DataFrame
            Dataframe with columns `metric` and `features` listing
            the metric values achieved with the respective features.
    """
    logger.info("%%% REDUCING FEATURE SPACE")
    # Initiate reference values
    threshold = acceptable_loss * reference_metric
    feature_list = setup.X_train.columns.to_list()
    best_feature_list = feature_list[:]
    metric_feature_df = pd.DataFrame(columns=["metric", "features"])
    new_metric = reference_metric

    logger.info(f"Algorithm selected for feature space reduction: {algorithm}")
    logger.info(f"Metric to optimize for: {metric}")
    logger.info(f"Acceptable loss ratio: {acceptable_loss}")
    logger.info(f"Reference metric: {reference_metric:.3f}")
    logger.info(
        f"Minimum acceptable metric: {acceptable_loss} * {reference_metric:.3f} = {threshold:.3f}"
    )

    # Iteratively remove features
    while (threshold <= new_metric) & (len(feature_list) > 1):
        (worst_feature, new_metric) = _find_worst_feature(
            setup=setup,
            algorithm=algorithm,
            metric=metric,
            feature_list=feature_list,
            hyperparams=hyperparams,
        )
        feature_list.remove(worst_feature)
        metric_feature_df.loc[len(metric_feature_df)] = [new_metric, feature_list[:]]

        # Update reference_metric and threshold if
        # reference_metric was improved upon
        if new_metric > reference_metric:
            reference_metric = new_metric
            threshold = acceptable_loss * reference_metric
            logger.info(
                f"Feature count: {len(feature_list)}, metric: {new_metric:.3f} (new best), removing worst feature: {worst_feature}"
            )
        else:
            logger.info(
                f"Feature count: {len(feature_list)}, metric: {new_metric:.3f}, removing worst feature: {worst_feature}"
            )

        # Update best_feature_list if metric is equal to
        # reference_metric
        if new_metric == reference_metric:
            best_feature_list = feature_list[:]

    # Adding `feature_count`` column to metric_feature_df
    metric_feature_df["feature_count"] = metric_feature_df.features.apply(
        lambda x: len(x)
    )

    logger.info(f"Best {metric} score found: {reference_metric:.3}")
    logger.info(f"Feature list for best score: {best_feature_list}")

    # Plot metric evolution
    sns.lineplot(data=metric_feature_df, x="feature_count", y="metric", sort=True)

    return best_feature_list, metric_feature_df


def _find_worst_feature(
    setup: _internals.Setup,
    algorithm: str,
    metric: str,
    feature_list: List[str],
    hyperparams: Optional[dict] = None,
) -> Tuple[str, float]:
    """
    Finds worst feature given a specific algorithm and
    metric.

    Loops over all features in feature_list, removes the
    individual feature and trains a models instance on the
    remaining features. Afterwards the feature impact is
    evaluated by calculating the achieved metric.

    The feature associated with the largest metric after
    removal of the feature is returned alongside the metric.

    Parameters
    ----------
    setup : Setup
        Dataclass containing the prepared data and further
        configurations.

    algorithm : str
        Algorithm to use for model training.

    metric : str
        Metric to use for evaluating model performance.

    hyperparams : Optional[dict]
        Hyperparameters to use with the given algorithm.
        Default `None` will use standard hyperparameters.

    Returns
    -------
    worst_feature: str
        Name of the feature best to be left out for training.

    new_metric: float
        Metric value achieved when leaving out worst feature.
    """
    # Initiate result list
    removed_feature = []
    new_metric = []

    # Iterate over feature list
    for feature in feature_list:
        _, metrics = train_model(
            algorithm,
            setup,
            feature_list=[feat for feat in feature_list if feat != feature],
            hyperparams=hyperparams,
        )
        removed_feature.append(feature)
        new_metric.append(metrics[metric].values[0])

    # Retrieve worst feature and metric
    new_metric_max = max(new_metric)
    max_index = new_metric.index(new_metric_max)
    worst_feature = removed_feature[max_index]

    return worst_feature, new_metric_max
