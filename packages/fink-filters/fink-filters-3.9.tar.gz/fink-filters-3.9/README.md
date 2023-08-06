[![pypi](https://img.shields.io/pypi/v/fink-filters.svg)](https://pypi.python.org/pypi/fink-filters)
[![Sentinel](https://github.com/astrolabsoftware/fink-filters/workflows/Sentinel/badge.svg)](https://github.com/astrolabsoftware/fink-filters/actions?query=workflow%3ASentinel)
[![PEP8](https://github.com/astrolabsoftware/fink-filters/workflows/PEP8/badge.svg)](https://github.com/astrolabsoftware/fink-filters/actions?query=workflow%3APEP8)
[![codecov](https://codecov.io/gh/astrolabsoftware/fink-filters/branch/master/graph/badge.svg)](https://codecov.io/gh/astrolabsoftware/fink-filters)

# Fink filters

This repository contains filters used to flag only particular parts of the full stream to be distributed to Fink users. Available filters (i.e. topics) are:

- sn_candidates: alerts identified as SN candidates
- early_sn_candidates: alerts identified as Early SN Ia candidates
- microlensing_candidates: alerts identified as Microlensing event candidates
- sso_ztf_candiates: alerts identified as Solar System Object in the MPC database
- sso_fink_candidates: alerts identified as Solar System Object candidates by Fink
- rrlyr: alerts identified as RRLyr in the SIMBAD database
- kn_candidates: alerts identified as kilonova candidates (ML-based)
- early_kn_candidates: alerts identified as kilonova candidates (cut-based)
- rate_based_kn_candidates: alerts identified as kilonova candidates from a fast (> 0.3 mag/day) decay
- orphan_grb: alerts identified as orphan GRB
- tracklet_candidates: alerts belonging to a tracklet (likely space debris or satellite glint)
- simbad_candidates: alerts with counterpart in the SIMBAD database
- yso_candidates: alerts identified as Candidate_YSO or Candidate_TTau\* in the SIMBAD database.

## Fink alert classification

Based on the filters outputs (which rely on alert content), we infer a classification for each alert. We currently have hundreds of classes that can be found [online](https://fink-portal.org/api/v1/classes). You can find the implementation of the classification method in [classification.py](fink_filters/classification.py), but the rule of thumb is:

1. if an alert has not been flagged by any of the filters, it is tagged as `Unknown`
2. if an alert has a counterpart in the SIMBAD database, its classification is the one from SIMBAD.
3. if an alert has been flagged by one filter, its classification is given by the filter (`Early SN Ia candidate`, `KN candidate`, `SSO candidate`, etc.)
4. if an alert has been flagged by more than one filter (except the SIMBAD one), it is tagged as `Ambiguous`.

Note that this classification is subject to change over time, as we learn new things or when new filters are created. The classification method is versioned (fink-filters version), so that users can track the change. Note that all the filters are not considered for the classification.

### Alert vs object classification

An object on the sky can emit several alerts, and based on available information on each alert, the classification can vary from one alert to another. We do not provide an _object_ classification. This is up to the user to decide on the nature of the object based on the list of alert classifications.

## How to contribute?

Learn how to [design](https://fink-broker.readthedocs.io/en/latest/tutorials/create-filters/) your filter, to integrate it inside the Fink broker, and redirect alert streams at your home.

## Installation

If you want to install the package (broker deployment), you can just pip it:

```
pip install fink_filters
```
