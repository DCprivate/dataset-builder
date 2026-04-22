from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import sha256_text

from dataset_builder.ingest.text import TextIngester

def main():
    temp = sha256_text("test")
    print(temp)

    ingester = TextIngester()
    temp2 = ingester.ingest("here")
    print(temp2)

if __name__ == "__main__":
    main()
