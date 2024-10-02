![cover](https://github.com/user-attachments/assets/9bed0677-3d03-4021-99a9-15fa1d0c5cac)

 Vision of Voice Application

This application allows users to describe images using their voice, converting the audio input into text with the OpenAI Whisper-1 model, and then generating an image from that text using the DALL-E model. Users can also obtain descriptions of their generated images via GeminiAI.

### How does App work?

![diyagram](https://github.com/user-attachments/assets/60be426e-eb8f-42f2-b4ee-8784f5bd30c6)



### Features

- **Whisper-1 Model**: Utilizes the OpenAI Whisper-1 model to convert audio recordings into text.
- **DALL-E Model**: Employs the DALL-E model to generate images from text.
- **Description Retrieval**: Users can click the "Describe" button to obtain descriptions of their generated images.

### Usage Instructions

1. **API Keys**: Enter your OpenAI and GoogleAI API keys in the left-side menu.
2. **Record Audio**: Use the application interface to record your voice.
3. **Check Audio**: Click the "Check" button to review your recorded audio.
4. **Send to AI**: You can either send the audio or use the direct send option.

### Libraries
```python
openai==1.48.0
streamlit==1.38.0
Wave==0.0.2
google-generativeai==0.8.2
streamlit-audiorec
```
### Requirements

- OpenAI API Key
- GoogleAI API Key

### Notes

- This application is developed for individual experiences and is not a commercial product.

### Contributing

If you have any suggestions or feedback regarding errors, please feel free to reach out to me on LinkedIn.

