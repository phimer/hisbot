from selenium import webdriver
import time
import smtplib
from twilio.rest import Client
from termcolor import colored


from login_info import login, pw
from login_info import sending_email, sending_email_pw
from login_info import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from login_info import receiving_email, my_phone, twilio_phone

# add passed courses for initial startup, script will save new passed courses automaticaly
passed_courses_list = ['Prüfungsleistung:Wirtschaftsinformatik', 'Prüfungsleistung: Englisch', 'Prüfungsleistung: Wirtschaftsinformatik', 'Prüfungsleistung: Objektorientierte Programmierung', 'Prüfungsleistung: Betriebswirtschaftslehre 1+2', 'Prüfungsleistung: E-Business', 'Prüfungsleistung: Datenbanken', 'Prüfungsleistung: Analysis', 'Prüfungsleistung: Data Warehouses', 'Rechnungswesen', "Wirtschaftsprivatrecht",
                       'Datenbanken', 'Analysis', 'Englisch', 'Data Warehouses', 'E-Business', 'Bisher erbrachte Credits und vorläufige Durchschnittsnote der PO-Version 6215', 'Prüfungsleistung: Software Engineering', 'Software Engineering', 'Statistik', 'Objektorientierte Programmierung', 'Wirtschaftsinformatik', 'Betriebswirtschaftslehre', 'Intercultural Communication', 'Prüfungsleistung: Intercultural Communication', 'Algebra', 'Prüfungsleistung: Algebra', 'Krisenmanagement - Ursachen, Vorbeugung und Bewältigung', 'Interdisziplinäres Studium Generale']


# # add your login information
# login = 'YOUR HIS LOGIN NUMBER'
# pw = 'YOUR HIS PW'
# receiving_email = 'YOUREMAILHERE'  # can be any email address
# # works with others, email function is configured for gmail - you have to "Allow less secure apps to access your account" in gmail - https://myaccount.google.com/lesssecureapps
# sending_email = 'YOUR GMAIL ADDRESS HERE'
# sending_email_pw = 'YOUR PASSWORD OF THE SENDING EMAIL'
# twilio_phone = '' #FORMAT: 'whatsapp:+491773234234'
# my_phone = ''

def whatsapp(neues_modul, note):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    text_message = f'{neues_modul} - {note}'

    client.messages.create(from_=twilio_phone,
                           body=text_message,
                           to=my_phone)


def email(modul_name, note):

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sending_email, sending_email_pw)

        subject = f'{modul_name} jetzt online'
        body = f'{modul_name} - {note}'

        msg = f'Subject: {subject}\n\n{body}'
        # msg = f'Subject: neue Note\n\nNeue Note im HiS {modul_name}'

        # (from, to, msg)
        smtp.sendmail(sending_email, receiving_email, msg)

    print(colored('E-Mail sent', 'green'))


class Bot():

    check = False

    def __init__(self):
        self.driver = webdriver.Chrome()

    def main(self):

        print(
            colored(f'{time.localtime().tm_hour}:{time.localtime().tm_min}', 'cyan'))

        try:

            self.driver.get(
                'https://his-www.dv.fh-frankfurt.de/qisserver/rds?state=user&type=0')
            matrikelNummer = self.driver.find_element_by_xpath(
                '//*[@id="asdf"]')
            matrikelNummer.send_keys(login)

            password = self.driver.find_element_by_xpath('//*[@id="fdsa"]')
            password.send_keys(pw)

            login_button = self.driver.find_element_by_xpath(
                '//*[@id="loginForm:login"]')
            login_button.click()

            prüfungsverwaltung = self.driver.find_element_by_xpath(
                '//*[@id="makronavigation"]/ul/li[3]/a')
            prüfungsverwaltung.click()
            leistungsübersicht = self.driver.find_element_by_xpath(
                '//*[@id="wrapper"]/div[6]/div[2]/div/form/div/ul/li[4]/a')
            leistungsübersicht.click()

            self.driver.find_element_by_xpath(
                '//*[@id="wrapper"]/div[6]/div[2]/form/ul/li/a[1]').click()
            self.driver.find_element_by_xpath(
                '//*[@id="wrapper"]/div[6]/div[2]/form/ul/li/ul/li/a[1]').click()

            # ects = self.driver.find_element_by_xpath(
            # '//*[@id="wrapper"]/div[6]/div[2]/form/table[2]/tbody/tr[14]/td[6]')

            name_list = []

            for i in range(1, 40):

                try:
                    modul_name = str(self.driver.find_element_by_xpath(
                        f'//*[@id="wrapper"]/div[6]/div[2]/form/table[2]/tbody/tr[{i}]/td[2]').text)

                    if modul_name not in passed_courses_list:

                        name_list.append(modul_name)

                except:
                    # print(f'exception {i} triggered')
                    pass

            spl = ''  # split
            if len(name_list) > 0:
                neues_modul = name_list.__getitem__(0)

                passed_courses_list.append(neues_modul)
                # passed_courses_list.append(f'Prüfungsleistung: {neues_modul}')

                # split
                spl = neues_modul[18:]
                passed_courses_list.append(spl)
                # sometimes theres not space after Prüfungsleistung:
                spl2 = neues_modul[17:]
                passed_courses_list.append(spl2)

            # note zu neuem modul, loop um richtiges i zu finden, um note zu modul zu bekommen
            for i in range(1, 40):

                try:
                    modul_name = str(self.driver.find_element_by_xpath(
                        f'//*[@id="wrapper"]/div[6]/div[2]/form/table[2]/tbody/tr[{i}]/td[2]').text)

                    if modul_name == neues_modul:

                        note = self.driver.find_element_by_xpath(
                            f'//*[@id="wrapper"]/div[6]/div[2]/form/table[2]/tbody/tr[{i}]/td[4]').text

                except:
                    # print(f'bottom exception {i} triggered')
                    pass

            if len(name_list) > 0:
                print(colored(f"NEUE NOTE IM HIS - {spl} - {note}", "red"))
                email(spl, note)
                # whatsapp(spl, note)
            else:
                print("keine neue Note")

        except:
            print(colored('big exception triggered', 'red'))
            # pass

        self.driver.close()


while(True):
    bot = Bot()
    bot.main()
    time.sleep(600)  # checks every 10 minutes

# bot = Bot()
# bot.main()
