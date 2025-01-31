import logging

logger = logging.getLogger(__name__)


def get_trait_counts(traits_list):
    """
    Count occurrences of each trait from the given list.
    :param traits_list: List of trait abbreviations.
    :return: Dictionary with trait counts.
    """
    trait_counts = {"MU": 0, "KL": 0, "IN": 0, "CH": 0, "FF": 0, "GE": 0, "KO": 0, "KK": 0}

    try:
        for trait in traits_list:
            if trait in trait_counts:
                trait_counts[trait] += 1
            else:
                logger.warning(f"Unexpected trait abbreviation found: {trait}")

    except Exception as e:
        logger.error(f"Error processing trait counts: {e}")

    return trait_counts
