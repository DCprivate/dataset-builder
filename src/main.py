from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import sha256_text

from dataset_builder.ingest.text import TextIngester
from dataset_builder.ingest.pdf import PdfIngester
from dataset_builder.ingest.web import WebsiteIngester
from dataset_builder.ingest.youtube import YouTubeIngester

def main():

    """ingester = TextIngester()
    temp = ingester.ingest("../examples/example.txt")
    print(temp)
    
    ingester_pdf = PdfIngester()
    temp2 = ingester_pdf.ingest("../examples/pdf_test.pdf")
    print(temp2)
    
    ingester_web = WebsiteIngester()
    temp3 = ingester_web.ingest("https://en.wikipedia.org/wiki/Middle_Nevka")
    #print(temp3)"""
    
    ingester_youtube = YouTubeIngester()
    temp4 = ingester_youtube.ingest("https://www.youtube.com/watch?v=U4gpio58908")
    print(temp4)

if __name__ == "__main__":
    main()
