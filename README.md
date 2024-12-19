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

## Note
The prophecy generation feature requires a working LM Studio installation with appropriate models. If you encounter any issues, please check the LM Studio documentation or raise an issue in this repository.
