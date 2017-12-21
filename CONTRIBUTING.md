Back from holiday! Here are some problems we need to fix! More are coming. Message me or email me at shaerthomas@gmail.com if you have questions.


Current Bugs that need to be fixed:

1. The HTML page which handles all the inputs was saved from the EU version of the supreme checkout website. This means that US/Asia
cannot use the bot for shipping. Proposed changes to fix this:

Create a new HTML page for each region and get the bot to automatically check which region the user is in and load up that HTML page. (will involve having to create new HTML pages for each region)

(Perhaps a lot easier) Add more shipping values in the HTML. If the shipping address is a state we could use ajax to create a new select option for states.


2. Allow the bot to be able to run on Mac/Linux. Apparently theres also a problem with Windows 10, I would appreciate if someone could confirm this.

3. FIX THE LOADING TIME OF THE HTML FILE! Selenium cannot interact with the chrome page till it is fully loaded. That is why I used ajax to only allow the user
to submit the data when the page has loaded via a button. The HTML file was saved off of
Supreme's checkout page to save time. I'm sure this has led to a lot of broken code which is causing the page to take forever to load. At some point
the HTML page needs to be recreated completely, but for now the loading time has to be increased!

Ways to deal with Captcha:

1. load users chrome profile onto driver

2. 2captcha

Other improvements:

1. Change how to bot receives the information from the HTML website to the python code. I do not like having to type 'done', this was a temporary solution
to the problem

2. REMOVE ALL TIME.SLEEP(fixed constant) METHODS. This is temporary to deal with the fact that selenium does not always wait for elements to load before interacting with them. 
Need to create a new way of checking if the element has loaded. 'Implicit wait' is what we need as quoted from CakeFleet.

3. Since selenium runs chrome driver as a 'automated browser for testing purposes' I'm not surprised that Supreme can detect selenium. I am currently looking into different libraries that could be used. Alternatively I may develop my own library that utilises screen imaging technology to read the website off chrome/ie/Firefox or any other browser without the browser ever knowing. This will eliminate the need for selenium entitely, allowing for greater flexiblity of our project.
