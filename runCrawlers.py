from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import tkinter as tk

window = None
entry = None


def handle_click(event):
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    movie_name = entry.get()
    window.destroy()
    for spider_name in process.spider_loader.list():
        setting.update({
            'FEED_FORMAT': 'json',
            'FEED_URI': spider_name + ".json"
        })
        configure_logging(settings=setting, install_root_handler=False)
        print("Running spider %s" % spider_name)
        process.crawl(spider_name, input='inputargument', movieName=movie_name)

    process.start()
    print("Completed")


def create_window():
    global window
    global entry
    window = tk.Tk()
    window.geometry("600x600")
    window.title("Movie/Series Title")
    label = tk.Label(text="Which Movie/Series do you want to find?")
    entry = tk.Entry()
    button = tk.Button(text="Find")
    button.bind("<Button-1>", handle_click)
    window.bind("<Return>", handle_click)
    label.pack()
    entry.pack()
    entry.focus_set()
    button.pack()
    window.lift()
    window.attributes("-topmost", True)
    window.mainloop()


create_window()
