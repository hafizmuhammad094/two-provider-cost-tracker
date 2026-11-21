
import os
import sys
import time
import json
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()


def ask_gemini(prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    start = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    seconds = time.perf_counter() - start

    return {
        "provider": "gemini",
        "model": model,
        "reply": response.text,
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
        "seconds": seconds
    }


def ask_groq(prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    seconds = time.perf_counter() - start

    return {
        "provider": "groq",
        "model": model,
        "reply": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "seconds": seconds
    }


def main():
    prompt = " ".join(sys.argv[1:])

    if not prompt:
        prompt = input("Enter your prompt: ")

    results = []

    # Gemini request
    print("\nConnecting to Gemini...")

    start = time.perf_counter()

    try:
        gemini_result = ask_gemini(prompt)
        results.append(gemini_result)
        print("Gemini successful!")

    except Exception as error:
        results.append({
            "provider": "gemini",
            "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            "reply": None,
            "input_tokens": None,
            "output_tokens": None,
            "seconds": round(time.perf_counter() - start, 3),
            "error": str(error)
        })
        print("Gemini failed:", error)

    # Groq request
    print("\nConnecting to Groq...")

    start = time.perf_counter()

    try:
        groq_result = ask_groq(prompt)
        results.append(groq_result)
        print("Groq successful!")

    except Exception as error:
        results.append({
            "provider": "groq",
            "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
            "reply": None,
            "input_tokens": None,
            "output_tokens": None,
            "seconds": round(time.perf_counter() - start, 3),
            "error": str(error)
        })
        print("Groq failed:", error)

    # Calculate cost
    for result in results:
        provider = result["provider"].upper()

        input_price = float(
            os.getenv(provider + "_INPUT_PRICE_PER_M", "0")
        )

        output_price = float(
            os.getenv(provider + "_OUTPUT_PRICE_PER_M", "0")
        )

        result["input_price_per_m"] = input_price
        result["output_price_per_m"] = output_price

        if result["input_tokens"] is not None:
            cost = (
                result["input_tokens"] * input_price
                + result["output_tokens"] * output_price
            ) / 1000000

            result["cost_usd"] = cost
        else:
            result["cost_usd"] = None

    # Print responses
    for result in results:
        print("\n", result["provider"].upper(), "RESPONSE:")
        print(result["reply"] or result.get("error"))

    # Comparison table
    print("\nPROVIDER COMPARISON")
    print("Provider | Input Tokens | Output Tokens | Seconds | Cost USD")

    for result in results:
        print(
            result["provider"],
            "|", result["input_tokens"],
            "|", result["output_tokens"],
            "|", round(result["seconds"], 3),
            "|", result["cost_usd"]
        )

    # Save JSON
    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print("\nResults saved in results.json")


if __name__ == "__main__":
    main()
