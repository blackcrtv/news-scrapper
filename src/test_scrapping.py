#from db.elastic import ElasticSearch
# from scrappers import MediafaxScraper, EuronewsScraper

# db = ElasticSearch()

# Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text-classification", model="nlpodyssey/bert-multilingual-uncased-geo-countries-headlines")

from srcapper_src.TextTransformer import TextProcessor
text_processor = TextProcessor()
# summarized_text = text_processor.summarize(_text)
text = "Noi detalii ies la iveală în ancheta din cazul navei scufundate în Marea Neagră, în apropiere de Sfântu Gheorghe. Vasul care i-a salvat pe opt marinari supraviețuitori ar fi fost cel care a provocat scufundarea cargobotului Mohammad Z. Coliziunea dintre cele două nave e subiectul unei anchete demarate de procurori. O navă sub pavilion Tanzania s-a scufundat, în sâmbătă dimineață, în Marea Neagră, la 26 de mile marine de Sfântu Gheorghe. La bordul ei se aflau 11 cetățeni sirieni și egipteni, dintre care trei sunt încă dați dispăruți. Conform unor surse Euronews, marinarii ar fi spus că nava s-a scufundat în aproape trei minute după ce a fost lovită de o ambarcațiune mai mică, poate chiar de o dronă marină. Pe de altă parte, Sindicatul Navigatorilor lansează ipoteza unei coliziuni cu o navă mai mare."
tokenized_result = text_processor.tokenize(text)
# marked_entities_text = text_processor.mark_entities(text, tokenized_result)

# print(marked_entities_text
print(tokenized_result)

# scrapper = EuronewsScraper(db)
# scrapper.start_scrapping(3)