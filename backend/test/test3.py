import json
import os
import sys
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

client = DocumentIntelligenceClient(
    endpoint=os.getenv('AZURE_DOC_URL', ''),
    credential=AzureKeyCredential(os.getenv('AZURE_DOC_KEY', ''))
)

with open(sys.argv[1], "rb") as f:
    data = f.read()
    # print(len(data))
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=data)
    )

result = poller.result()


print(f"Model: {result.model_id}")
print(f"Pages returned: {len(result.pages)}")

with open(f'debug.json', 'w') as f:
    json.dump(result.as_dict(), f, indent=4)

if not result.documents:
    print("doc process failed")
    sys.exit(1)


for idx, page in enumerate(result.documents):
    buffer = page.as_dict()
    with open(f'res_{idx}.json', 'w') as f:
        json.dump(buffer, f, indent=4)