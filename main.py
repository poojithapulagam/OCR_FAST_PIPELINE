from src.pipeline import OCRPipeline

pipeline = OCRPipeline()
results = pipeline.run()

for r in results:
    print("\n=== RESULT ===")
    print("Extracted Name:", r.get("name"))
    print("Extracted Address:", r.get("address"))

    # match key exists in pipeline output
    if r.get("match"):
        print("Match Found:", r["match"]["preferred_full_name"])
        print("Address:", r["match"]["address"])
    else:
        print("Match: No record found")
