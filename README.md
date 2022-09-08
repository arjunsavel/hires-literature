# hires-literature

[![Generate plots](https://github.com/arjunsavel/hires-literature/actions/workflows/generate_plots.yml/badge.svg)](https://github.com/arjunsavel/hires-literature/actions/workflows/generate_plots.yml) [![Scrape ArXiv](https://github.com/arjunsavel/hires-literature/actions/workflows/scrape_arxiv.yml/badge.svg)](https://github.com/arjunsavel/hires-literature/actions/workflows/scrape_arxiv.yml) [![DOI](https://zenodo.org/badge/527634198.svg)](https://zenodo.org/badge/latestdoi/527634198)


This repo aims to contain all papers related to high-resolution spectroscopy of exoplanet atmospheres — theory and observation. The status of this work can be tracked in the [related project](https://github.com/users/arjunsavel/projects/1). 

The notebook is for exploratory plots and explicit workings-through. Also, new entries are currently added via the notebook (though this will soon change!).

The below data fields for *observational* works are slated to be tracked:
- [x] Lead author
- [x] Target name
- [x] Publication year
- [x] Detected species
- [ ] Non-detected species
- [ ] Tellurics correction method
- [ ] Analysis method (e.g., retrieval, grid of paramaterized forward models)
- [ ] Paper URL
- [x] Detection significance
- [ ] Whether the data is newly acquired or archival
- [ ] Associated Doppler shifts of detected species
- [ ] Code used for forward model, if applicable
- [x] Instrument used for detections
- [ ] Comments (e.g., author caveats)

The below data fields for *theoretical* works are slated to be tracked:
- [x] Lead author
- [x] Title
- [x] Publication year
- [x] Number of dimensions considered
- [x] Paper URL
- [ ] Comments (e.g., author caveats)
- [ ] Subfield tags (e.g., astrobiology)


The below data fields for *instrument* are slated to be tracked:
- [ ] Resolution
- [ ] Wavelength min
- [ ] Wavelength max
- [ ] First light
- [ ] Normal telescope it's mounted in
- [ ] Location of that telescope
- [ ] Altitude of that telescope
- [ ] Comments (e.g., other available modes)

In addition to the raw data tracking, this repository will generate the following plots:
- [x] Number of theory papers over time
- [x] Number of theory papers that are multidimensional
- [x] Number of species observed over time
- [x] Variety of species observed per planet
