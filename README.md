# USEmbassyCrawler
This script crawls the Israeli US embassy website, and tries to schedule a visa interview meeting ASAP.
The USEmbassyCrawler script is relevant for users who already have a scheduled appointment to a vias interviw, 
and wish to find an earlier available appointment date. specifically - available slots in the next following 2 months. 

Steps:
1. log in to the embassy website given user credentials (should be entered in the main 
function by assigning the variables embassy_website_username + embassy_website_password).
2. go to the appointment schedule tab.
3. select appointment location (Jerusalem/Tel Aviv).
4. check if there are available slots in the next two months.
5. if there is a slot - reschedule interview date.

**Disclaimer: this script was created to crawl the US embassy website as it was defined on Nov 2021, changes in the website's structure
can affect the behavour of the script.
