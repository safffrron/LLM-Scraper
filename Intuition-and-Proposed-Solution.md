## Task in hand 
<pre>
To build an agent that is capable of fetching a user-level order details from the Amazon website.
</pre>

## Requirements and Intuition
<pre>
1. We can use either Javascript or Python to first login into Amazon and then scrape the required details.
2. We need to fetch the RAW HTML file which we can later give to model we'll be using.
3. We can then provide that HTML file to the model to extract the required details.
</pre>

## Things to keep in mind :
<pre>
1. We need to make sure that the agent is capable of handling the login process.
2. We need to make sure that the agent is capable of handling the CAPTCHA.
3. We need to make sure that the agent is capable of handling the dynamic nature of the website.
4. We need to make sure that the agent is capable of handling the changes in the website.
5. The agent should be able to handle different pages and interactions.
</pre>

## Libraries to be used :
<pre>
1. Selenium
2. Transformers / pipeline (for model)
3. JSON
4. OS and time 

Language used : Python
</pre>

## Why scraping using LLM and not simple text extraction?
<pre>
1. The web page is dynamic and changes regularly
2. The data is not in a structured format.
3. Helps us reduce time and effort in writing complex code.
4. Helps us in extracting the data in a more structured format specifically the way we want.
</pre>
