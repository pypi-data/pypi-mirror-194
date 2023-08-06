import glob
import os
import time

import win32com.client as win32


def remove_meta():
    link_log = open(file="links_log.txt", mode="w", encoding="utf-8")
    stop_word = "stresstest_lab"

    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    filetypes = ["**/*.xls", "**/*.xlsx", "**/*.xlsm"]

    for filetype in filetypes:
        for file in glob.iglob(filetype, recursive=True):
            absolute_path = os.path.abspath(file)
            print("Working with file:", absolute_path)
            try:
                wb = excel.Workbooks.Open(absolute_path)
                time.sleep(1)
            except:
                print("Error occurred when tried to open file:", absolute_path)
                continue

            workbook_links = wb.LinkSources()
            if workbook_links:
                bad_links = list(filter(lambda link: stop_word in link, workbook_links))
                if bad_links:
                    link_log.write(f"In file {absolute_path} found bad links:\n")
                    for bad_link in bad_links:
                        link_log.write(f"- {bad_link}\n")

            wb.RemovePersonalInformation = True
            wb.Save()
            wb.Close()

    link_log.close()
    excel.Quit()
