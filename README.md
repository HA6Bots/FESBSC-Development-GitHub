# FESBSC-Development-GitHub
The official source code for FESBSC. Development is still in progress.
# Current plan
1. Make a good working **console** version with a **large** success rate.
2. Add the GUI back
3. Counter new anti-bot counter-measures
# Features
- Save payment information locally encrypted with AES
- Purchase multiple items at once, no more than one of each item allowed.
- Strict item selection. This will only buy an item which has a **100%** match to your specified information. This will try to guaranty NO wrong purchases due to timing or similar named items
- Select a specific size OR buy the first available size
- Time based purchase
- High chance to bypass reCAPTCHA if you login a head of time into a google account in the chrome window opened by the bot
- Automatically generate a log file to help debugging if problems occur
# Usage
### USE "Main.py" LOCATED IN THE "CommandL" FOLDER WITH PYTHON 3
1. If you have saved payment details, you can enter the used password and check if the information is correct.
Else you enter payment information and chose if you want to save the information.
2. Enter the product category
3. Enter keywords, use a comma to separate words e.g. RefleCTIve,slEEve,LoGo,PuFFer (not case sensitive)
4. Enter the product size or enter "D" to select the first available size or if there is no selectable size
5. Enter a colour or leave blank to select the first available colour
6. Confirm the given information for typos and such
7. Enter if you want to use **STRICT** item selection (RECOMMENDED TO USE THIS FEATURE BECAUSE OF POSSIBLE TIMING ISSUES)
8. Enter the drop hour e.g. enter 14 for 2:00PM
**OPTIONAL** open a new tab and login into a google account to try to bypass reCAPTCHA
9. Keep the bot and the chrome window open and pray to the supreme gods
### Contribution and issues
If you need help or advice, add danielyc&#35;9114 on discord or send an email to danielyc.moddev@gmail.com

If you encounter any problems with the bot or if you have enhancement suggestion,
make an Issue and please attach the logfile (if generated) or the python error

If you have a direct code attribution, fork and make a pull request

#### This will keep everything organised
