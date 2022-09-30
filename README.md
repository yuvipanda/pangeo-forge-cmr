# pangeo-forge-cmr

Small library that integrates NASA's [Common Metadata Repository](https://www.earthdata.nasa.gov/eosdis/science-system-description/eosdis-components/cmr)
(CMR) with [pangeo-forge-recipes](https://github.com/pangeo-forge/pangeo-forge-recipes).
The goal is to help make pangeo-forge recipes that use CMR for getting raw data.

## Example

```python
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe
from pangeo_forge_cmr import get_cmr_granules_links

# Get the GPM IMERG Late Precipitation Daily data
shortname = 'GPM_3IMERGDL'

recipe = XarrayZarrRecipe( # We are making Zarr, could be something else too
    pattern_from_file_sequence(
        get_cmr_granules_links(shortname), # Provide a list of files by querying CMR
        concat_dim='time',  # Describe how the dataset is chunked
    ),
)
```