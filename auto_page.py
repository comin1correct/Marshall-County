#Automating Instagram with Python and Selenium - EuroPython2017
from time import sleep
from selenium import webdriver

# waits - else it fails to load data
from selenium.webdriver.support.ui import WebDriverWait

#error on action chains with out import
from selenium.webdriver.common.action_chains import ActionChains

#excel(xls)
import xlwt

class MarshallCounty():

    def __init__(self, web_address,sheet_name):
        # starting a new browser session
        self.browser = webdriver.Chrome()
        self.address = web_address
        # create a blank spreadsheet file
        self.wb = xlwt.Workbook()
        # create a sheet within the file
        self.ws = self.wb.add_sheet(sheet_name)

    def open_to_site(self):
        self.browser.get(self.address)


    def input_last(self,last_name):
        # find the input and data entered
        # note: had to enable Right-Clicking on Individual Sites with a Bit of Your Own JavaScript
        # https://www.howtogeek.com/248731/how-to-enable-right-clicking-on-web-sites-that-block-it/
        # Working: javascript:void(document.oncontextmenu=null);
        lname_input = self.browser.find_element_by_xpath\
            ('//*[@id="CallFormPanel_contentSplitter_CallToolPanel_txtLname_I"]')

        ActionChains(self.browser) \
            .move_to_element(lname_input).click() \
            .send_keys(last_name) \
            .perform()

    def preform_search(self):
        # find the search index button and click it
        search_index = self.browser.find_element_by_xpath(
            '//*[@id="CallFormPanel_contentSplitter_CallToolPanel_rc_T0G2I2_LI"]')

        ActionChains(self.browser) \
            .move_to_element(search_index) \
            .click().perform()

        # Wait for AJAX to load before parsing data
        self.browser.implicitly_wait(5)


    def parse_data(self):
        counter = 1
        #defining the headers
        self.ws.write(0,0,'Name')
        self.ws.write(0,1,'Description')
        self.ws.write(0,2,'Instrument No.')

        for i in range(0, 100):
            sub = self.browser.find_element_by_xpath(
                '//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow' + str(i) + '"]/td[8]')
            sub.click()
            if (sub.get_attribute("innerHTML") == "GRANTOR"):

                name = self.browser.find_element_by_xpath(
                    '//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow' + str(i) + '"]/td[9]')

                description = self.browser.find_element_by_xpath('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow'
                                                            + str(i) + '"]/td[10]')

                instrument = self.browser.find_element_by_xpath('//*[@id="CallFormPanel_contentSplitter_grd_DXDataRow'
                                                           + str(i) + '"]/td[11]')

                #data to spreadsheet
                self.ws.write(counter, 0, str(name.text))
                self.ws.write(counter, 1, str(description.text))
                self.ws.write(counter, 2, str(instrument.text))
                counter += 1

        self.wb.save("search1.xls")
        # make sure the browser stays open for 20 seconds
        sleep(20)
        # clean exit
        self.browser.close()



def main():
    m1 = MarshallCounty('http://129.71.117.225/','record_search')
    m1.open_to_site()
    m1.input_last('smith')
    m1.preform_search()
    m1.parse_data()

if __name__ == '__main__':
    main()


#TODO: - image OCR to search for lease numbers
#https://stackoverflow.com/questions/13437727/python-write-to-excel-spreadsheet
#https://www.youtube.com/watch?v=FbWnuO7GGBQ



#xpath to the container for image //*[@id="CallFormPanel_splitImage_mainSplit_1"]
#more specific //*[@id="CallFormPanel_splitImage_mainSplit_viewerPanel"]


#xpath to click image link  //*[@id="CallFormPanel_contentSplitter_grd_cell4_1_ScannedButton              486065"]
