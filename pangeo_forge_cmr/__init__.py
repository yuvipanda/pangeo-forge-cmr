from cmr import GranuleQuery
from pangeo_forge_recipes.patterns import FilePattern, pattern_from_file_sequence
import logging

# We only operate during the *parse* time, so output to the pangeo force *parsing* log
log = logging.getLogger("pangeo_forge_recipes.parse")


def get_cmr_granule_links(shortname: str, version: str, limit: int = 0):
    """
    Return downloadable files for given CMR shortname and given version

    limit specifies number of granules to fetch. Set to 0 to retrieve
    all of them.
    """
    # Get a list of granules for this collection from CMR
    api_granule = GranuleQuery()
    api_granule.parameters(
        short_name=shortname,
        version=version
    )
    api_granule_downloadable = api_granule.downloadable()

    if limit == 0:
        granules = api_granule.get_all()
    else:
        granules = api_granule.get(limit)

    log.info(f'Looking for HTTP downloadable files from CMR for {shortname} version {version}')

    # Find list of all downloadable URLs for the granules
    downloadable_urls = []
    for granule in granules:
        for link in granule['links']:
            # Find downloadable data URL
            if link['rel'] == 'http://esipfed.org/ns/fedsearch/1.1/data#':

                log.debug(f'Found downloadable granule URL {link["href"]} for {shortname}')
                downloadable_urls.append(link['href'])
                break
        else:
            log.debug(f"No downloadable URL found in {granule}")

    log.info(f'Found {len(downloadable_urls)} files from CMR for {shortname} version {version}')
    return downloadable_urls


def files_from_cmr(shortname: str, version: str, concat_dim, nitems_per_file=None, **kwargs) -> FilePattern:
    """
    Return a filepattern with *all* downloadable granules for given shortname & version

    Rest of parameters are passed straight to pangeo_forge_recipes.patterns.pattern_from_file_seqeuence
    convenience method.
    """
    urls = get_cmr_granule_links(shortname, version)
    return pattern_from_file_sequence(
        urls,
        concat_dim,
        nitems_per_file,
        **kwargs
    )
