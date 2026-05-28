from transformers import pipeline

# Use text-generation instead of summarization
generator = pipeline(
    "text-generation",
    model="gpt2"
)

def generate_summary(text):

    try:

        prompt = f"Summarize this passport-related post in one short sentence:\n{text}\nSummary:"

        result = generator(
            prompt,
            max_new_tokens=30,
            truncation=True
        )

        output = result[0]["generated_text"]

        # Extract summary part
        summary = output.split("Summary:")[-1].strip()

        return summary

    except Exception as e:
        return "AI summary unavailable."