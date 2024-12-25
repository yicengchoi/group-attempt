#  Memory and the Past: A Tarot Multimedia Experience

### Concept:

Create an interactive web page UI in the form of tarot cards, with content themes related to Dementia patients.

### About

Epidemiology

Dementia is one of the most common neurodegenerative disorders among the elderly, though there are also a small number of middle-aged patients. According to information from the Department of Health, one in 10 people aged 70 or above in Hong Kong suffers from dementia, with the rate increasing to one in three among those aged 85 or above. It is estimated that by 2036, there will be about 280,000 patients with dementia in Hong Kong.

### What is Dementia?

Also known as major neurocognitive disorder, dementia occurs when brain cells are damaged or lost at a faster rate than normal as a person ages. This can severely affect brain function across many areas such as memory, thinking, behavior, and the ability to care for oneself, and can negatively impact the quality of life of patients and family members.

This work utilizes data from https://dementiadiaries.org/, and we appreciate the resources provided by the website. This work is for non-commercial purposes only and does not involve any commercial activities or profit-making endeavors.


## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m tkinter
``` 

### 2. LM Studio Setup
To use the prophecy generation feature, you need to set up LM Studio:

1. Download and Install LM Studio
   - Download LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)
   - Install it on your system

2. Download the Required Model
   - Open LM Studio
   - Go to the Models tab
   - Search for "Meta Llama 3.1 8B Instruct"
   - Download the model

3. Start the Local Server
   - Select the downloaded model in LM Studio
   - Click "Start Server"
   - Ensure the server is running on `http://localhost:1234`
   - The server should show these endpoints:
     ```
     GET  http://localhost:1234/v1/models
     POST http://localhost:1234/v1/chat/completions
     POST http://localhost:1234/v1/completions
     POST http://localhost:1234/v1/embeddings
     ```

### 3. Alternative Models
If you can't use the meta-llama model, you can modify the code to use other models:
1. Open `attempt1.py`
2. Find the `generate_prophecy()` method
3. Change the "model" parameter in the API call:
   ```python
   "model": "meta-llama-3.1-8b-instruct"
   ```


### 4. Troubleshooting
If you encounter issues with the prophecy generation:
- Ensure LM Studio server is running
- Check if the correct model is loaded
- Verify the server port (default: 1234)
- Check the console for error messages

### Note
The prophecy generation feature requires a working LM Studio installation with appropriate models. If you encounter any issues, please check the LM Studio documentation or raise an issue in this repository.





## Memory Reader - Tarot Card Experience Guide

Welcome to our Tarot Card Experience! This experience consists of three card draws, each corresponding to a different theme: "Emotions", "Forgot", and "Wish". We have used web scraping technology to collect relevant sentences and author information from https://dementiadiaries.org/ to provide interpretations for the tarot cards.

### Step-by-Step Instructions

1.Launch the Server: Complete the LM Studio model loading and start the server.
![屏幕截图 2024-12-25 170000](https://github.com/user-attachments/assets/93d2bebd-6569-4f0a-bb4f-4a9f09c47d8e)


2.Run the Script: Run the attempt1.py script in the default group-attempt directory.


3.Access the Memory Reader Page: The Memory Reader page will pop up.
![屏幕截图 2024-12-25 144542](https://github.com/user-attachments/assets/eaa7eb02-ddce-48ad-b17e-4e32e0c08d4a)


4.Select a Card: Choose a card on each page and click the "seclet" button in the card interpretation pop-up window.
![屏幕截图 2024-12-25 143446](https://github.com/user-attachments/assets/4c0456e8-0d5c-423e-bd87-7a802dff4347)



5.Switch Themes: After selecting a card on one theme page, click the "next" button in the top-right corner to switch to the next theme page.


6.Review Your Selections: After selecting cards for all three themes, review your choices on the "Your Memory Cards" page.
![屏幕截图 2024-12-25 143756](https://github.com/user-attachments/assets/8494bb1f-3bae-4e83-883d-e95aaece2d85)



7.View Your Prophecy: Click the "prophecy memory" button to view your prophecy.
![屏幕截图 2024-12-25 143845](https://github.com/user-attachments/assets/08ddea71-1c58-49ec-82e3-5c7060c64306)



8.Restart: Click the "restart" button to start the experience again.



### Important Notes


1.Ensure that the LM Studio model has been loaded and the server has been started.

2.Run the attempt1.py script in the default group-attempt directory.

3.Follow the steps to select cards and switch themes.

