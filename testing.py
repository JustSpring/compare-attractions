from bs4 import BeautifulSoup
import urllib.request


def getelements2(url, content_info, name_info, content_info2 ):
    element = ""
    des=""
    results_names = ""
    element2=""
    element3=""
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    print(soup)
    for link in soup.find_all("div", class_ = content_info):
        element1=link
        print(element1)
    # data = x
    # data2= str(x.get(b))
    # return data,data2

print(getelements2('https://www.leumi.co.il/LeumiBenefit/45575/23435','benefitInfo_content', 'h1','h2'))
#if __name__ == "__main__":
    #print(getoneinfo_and_class('benefitInfo_content', 'h1'))
