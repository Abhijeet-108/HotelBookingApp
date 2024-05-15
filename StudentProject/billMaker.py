import pandas as pd
from fpdf import FPDF

article = pd.read_csv("articles.csv")

class Article:
    def __init__(self, article_id):
        self.id = article_id
        self.name = article.loc[article["id"] == self.id, 'name'].squeeze()
        self.price = article.loc[article["id"] == self.id, 'price'].squeeze()
    def available(self):
        in_stock = article.loc[article["id"] == self.id, 'name'].squeeze()
        return in_stock

class Reciept:
    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article.id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1)

        pdf.output("receipt.pdf")


print(article)
article_ID = int(input("Choose ID of a article: "))
articles = Article(article_id=article_ID)
if articles.available():
    reciept = Reciept(articles)
    reciept.generate()
else:
    print("Article you choose is not in stock......")


