from mangas_origines.exceptions.exceptions import WrongDomain, ScanNotFound, BadScanIdFormat, MangasOriginesNotAvailable
from mangas_origines.objects.scan import Scan
from mangas_origines import utils
from bs4 import BeautifulSoup
import aiohttp


class MangasOrigines:
    """
    A class used to centralize the functions of the client

    ...

    Attributes
    ----------
    headers : dict
        use of personalized headers for requests

    Methods
    -------
    __get_scan(scan_url: str)
        Create Scan object by URL of scan
    get_scan_by_url(scan_url)
        Get a scan by its URL
    get_scan_by_name_id(scan_name_id)
        Get a scan by its name id
    """

    def __init__(self, headers: dict = None):
        self.headers = headers

        if self.headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

        self.auth: Auth = None

    async def __get_scan(self, scan_url: str) -> Scan:
        """Create Scan object by URL of scan

        Parameters
        ----------
        scan_url : str
            The scan url.
            e.g: https://mangas-origines.fr/manga/martial-peak/

        Returns
        -------
        Scan
            a Scan object to get some infos or execute action about scan

        Raises
        ------
        WrongDomain
            If the scan URL is not the one of mangas-origines.fr.
        MangasOriginesNotAvailable
            If mangas-origines.fr is not accessible.
        ScanNotFound
            If the scan was not found.
        BadScanIdFormat
            If the scan ID is in an incorrect format.
        """
        if 'mangas-origines.fr' not in scan_url:
            raise WrongDomain()

        async with aiohttp.ClientSession(headers=self.headers) as client_session:
            async with client_session.get(scan_url) as r:
                if r.status != 200 and r.status != 404:
                    raise MangasOriginesNotAvailable(r.status)
                elif r.status == 404:
                    raise ScanNotFound(scan_url)

                bs = BeautifulSoup(await r.text(), 'html.parser')

                try:
                    scan_id_str = bs.find('input', {'class': 'rating-post-id'}).get('value')
                except AttributeError:
                    raise ScanNotFound(scan_url)

                try:
                    scan_id = int(scan_id_str)
                except ValueError:
                    raise BadScanIdFormat()

                try:
                    scan_name_id = scan_url.split('/')[4]
                    title = utils.truncate_emojis(bs.find('div', {'class': 'post-title'}).find('h1').text).strip()
                    scan_genres = {}
                    for x in bs.find('div', 'genres-content').find_all('a'):
                        scan_genres[x.text.strip()] = x.get('href')

                    scan_types = {}
                    for x in bs.find_all('div', 'post-content_item'):
                        if 'Type' in x.text.strip():
                            for x2 in x.find('div', 'summary-content').text.strip().split(', '):
                                scan_types[x2] = 'https://mangas-origines.fr/manga-genre/' + x2

                    year_of_release_div = bs.find('div', {'class': 'post-status'}).find('div', 'summary-content')
                    year_of_release = year_of_release_div.find(
                        'a'
                    ).text.strip() if 'Non renseigné' in year_of_release_div else None
                    summary_image = bs.find('div', {'class': 'summary_image'}).find('img').get('data-src')
                    author = bs.find('div', {'class': 'author-content'}).find('a')
                    author_name = None if author is None else author.text.strip()
                    author_url = None if author is None else author.get('href')
                    artist = bs.find('div', {'class': 'artist-content'}).find('a')
                    artist_name = None if artist is None else artist.text.strip()
                    artist_url = None if artist is None else artist.get('href')
                    notes = float(bs.find('span', 'total_votes').text.strip())
                    ratting_count_check = bs.find('span', {'id': 'countrate'})
                    ratting_count = None if ratting_count_check is None else int(ratting_count_check.text.strip().replace('avis', ''))
                except AttributeError:
                    raise ScanNotFound(scan_url)

                scan = Scan(
                    self.headers, scan_id, scan_name_id, scan_url, scan_genres, scan_types, title, year_of_release, summary_image, author_name, author_url,
                    artist_name, artist_url, notes, ratting_count
                )
                await scan.get_all_chapters_url()

                return scan

    async def get_scan_by_url(self, scan_url: str) -> Scan:
        """Get a scan by its URL

        Parameters
        ----------
        scan_url : str
            The scan url.
            e.g: https://mangas-origines.fr/manga/martial-peak/

        Returns
        -------
        Scan
            a Scan object to get some infos or execute action about scan
        """
        return await self.__get_scan(scan_url)

    async def get_scan_by_name_id(self, scan_name_id: str) -> Scan:
        """Get a scan by its name id

        Parameters
        ----------
        scan_name_id : str
            The scan name id.
            e.g: martial-peak

        Returns
        -------
        Scan
            a Scan object to get some infos or execute action about scan
        """
        return await self.__get_scan('https://mangas-origines.fr/manga/' + scan_name_id)
