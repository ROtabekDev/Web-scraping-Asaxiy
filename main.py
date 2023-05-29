import requests
from bs4 import BeautifulSoup
import json

language = ['uz', 'ru']
data = {}


def get_category_data(lang_list):
    category_data = []
    languages = lang_list
    for i in range(len(languages)):

        url = f"https://asaxiy.uz/{languages[i]}/product"

        response = requests.get(url=url)

        soup = BeautifulSoup(response.text, "lxml")

        a = soup.find_all("a", {'class': 'product__content__list__item__link'})

        for j in range(len(a)):
            category_name = a[j].text.strip()
            detail_url = f"https://asaxiy.uz{a[j].get('href')}"

            if i > 0:
                category_data[j][f'name_{languages[i]}'] = category_name
                category_data[j][f'detail_url_{languages[i]}'] = detail_url
            else:
                category_data.append(
                    {
                        'id': j + 1,
                        f'name_{languages[i]}': category_name,
                        f'detail_url_{languages[i]}': detail_url,
                    }
                )

    filtered_data = [d for d in category_data if "brand=" not in d['detail_url_uz']]

    file_name = "category_data.json"

    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)
    return filtered_data


def get_product_urls(category_data, lang_list):
    product_urls = []
    category_data = category_data
    languages = lang_list

    for i in range(len(languages)):
        for cat_id in range(1):  # for cat_id in range(len(category_data))

            category_detail_url = category_data[0][f'detail_url_{languages[i]}']  # category_data[cat_id]
            category_name = category_data[0][f'name_{languages[i]}']

            response = requests.get(url=category_detail_url)

            soup = BeautifulSoup(response.text, "lxml")

            pagination = soup.find_all("li", {'class': 'page-item'})
            page_count = len(pagination) - 2

            for k in range(page_count):

                url = f"{category_detail_url}/page={k + 1}"
                response = requests.get(url=url)

                soup = BeautifulSoup(response.text, "lxml")

                product_item = soup.find_all("div", {'class': 'col-6 col-xl-3 col-md-4'})

                for j in range(len(product_item)):
                    product_url = f"https://asaxiy.uz{product_item[j].find('a').get('href')}"
                    if i > 0:
                        product_urls[j + (k * 24)][f'detail_url_{languages[i]}'] = product_url
                        product_urls[j + (k * 24)][f'category_name_{languages[i]}'] = category_name
                    else:
                        product_urls.append(
                            {
                                'id': k * 24 + j + 1,
                                f'detail_url_{languages[i]}': product_url,
                                f'category_name_{languages[i]}': category_name,
                            }
                        )
    file_name = "product_urls.json"

    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(product_urls, file, indent=4,  ensure_ascii=False)
    return product_urls


def get_product_data(product_urls, lang_list):
    product_data = []

    languages = lang_list

    for i in range(len(languages)):
        for j in range(len(product_urls)):
            print(product_data)

            url = product_urls[j].get(f'detail_url_{languages[i]}')

            response = requests.get(url=url)

            soup = BeautifulSoup(response.text, "lxml")

            image_link = soup.find("div", class_='item__img').find('img')['src']

            product_title = soup.find("h1", class_='product-title').text
            product_price = soup.find("span", class_='price-box_new-price').get("content")

            split_url = url.split('/')
            product_slug = split_url[-1]

            description_item = soup.find("div", class_="description__item")
            p_elements = description_item.find_all("p")
            product_description = ' '.join([p.get_text(strip=True) for p in p_elements])

            product_category_name = product_urls[j].get(f'category_name_{languages[i]}')

            if i > 0:
                product_data[j][f'title_{languages[i]}'] = product_title
                product_data[j][f'description_{languages[i]}'] = product_description
                product_data[j][f'category_name_{languages[i]}'] = product_category_name
            else:
                product_data.append(
                    {
                        'id': j + 1,
                        f'title_{languages[i]}': product_title,
                        "image_link": image_link,
                        'price': product_price,
                        f'description_{languages[i]}': product_description,
                        'slug': product_slug,
                        'detail_url': url,
                        f'category_name_{languages[i]}': product_category_name
                    }
                )

    file_name = "product_data.json"

    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(product_data, file, indent=4, ensure_ascii=False)
    return product_data


def main():
    category_data = get_category_data(language)
    product_urls = get_product_urls(category_data, language)
    get_product_data(product_urls, language)


if __name__ == '__main__':
    main()
