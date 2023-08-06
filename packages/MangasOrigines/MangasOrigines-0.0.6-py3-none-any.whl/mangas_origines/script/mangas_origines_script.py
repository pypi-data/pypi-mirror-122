from mangas_origines.exceptions.exceptions import ScanNotFound, MangasOriginesNotAvailable
from mangas_origines.mangas_origines import MangasOrigines
from mangas_origines.script import arguments_builder
from mangas_origines import utils
import urllib.parse
import aiofiles
import asyncio
import aiohttp
import cursor
import json
import halo
import os


class Update:
    def __init__(self):
        self.images_url_len = 0
        self.images_downloaded = 0
        self.to_download = []
        self.scan = None

    async def generate_json(self, spinner: halo.Halo, path: str):
        spinner.text = 'Generate JSON...'
        spinner.start()

        json_content = {
            'scan_id': self.scan.scan_id, 'name_id': self.scan.name_id, 'url': self.scan.url,
            'genres': self.scan.genres, 'types': self.scan.types, 'title': self.scan.title,
            'year_of_release': self.scan.year_of_release, 'image_url': self.scan.image_url,
            'author_name': self.scan.author_name, 'author_url': self.scan.author_url,
            'artist_name': self.scan.artist_name, 'artist_url': self.scan.artist_url,
            'notes': self.scan.notes, 'ratting_count': self.scan.ratting_count,
            'has_seasons': self.scan.has_seasons
        }

        async with aiofiles.open(path + 'infos.json', 'wb') as f:
            await f.write(json.dumps(json_content, indent=4, ensure_ascii=False).encode('utf-8'))

        async with aiohttp.ClientSession(headers=self.scan.headers) as client_session:
            async with client_session.get(urllib.parse.quote(self.scan.image_url, safe='://')) as r:
                async with aiofiles.open(path + 'icon.png', 'wb') as f:
                    async for data in r.content.iter_chunked(1024):
                        await f.write(data)
        spinner.stop()
    
    async def download(self, element: list):
        file_name = os.path.basename(element[0])

        utils.create_folder(element[2])
        if os.path.isfile(element[1] + file_name) is False:
            async with aiohttp.ClientSession(headers=self.scan.headers) as client_session:
                try:
                    async with client_session.get(urllib.parse.quote(element[0], safe='://'), timeout=800) as r:
                        async with aiofiles.open(element[2] + file_name, 'wb') as f:
                            try:
                                async for data in r.content.iter_chunked(1024):
                                    await f.write(data)
                            except aiohttp.ClientPayloadError:
                                return utils.print_error(f'Incorrect link: {element[0]}')
                except asyncio.TimeoutError:
                    return utils.print_error(f'Timeout: {element[0]}')
            utils.create_folder(element[1])
            os.rename(element[2] + file_name, element[1] + file_name)
        self.images_downloaded += 1

        utils.progress_bar(self.images_downloaded, self.images_url_len, 'Download all images')
        self.to_download.remove(element)
        
    async def get_scan_pictures(self, spinner: halo.Halo, scan: str, path: str, temp_path: str, force_check: bool):
        try:
            if 'mangas-origines.fr' in scan:
                self.scan = await MangasOrigines().get_scan_by_url(scan)
            else:
                self.scan = await MangasOrigines().get_scan_by_name_id(scan)
        except ScanNotFound:
            spinner.stop()
            return utils.print_error(f"I can't found scan: {scan}!")
        except MangasOriginesNotAvailable as e:
            spinner.stop()
            return utils.print_error(f'Mangas Origines is not available, error: {e.error_code}!')

        for x in self.scan.chapters_url:
            chapter = self.scan.get_chapter_name(x)

            if self.scan.has_seasons:
                season = self.scan.get_chapter_season(x)
                gen_path = path + season + os.sep + chapter + os.sep
                gen_temp_path = temp_path + season + os.sep + chapter + os.sep
            else:
                chapter = self.scan.get_chapter_name(x)
                gen_path = path + chapter + os.sep
                gen_temp_path = temp_path + chapter + os.sep

            if os.path.exists(gen_path) is False or force_check:
                get_chapter = await self.scan.get_chapter_by_url(x)
                for x1 in get_chapter.images_url:
                    self.to_download.append([x1, gen_path, gen_temp_path])
                self.images_url_len += len(get_chapter.images_url)

    async def update(self, command_return: dict):
        arguments = command_return['args']
        arg_index = arguments.index('-S')
        force_check = '--check' in arguments
        generate_json = '--generate-json' in arguments

        if len(arguments) >= arg_index + 2:
            if len(arguments) >= arg_index + 4:
                spinner = halo.Halo(text='Loading', spinner='dots')
                spinner.start()

                path_to_clean = arguments[arguments.index('-P') + 1]
                path = path_to_clean if path_to_clean[-1] == os.sep else path_to_clean + os.sep
                temp_path = path + 'temp' + os.sep

                if os.access(os.path.dirname(path), os.W_OK) is False:
                    spinner.stop()
                    return utils.print_error("I can't use this folder (bad permission, or incorrect path).")
                utils.create_folder(path)

                await self.get_scan_pictures(spinner, arguments[arg_index + 1], path, temp_path, force_check)
                spinner.stop()

                if generate_json:
                    await self.generate_json(spinner, path)

                if not self.to_download:
                    utils.delete_folder(temp_path)
                    return print('Nothing to download.')

                cursor.hide()
                utils.progress_bar(0, self.images_url_len, 'Download all images')
                while self.to_download:
                    await utils.limit_tasks(15, *[self.download(element) for element in self.to_download])
                cursor.show()

                utils.delete_folder(temp_path)
                utils.clear_line()

                print('\r\033[1mDownload complete!\033[0m')
            else:
                utils.print_error('You must enter download path (with -P option).')
        else:
            utils.print_error('You must enter scan url/name.')

    async def update_all_scans(self, command_return: dict):
        arguments = command_return['args']
        arg_index = arguments.index('-U')
        force_check = '--check' in arguments

        if len(arguments) >= arg_index + 2:
            spinner = halo.Halo(text='Loading', spinner='dots')
            spinner.start()

            path = arguments[arg_index + 1] if arguments[arg_index + 1][-1] == os.sep else arguments[arg_index + 1] + os.sep

            if os.access(os.path.dirname(path), os.W_OK) is False:
                spinner.stop()
                return utils.print_error("I can't use this folder (bad permission, or incorrect path).")

            total = len(os.listdir(path))
            ignored = 0
            json_not_found = 0
            json_not_found_list = []

            for folder in os.listdir(path):
                path_gen = path + folder + os.sep
                path_temp_gen = path_gen + 'temp' + os.sep
                if os.path.exists(path_gen + 'infos.json'):
                    async with aiofiles.open(path_gen + 'infos.json', 'rb') as f:
                        text = await f.read()
                    text_parsed = json.loads(text)
                    if 'name_id' in text_parsed:
                        await self.get_scan_pictures(spinner, text_parsed['name_id'], path_gen, path_temp_gen, force_check)
                    else:
                        ignored += 1
                else:
                    json_not_found_list.append(path_gen)
                    json_not_found += 1

            spinner.stop()

            if not self.to_download:
                return print('Nothing to download.')

            cursor.hide()
            utils.progress_bar(0, self.images_url_len, 'Download all images')
            while self.to_download:
                await utils.limit_tasks(15, *[self.download(element) for element in self.to_download])
            cursor.show()

            utils.clear_line()

            print(
                f'\r\033[1mDownload complete ({total - ignored} downloaded, {ignored} ignored, {json_not_found} json not founded)!\033[0m'
            )

        else:
            utils.print_error('You must enter path to check.')


async def get_infos(command_return: dict):
    arguments = command_return['args']
    arg_index = arguments.index('-I')

    if arg_index + 2 == len(arguments):
        spinner = halo.Halo(text='Loading', spinner='dots')
        spinner.start()

        try:
            scan = await MangasOrigines().get_scan_by_name_id(arguments[arg_index + 1])
        except ScanNotFound:
            spinner.stop()
            return utils.print_error(f"I can't found scan: {arguments[arg_index + 1]}!")
        except MangasOriginesNotAvailable as e:
            spinner.stop()
            return utils.print_error(f'Mangas Origines is not available, error: {e.error_code}!')

        scan_infos_text = f"\n{scan.title}'s infos:\n"
        scan_infos_text += f"   ID: {scan.scan_id}\n"
        scan_infos_text += f"   Author: {'No information' if scan.year_of_release is None else scan.author_name} - {'No information' if scan.year_of_release is None else scan.author_url}\n"
        scan_infos_text += f"   Artiste: {'No information' if scan.year_of_release is None else scan.artist_name} - {'No information' if scan.year_of_release is None else scan.artist_url}\n"
        genres_list = ', '.join([x for x in scan.genres])
        scan_infos_text += f"   Genres: {genres_list}\n"
        scan_types = ', '.join([x for x in scan.types])
        scan_infos_text += f"   Types: {scan_types}\n"
        scan_infos_text += f"   Year of release: {'No information' if scan.year_of_release is None else scan.year_of_release}\n"
        scan_infos_text += f"   Chapters number: {len(scan.chapters_url)}\n"
        scan_infos_text += f"   Has season: {'Yes' if scan.has_seasons else 'No'}\n"
        scan_infos_text += f"   Notes: {scan.notes}\n"
        scan_infos_text += f"   Ratting count: {scan.ratting_count}\n"
        spinner.stop()
        print(scan_infos_text)
    else:
        utils.print_error('You must enter scan url/name.')


def get_version(command_return: dict):
    from mangas_origines import __version__, __license__

    version_text = f'\033[1mMangasOrigines {__version__}\033[0m\n'
    version_text += f'Created by \033[1mAsthowen\033[0m - \033[1mcontact@asthowen.fr\033[0m\n'
    version_text += f'License: \033[1m{__license__}\033[0m'

    print(version_text)


def start():
    parser = arguments_builder.ArgumentsBuilder('A script to make some things on mangas-origines.fr.')

    parser.add_argument(
        '-S', action=Update().update, description='Download scan.', command_usage='-S scan_id -P path [--check, --generate-json]'
    )
    parser.add_argument('-U', action=Update().update_all_scans, description='Update all scans in folder.', command_usage='-U path')
    parser.add_argument('-I', action=get_infos, description='Get scan infos.', command_usage='-I scan_id')
    parser.add_argument('-V', action=get_version, description='Get version infos.', command_usage='-V')

    try:
        parser.build()
    except KeyboardInterrupt:
        cursor.show()
        utils.clear_line()
        utils.print_error('Script stopped by user.')


if __name__ == '__main__':
    start()
