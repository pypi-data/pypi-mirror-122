from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.product import abg_residue_nitrogen, abg_total_residue_nitrogen_content
from hestia_earth.models.utils.dataCompleteness import _is_term_type_complete
from hestia_earth.models.utils.cycle import valid_site_type
from . import MODEL

TERM_ID = 'nh3ToAirCropResidueDecomposition'


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(residue_nitrogen: float, nitrogenContent: float):
    a = a = min([
        max([(0.38 * 1000 * nitrogenContent/100 - 5.44) / 100, 0]),
        17 / 100
    ])
    value = a * residue_nitrogen * 1.21589
    return [_emission(value)] if nitrogenContent > 5 else [_emission(0)]


def _should_run(cycle: dict):
    products = cycle.get('products', [])
    residue_nitrogen = abg_residue_nitrogen(products)
    abg_residue_nitrogen_content = abg_total_residue_nitrogen_content(products)

    debugRequirements(model=MODEL, term=TERM_ID,
                      residue_nitrogen=residue_nitrogen,
                      abg_residue_nitrogen_content=abg_residue_nitrogen_content)

    should_run = all([
        valid_site_type(cycle),
        residue_nitrogen > 0 or _is_term_type_complete(cycle, {'termType': TermTermType.CROPRESIDUE.value})
    ])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, residue_nitrogen, abg_residue_nitrogen_content


def run(cycle: dict):
    should_run, residue_nitrogen, nitrogenContent = _should_run(cycle)
    return _run(residue_nitrogen, nitrogenContent) if should_run else []
