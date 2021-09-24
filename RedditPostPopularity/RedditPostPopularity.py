"""
    Plots upvotes and comments over 20sec period.
    TODO:
        try, except statement for reading in file
        Keep plotted data tidy
        Clean up code
        Prediction Plot?
"""

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from selenium import webdriver

WEB_DRIVER = "WEB DRIVER PATH"
driver = webdriver.Chrome(WEB_DRIVER)
i = 0

fig, (ax1, ax2) = plt.subplots(2)

while True:
    driver.get("REDDIT POST URL")
    upvotes = driver.find_element_by_xpath('//*[@id="vote-arrows-t3_ptxf44"]/div')
    comments = driver.find_element_by_class_name("FHCV02u6Cp2zYL0fhQPsO")
    upvotes_text = upvotes.text.replace(".","").replace("k","00")
    comments_text = comments.text.split()[0].replace(".","").replace("k","00")
    print(upvotes_text)
    print(comments_text)

   
    with open("track.txt", "a") as file:
        file.write(str(i) + " | " + upvotes_text + " | " + comments_text + "\n")
        i+=1

    index = []
    com = []
    upvote = []
    with open("track.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            split_string = line.split("|")
            index.append(split_string[0])
            upvote.append(split_string[1])
            com.append(split_string[2])

    ax1.plot(index, upvote)
    ax1.set_title("Upvotes")
    ax1.set_xlim(0,10)

    ax2.plot(index, com)
    ax2.set_title("Comments")
    ax2.set_xlim(0, 10)
    plt.draw()
    plt.pause(20)

    time.sleep(20)
