## LLM-Scraper

### Introduction 
The LLM Fetcher is a Python script that automates the task of fetching user-level order details from the Amazon website. By leveraging Selenium, the script navigates to the order history page, extracts key order details from each historical order, and saves them in a structured format.

Features: 
1. Automated navigation to the Amazon order history page.
2. Extraction of order details such as order number, product names, quantities, prices, and delivery status.
3. Saving of order details in raw HTML files with a structured naming convention.
4. Structured storage of order details in JSON or CSV format.
5. Secure handling of user authentication credentials.
6. Robust handling of unexpected events and website changes

For more info check  [Intuition-and-Proposed-Solution.md](Intuition-and-Proposed-Solution.md)

### Set-up
1. Clone this repository using :
   
   ```
   git clone https://github.com/safffrron/LLM-Scraper.git
   ```

   For more information on cloning refer - https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

2. Install selenium , by writing this in your terminal or your python notebook :
   ```
   pip install selenium 
   ```
   The other required dependencies like the LLM model , will automatically be installed during execution.

### Things to consider - 

1. You may incur an error while login in Amazon , specifically when there is a captcha page. In that case just enter the captcha manually and press enter , if the problem is not solved just sign in the browser manually and re run the block of code. This will solve the error.
   
2. This scraper works on a free openly available LLM taken from Huggingface.transformers called GPT neo. For improving the performance you can replace that by your own better LLM model such as GPT 4 and such.
   
3. When getting the order history , it only consider the default page that pops up. To include other pages , if there is next page button decomment the section as mentioned there.

### Running - 

For running via termial , first cd to this repo and execute - 
```
python main.py
```

### Understanding the code base - 

If you want to understand the codebase deeply , a notebook with all the comments is provided.
