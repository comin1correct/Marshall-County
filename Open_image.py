"""This is a docstring - required by PEP 257 -
    Source: Automating Instagram with Python and Selenium - EuroPython2017

    This script is used to parse IDX - webserver appication for matching
    oil and gas leases, then provide them to the google Vision API to
    update current records.
"""
from Vision_URL import myVision
from selenium import webdriver
# error on action chains with out import
from selenium.webdriver.common.action_chains import ActionChains
# handling new window - see method: new_window()
#from selenium.webdriver.support import expected_conditions as EC
# waits - else it fails to load data
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class MarshallCounty():
    """This is a docstring - required by PEP 257"""
    def __init__(self, web_address):
        # starting a new browser session
        self.browser = webdriver.Chrome()
        self.address = web_address
        self.image_urls = []

    def open_to_site(self):
        """Using selenium to open site"""
        self.browser.get(self.address)

    def input_last(self, last_name):
        """Search IDX base on last name"""
        # find the input and data entered
        # note: had to enable Right-Clicking on Individual Sites with a Bit of Your Own JavaScript
        # https://www.howtogeek.com/248731/how-to-enable-right-clicking-on-web-sites-that-block-it/
        # Working: javascript:void(document.oncontextmenu=null);
        lname_input = self.browser.find_element_by_xpath \
            ('//*[@id="CallFormPanel_contentSplitter_CallToolPanel_txtLname_I"]')

        ActionChains(self.browser) \
            .move_to_element(lname_input).click() \
            .send_keys(last_name) \
            .perform()

    def preform_search(self):
        """running the query and waiting for results to process"""
        # find the search index button and click it
        search_index = self.browser.find_element_by_xpath(
            '//*[@id="CallFormPanel_contentSplitter_CallToolPanel_rc_T0G2I2_LI"]')

        ActionChains(self.browser) \
            .move_to_element(search_index) \
            .click().perform()

        # Wait for AJAX to load before parsing data
        self.browser.implicitly_wait(5)

    def parse_data(self):
        """Analysing the data"""
        ##counter = 1  --- for use with spreadsheets
        for i in range(0, 100):
            sub = self.browser.find_element_by_xpath(
                # Description
                '//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow' + str(i) + '"]/td[5]')
            # print(sub.get_attribute("innerHTML"))
            sub.click()
            if sub.get_attribute("innerHTML") == "OIL &amp; GAS LEASE":
                self.new_window(i)

                name = self.browser.find_element_by_xpath\
                ('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow'
                 + str(i) + '"]/td[9]')

                description = self.browser.find_element_by_xpath\
                    ('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow'
                     + str(i) + '"]/td[10]')

                instrument = self.browser.find_element_by_xpath\
                    ('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow'
                     + str(i) + '"]/td[11]')

        # make sure the browser stays open for 20 seconds
        sleep(20)
        # clean exit
        self.browser.close()

    def new_window(self, counter):
        """Handling the new windows and retriving url for Vision API"""
        window_before_click = self.browser.window_handles[0]

        # clicking a tag
        self.browser.find_element_by_xpath\
            ('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow' + str(
                counter) + '"]/td/a').click()
        # WebDriverWait(self.browser,10).until(EC.number_of_windows_to_be(1))
        new_window = self.browser.window_handles[1]
        # switching to new window
        self.browser.switch_to_window(new_window)
        self.javascript_url()
        # close new window
        sleep(4)
        self.browser.close()
        # switch back to main window
        self.browser.switch_to_window(window_before_click)

    def javascript_url(self):
        """method to get URL to image"""
        # Retrieving url via javascript -- return is required to set variable
        url = self.browser.execute_script("return document.images[50].getAttribute('src')")
        # --- look like the link expires
        self.image_urls.append("URL: http://129.71.117.225{}".format(url))


##       ACTIVATE VISION API
##        new = myVision()
##        new.detect_document_uri("http://129.71.117.225{}".format(url))


def main():
    """Running"""
    run1 = MarshallCounty('http://129.71.117.225/')
    run1.open_to_site()
    run1.input_last('smith')
    run1.preform_search()
    run1.parse_data()
    for item in run1.image_urls:
        print(item)

if __name__ == '__main__':
    main()
