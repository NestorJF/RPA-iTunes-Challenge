from importlib.resources import path
from libraries.common import act_on_element, capture_page_screenshot, log_message, check_file_download_complete, files
from config import OUTPUT_FOLDER, tabs_dict

class ITunes():

    def __init__(self, rpa_selenium_instance, credentials: dict):
        self.browser = rpa_selenium_instance
        self.itunes_url = credentials["url"]
        self.data_dict_list = []


    def extract_information(self):
        """
        Extracts cast information from the itunes website and goes to each artist to extract their movies.
        """
        tabs_dict['LordofTheRingiTunesPage'] = len(tabs_dict)
        cast_elements = act_on_element('//div[@class="l-row cast-list"]//dd/a', "find_elements")[:5]
        self.browser.execute_javascript("window.open()")
        self.browser.switch_window(locator="NEW")
        tabs_dict['ArtistiTunesPage'] = len(tabs_dict)

        for cast_element in cast_elements:
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict['LordofTheRingiTunesPage']])

            artist_name = cast_element.text
            artist_link = cast_element.get_attribute("href")

            artist_found = [artist for artist in self.data_dict_list if artist['artist_name'] == artist_name]
            if len(artist_found) == 0:
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict['ArtistiTunesPage']])
                self.browser.go_to(artist_link)

                cast_data_dict = {
                    "artist_name": artist_name,
                    "movies": self.get_movies_of_artist()
                }
                self.data_dict_list.append(cast_data_dict)

                #self.browser.execute_javascript("window.close()")
        
    
    def get_movies_of_artist(self):
        """
        Extracts movies (name and genre) of the artist page.
        """
        movies_elements = act_on_element('//section[descendant::h2[@class="section__headline" and text() = "Movies"]]/div[@class="l-row l-row--peek"]/a', 'find_elements')
        movies_list = []
        for movie in movies_elements:
            movies_data_dict = {
                "Name": movie.find_element_by_xpath('.//div[@class="we-lockup__title "]/div').text,
                "Genre": movie.find_element_by_xpath('.//div[@class="we-truncate we-truncate--single-line  we-lockup__subtitle"]').text
            }
            movies_list.append(movies_data_dict)
        
        return movies_list

    def write_data_excel(self):
        """
        Writes the data extracted to an excel file. Each sheet belongs to an artist.
        """
        files.create_workbook(path = "{}/iTunes_data.xlsx".format(OUTPUT_FOLDER))
        files.remove_worksheet(name="Sheet")
        for artist_dict in self.data_dict_list:
            files.create_worksheet(name = artist_dict['artist_name'], content = None, exist_ok = False, header = False)
            files.append_rows_to_worksheet(artist_dict['movies'], name = artist_dict['artist_name'], header = True, start = None)
        files.save_workbook(path = None)
        files.close_workbook()
        
