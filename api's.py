
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from text_summarization_with_openai import summarize_with_options, extract_text_from_document, get_translated_text
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)
class SummarizeTextInput(BaseModel):
    text_to_summarize: str
    number_of_words: int
    summary_format: str


class TranslateTextInput(BaseModel):
    text_to_translate: str
    target_language: str




@app.post("/summarize")
async def summarize_text(summary_data: SummarizeTextInput):
    summarized_text = await summarize_with_options(summary_data.text_to_summarize, summary_data.number_of_words, summary_data.summary_format)
    if summarized_text is None:
        raise HTTPException(status_code=500, detail="Failed to summarize text")
    else:
        return {"summary": summarized_text}




@app.post("/translate")
async def translate_text(translate_data: TranslateTextInput):
    translated_text = await get_translated_text(translate_data.text_to_translate, translate_data.target_language)
    if translated_text is None:
        raise HTTPException(status_code=500, detail="Failed to translate text")
    else:
        return {"translated_text": translated_text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)