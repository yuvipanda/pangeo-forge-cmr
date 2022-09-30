from cmr import GranuleQuery


def get_cmr_granule_links(shortname: str, limit: int = 0):
    """
    Return downloadable files for given CMR shortname

    limit specifies number of granules to fetch. Set to 0 to retrieve
    all of them.
    """
    # Get a list of granules for this collection from CMR
    api_granule = GranuleQuery()
    api_granule.parameters(
        short_name=shortname
    )
    # FIXME: Use logging instead here
    # We use print statements to provide debug output as we go laong
    print(f'number of granules: {api_granule.hits()}')
    api_granule_downloadable = api_granule.downloadable()
    print(f'number of downloadable granules: f{api_granule_downloadable.downloadable().hits()}')

    if limit == 0:
        granules = api_granule.get_all()
    else:
        granules = api_granule.get(limit)

    # Find list of all downloadable URLs for the granules
    downloadable_urls = []
    for granule in granules:
        for link in granule['links']:
            # Find downloadable data URL
            if link['rel'] == 'http://esipfed.org/ns/fedsearch/1.1/data#':
                print('adding url: ' + link['href'])
                downloadable_urls.append(link['href'])
                break
        else:
            # FIXME: Provide useful info here
            print('no downloadable url found')

    return downloadable_urls
